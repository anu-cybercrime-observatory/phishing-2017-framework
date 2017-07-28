#!/usr/bin/python3

import database
import Email

from templateGenerator import TemplateGenerator


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
                       + "<input type='button' value='Edit' onclick=\"location.href = 'editEmailTemplate.py?email_id=" + str(e.ID()) + "';\"" + ("" if e.IsEditable() else " disabled") + "/>"
                       + "<input type='button' value='View' onclick=\"window.open('viewEmail.py?id=" + str(e.ID()) + "', '_newTab');\" />"
                       + "</td></tr>" for e in emails]
template_loop = "\n".join(template_loop_lines)

variables = dict()
variables['WEBSITE_TITLE'] = "Spear Phishing Control Panel"
variables['PAGE_HEADING'] = "Email Templates"
variables['PAGE_SCRIPTS'] = ""
variables['PAGE_ONLOAD'] = ""
variables['TEMPLATE_LOOP'] = template_loop

template = TemplateGenerator("viewEmailTemplates")
template.parse(variables)
