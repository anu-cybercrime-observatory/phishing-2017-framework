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
template_data = CreateDefaultTemplateVariables()

if action == "save":
    if email_id in email_index:
        # update existing ..
        email = email_index[email_id]
        email.SetName(data['template_name'].value)
        email.SetSubject(data['template_subject'].value)
        email.SetOriginatingName(data['template_orgname'].value)
        email.SetOriginatingEmail(data['template_orgemail'].value)
        email.SetBody(data['template_body'].value)

        db.ExecuteQuery(email.UpdateSQL())
    else:
        # insert new
        email = Email.Email()
        email.SetName(data['template_name'].value)
        email.SetSubject(data['template_subject'].value)
        email.SetOriginatingName(data['template_orgname'].value)
        email.SetOriginatingEmail(data['template_orgemail'].value)

        id = db.ExecuteInsert(email.InsertSQL())

        email.SetID(id)
        email.SetBody(data['template_body'].value)

    # redirect to viewEmails list!
    print("Location: viewEmailTemplates.py\n\n")
    exit(0)

else:
    if email_id in email_index:
        PopulateData(template_data, email_index[email_id])


# Print the template out to the screen.

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

with open("htmlTemplates/editEmailTemplate.html") as inputFile:
    lines = inputFile.readlines()

for line in lines:
    line = line.strip()
    line = line.replace("<$EMAIL_ID>", str(email_id))
    line = line.replace("<$EMAIL_NAME>", template_data['template_name'])
    line = line.replace("<$EMAIL_SUBJECT>", template_data['template_subject'])
    line = line.replace("<$EMAIL_ORGNAME>", template_data['template_orgname'])
    line = line.replace("<$EMAIL_ORGEMAIL>", template_data['template_orgemail'])

    bodyCode = template_data['template_body']
    bodyCode = bodyCode.replace("&", "&amp")

    line = line.replace("<$EMAIL_BODY>", bodyCode)

    print(line)
