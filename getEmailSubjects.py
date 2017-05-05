#!/usr/bin/python3

import database
import json
import Email


print("Content-Type: text/html")    # HTML is following
print()                             # blank line, end of headers

db = database.Database()
emails = Email.LoadAll(db)

results = []
for email in emails:
    json_email = dict()
    json_email['id'] = email.ID()
    json_email['subject'] = email.Subject()
    results.append(json_email)

print(json.dumps(results))
