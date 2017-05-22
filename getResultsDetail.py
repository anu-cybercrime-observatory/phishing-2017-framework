#!/usr/bin/python3

from datetime import datetime, timedelta
import database
import batch
import json
import cgi


def returnDayBox(startingTimestamp, currentTimestamp):
    """
    Returns a number from 0 to 23 representing which 4-hour block currentTimestamp fits in to
    relative to startingTimestamp, which occupies block zero. startingTimestamp has been rounded down
    to the nearest 4-hour start point (0:00, 4:00, 8:00, 12:00, 16:00, 20:00)

    :param startingTimestamp:
    :param currentTimestamp:
    :return:
    """
    return int((currentTimestamp - startingTimestamp) / (60 * 60 * 2))


def normaliseStartingTimestamp(startingTimestamp):
    """
    Normalise the timestamp to floor[four hour interval]
    :param startingTimestamp:
    :return:
    """
    return int(startingTimestamp / (60 * 60 * 2)) * 60 * 60 * 2


def getActivityType(activityId):
    if activityId is 0:
        return "Email Sent"

    listener = int(activityId / 10)
    activity = activityId % 10

    listeners = ['zero', 'Landing Page', 'ISIS', 'Wattle', 'Landing Page']
    activities = ['zero', 'Page Opened', 'Form Submitted']

    return listeners[listener] + " - " + activities[activity]


def getSql(sql):
    """
    This function does nothing at all, since the SQL result is in the format
    (id, group_name) and can be processed rapidly once all the results are out of the database.
    :param sql:
    :return:
    """
    return sql


def processActivity(sql):
    """
    Returns a dictionary containing the data found within the activity table.

    id, what, user_id, batch_id, datetime, ip_addy

    Only interested in what, user_id and batch_id in this case!

    :param sql:
    :return:
    """
    _, what, u_id, b_id, _, _ = sql

    res = dict()
    res['activity_type'] = what
    res['batch_id'] = b_id
    res['user_id'] = u_id
    return res


# Which of our many batches are we interested in?
data = cgi.FieldStorage()
batch_id = int(data['id'].value) if 'id' in data else 0

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers


db = database.Database()

batches = batch.LoadAll(db)
groups = db.LoadFromDatabase("groups", getSql)
group_index = dict()
for (group_id, group_name) in groups:
    group_index[group_id] = group_name


query = "SELECT u.id, u.groupId, a.what, a.datetime FROM user u, batch b, activity a" \
        " WHERE a.batch_id = b.id AND u.id = a.user_id AND b.id = " + str(batch_id)

holding = dict()
activityData = db.ExecuteSelectQuery(query)
startingTimestamp = ""
for activity in activityData:
    user_id, group_id, activity_id, timestamp = activity

    if activity_id not in holding:
        holding[activity_id] = dict()

    if group_id not in holding[activity_id]:
        holding[activity_id][group_id] = dict()

    if user_id not in holding[activity_id][group_id]:
        holding[activity_id][group_id][user_id] = timestamp

    if activity_id is 0:
        if startingTimestamp == "" or int(timestamp) < int(startingTimestamp):
            startingTimestamp = timestamp

startingTimestamp = int(startingTimestamp)

# Try to work out which 'box' to begin from
# Need the 'date' of the timestamp
# All data starts from Midnight -> 4am on the date of dispatch.
startingTimestamp = normaliseStartingTimestamp(startingTimestamp)

results = []
for key in holding.keys():
    outerDict = dict()
    workingDict = holding[key]

    newDict = []
    for groupKey in workingDict.keys():
        timeIntervals = [0] * 24
        for userKey in workingDict[groupKey]:
            timestamp = workingDict[groupKey][userKey]
            timestamp = returnDayBox(startingTimestamp, timestamp)
            if 0 <= timestamp < 24:
                timeIntervals[timestamp] += 1

        innerDict = dict()
        innerDict['group_id'] = groupKey
        innerDict['group_name'] = group_index[groupKey]
        innerDict['count'] = len(workingDict[groupKey])
        innerDict['time_intervals'] = timeIntervals
        newDict.append(innerDict)

    outerDict['activity_id'] = key
    outerDict['activity_type'] = getActivityType(key)
    outerDict['results'] = newDict

    results.append(outerDict)

print(json.dumps(results))
