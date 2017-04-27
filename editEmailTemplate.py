#!/usr/bin/python3

import cgi
import database
import Email


def CreateDefaultTemplateVariables():
    template_data = dict()
    template_data['template_name'] = ""
    template_data['template_subject'] = ""
    template_data['template_orgname'] = ""
    template_data['template_orgemail'] = ""
    template_data['template_body'] = ""
    template_data['action'] = "new"

    return template_data


def PopulateData(template_data, email_template):
    """
    Inserts into the given template data dictionary the email template fields
    stored in the email_template object.

    :param template_data:
    :param email_template:
    :return:
    """
    template_data['template_name'] = email_template.Name()
    template_data['template_subject'] = email_template.Subject()
    template_data['template_orgname'] = email_template.OriginatingName()
    template_data['template_orgemail'] = email_template.OriginatingEmail()
    template_data['template_body'] = email_template.Body()


def generateEmail(sqlData):
    res = dict()
    res['id'] = int(sqlData[0])
    res['name'] = sqlData[2]

    return res


# if we've been asked to display a template, get that template.
data = cgi.FieldStorage()
if 'email_id' in data:
    email_id = int(data['email_id'].value)
else:
    email_id = 0

if 'action' in data:
    action = data['action'].value
else:
    action = ""


# load the relevant data from the database.
db = database.Database()
emails = db.LoadFromDatabase(Email.Email.table_name, Email.CreateFromSQL)
email_index = dict()
for email in emails:
    email_index[email.ID()] = email


# set some default values for the variables to insert into the template.
template_data = dict()
template_data['template_name'] = ""
template_data['template_subject'] = ""
template_data['template_orgname'] = ""
template_data['template_orgemail'] = ""
template_data['template_body'] = ""


template_data = CreateDefaultTemplateVariables()
if action == "view":
    template_data['action'] = "save"
    if email_id in email_index:
        PopulateData(template_data, email_index[email_id])

elif action == "save":
    template_data['action'] = "save"
elif action == "new":
    template_data['action'] = "save"


options = ["<option value='" + str(e.ID()) + "'>" + e.Name() + "</option>" for e in emails]
emailSelect = "<select name='email_id'><option value='0'>New ..</option>"\
              + "\n".join(options) + "</select>"

# Print the template out to the screen.

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

with open("htmlTemplates/editEmailTemplate.html") as inputFile:
    lines = inputFile.readlines()

for line in lines:
    line = line.strip()
    line = line.replace("<$ACTION>", template_data['action'])
    line = line.replace("<$EMAILS_DROPDOWN>", emailSelect)
    line = line.replace("<$EMAIL_ID>", str(email_id))
    line = line.replace("<$EMAIL_NAME>", template_data['template_name'])
    line = line.replace("<$EMAIL_SUBJECT>", template_data['template_subject'])
    line = line.replace("<$EMAIL_ORGNAME>", template_data['template_orgname'])
    line = line.replace("<$EMAIL_ORGEMAIL>", template_data['template_orgemail'])
    line = line.replace("<$EMAIL_BODY>", template_data['template_body'])

    print(line)
