#!/usr/bin/python3

import database
import Email


# load the relevant data from the database.
db = database.Database()
emails = db.LoadFromDatabase(Email.Email.table_name, Email.CreateFromSQL)
email_index = dict()
for email in emails:
    email_index[email.ID()] = email


template_loop_lines = ["<tr><td>" + e.Name()
                       + "</td><td>" + e.Subject()
                       + "</td><td>" + e.FromAppearance().replace("<", "&lt;").replace(">", "&gt;")
                       + "</td><td>"
                       + "<input type='button' value='Edit' onclick=\"location.href = 'editEmailTemplate.py?email_id=" + str(e.ID()) + "';\" />"
                       + "<input type='button' value='View' onclick=\"window.open('viewEmail.py?id=" + str(e.ID()) + "', '_newTab');\" />"
                       + "</td></tr>" for e in emails]
template_loop = "\n".join(template_loop_lines)

# Print the template out to the screen.

print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

with open("htmlTemplates/viewEmailTemplates.html") as inputFile:
    lines = inputFile.readlines()

for line in lines:
    line = line.strip()
    line = line.replace("<$TEMPLATE_LOOP>", template_loop)

    print(line)
