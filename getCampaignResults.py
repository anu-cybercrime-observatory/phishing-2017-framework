#!/usr/bin/python3

import datetime
import database
import batch
import json


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


print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers


db = database.Database()

batches = batch.LoadAll(db)
groups = db.LoadFromDatabase("groups", getSql)
group_index = dict()
for (group_id, group_name) in groups:
    group_index[group_id] = group_name

batch_join = db.LoadFromDatabase("batch_group", getSql)
for (batch_id, group_id) in batch_join:
    if batch_id in batches:
        batches[batch_id].AddGroup(group_id)

activityData = db.LoadFromDatabase("activity", processActivity)
for activity in activityData:
    if activity['batch_id'] in batches:
        batches[activity['batch_id']].AddActivity(activity['activity_type'], activity['user_id'])

results = []
for batch in batches.values():
    jsonDict = dict()
    jsonDict['id'] = batch.ID()
    jsonDict['group_ids'] = batch.Groups()
    jsonDict['subject_id'] = batch.email_id
    jsonDict['timestamp'] = batch.timestamp
    jsonDict['results'] = batch.MaximalActivity()
    jsonDict['formatted_time'] = datetime.datetime.fromtimestamp(batch.timestamp).strftime('%Y-%m-%d %H:%M:%S')
    results.append(jsonDict)

print(json.dumps(results))
