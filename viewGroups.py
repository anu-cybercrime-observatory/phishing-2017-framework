#!/usr/bin/python3

import cgi
import database
import participant


def generateGroup(sqlData):
    res = dict()
    res['id'] = int(sqlData[0])
    res['name'] = sqlData[1]
    res['option'] = "<option value='" + str(sqlData[0]) + "'>" + sqlData[1] + "</option>"
    return res


# if we've been asked to display a group, get that group.
data = cgi.FieldStorage()
if 'group' in data:
    selectedGroup = int(data['group'].value)
else:
    selectedGroup = 0


db = database.Database()
groups = db.LoadFromDatabase("groups", generateGroup)
group_index = dict()
for group in groups:
    group_index[group['id']] = group

people = participant.LoadAll(db)

if selectedGroup is not 0:
    people = ["<tr><td>" + str(p._id) + "</td><td>" + group_index[p.group_id]['name'] + "</td></tr>"
              for p in people if int(p.group_id) is selectedGroup]
    peopleRows = "\n".join(people)
else:
    peopleRows = "<tr><td colspan='2'>No data</td></tr>"

groups2 = [g['option'] for g in groups]

groupSelect = "<select name='group'>" + "\n".join(groups2) + "</select>"

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

with open("htmlTemplates/viewGroups.html") as inputFile:
    lines = inputFile.readlines()

for line in lines:
    line = line.strip()
    line = line.replace("<$GROUPS_DROPDOWN>", groupSelect)
    line = line.replace("<$GROUP_ROWS>", peopleRows)
    print(line)

db.Close()
