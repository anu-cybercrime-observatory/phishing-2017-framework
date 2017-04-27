#!/usr/bin/python3

import cgi
import database
import Email


# if we've been asked to display a template, get that template.
data = cgi.FieldStorage()
if 'id' in data:
    email_id = int(data['id'].value)
else:
    email_id = 0


# load the relevant data from the database.
db = database.Database()
emails = db.LoadFromDatabase(Email.Email.table_name, Email.CreateFromSQL)
email_index = dict()
for email in emails:
    email_index[email.ID()] = email

if email_id in email_index:
    email = email_index[email_id]
    subject = email.Subject()
    body = email.Body()
else:
    subject = "No email"
    body = "<p>Invalid email ID provided</p>"

# Print the template out to the screen.

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

with open("htmlTemplates/viewEmail.html") as inputFile:
    lines = inputFile.readlines()

for line in lines:
    line = line.strip()
    line = line.replace("<$SUBJECT>", subject)
    line = line.replace("<$BODY>", body)

    print(line)
