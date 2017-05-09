#!/usr/bin/python3

import database
import batch
import json
import cgi


def getActivityType(activityId):
    if activityId is 0:
        return "Email Sent"
    if activityId is 1:
        return "Link Clicked"
    if activityId is 2:
        return "Form Submitted"

    return "Unknown Activity"


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


query = "SELECT u.id, u.groupId, a.what FROM user u, batch b, activity a" \
        " WHERE a.batch_id = b.id AND u.id = a.user_id AND b.id = " + str(batch_id)

holding = dict()
activityData = db.ExecuteSelectQuery(query)
for activity in activityData:
    user_id, group_id, activity_id = activity

    if activity_id not in holding:
        holding[activity_id] = dict()

    if group_id not in holding[activity_id]:
        holding[activity_id][group_id] = dict()

    holding[activity_id][group_id][user_id] = True

results = []
for key in holding.keys():
    outerDict = dict()
    workingDict = holding[key]

    newDict = []
    for groupKey in workingDict.keys():
        numberUnique = len(workingDict[groupKey])

        innerDict = dict()
        innerDict['group_id'] = groupKey
        innerDict['group_name'] = group_index[groupKey]
        innerDict['count'] = numberUnique
        newDict.append(innerDict)

    outerDict['activity_id'] = key
    outerDict['activity_type'] = getActivityType(key)
    outerDict['results'] = newDict

    results.append(outerDict)

print(json.dumps(results))
