#!/usr/bin/python3

import database
import json


def getSql(sql):
    return sql

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

db = database.Database()
groups = db.LoadFromDatabase("groups", getSql)

results = []
for (group_id, group_name) in groups:
    json_group = dict()
    json_group['id'] = group_id
    json_group['name'] = group_name
    results.append(json_group)

print(json.dumps(results))
