#!/usr/bin/python3

import cgi
import database
import participant

from templateGenerator import TemplateGenerator


def generateGroup(sqlData):
    res = dict()
    res['id'] = int(sqlData[0])
    res['name'] = sqlData[1]
    res['option'] = "<option value='" + str(sqlData[0]) + "'>" + sqlData[1] + "</option>"
    return res


def generateLink(sqlData):
    res = dict()
    res['user_id'] = sqlData[0]
    res['group_id'] = sqlData[1]
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
people_index = dict()
for person in people:
    people_index[person._id] = person

user_group_link = db.LoadFromDatabase("user_group_join", generateLink)

if selectedGroup is not 0:
    listOfPeople = []
    for join in user_group_link:
        if int(join['group_id']) is selectedGroup:
            p = people_index[join['user_id']]
            listOfPeople.append("<tr><td>" + str(p._id) + "</td><td>" + group_index[p.group_id]['name'] + "</td></tr>")

    peopleRows = "\n".join(listOfPeople)
else:
    peopleRows = "<tr><td colspan='2'>No data</td></tr>"

groups2 = [g['option'] for g in groups]

groupSelect = "<select name='group'>" + "\n".join(groups2) + "</select>"


variables = dict()
variables['WEBSITE_TITLE'] = "Spear Phishing Control Panel"
variables['PAGE_HEADING'] = "Participant Groups"
variables['PAGE_SCRIPTS'] = ""
variables['PAGE_ONLOAD'] = ""
variables['GROUPS_DROPDOWN'] = groupSelect
variables['GROUP_ROWS'] = peopleRows

template = TemplateGenerator("viewGroups")
template.parse(variables)
