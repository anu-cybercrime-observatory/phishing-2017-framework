#!/usr/bin/python3

"""
listen.py

This is the clearpixel listener that is used to determine when an email has been opened by the recipient.

Listener id: 5
Activity id: 1 only.
"""


import os
import cgi
import time
import database


# the data we want is encoded in the following format:
# <16 bytes of junk>AAACC<more junk>
#
# where AAA is the user identifier and
# CC is the batch number

data = cgi.FieldStorage()
dataString = ""
if 'x' in data:
    dataString = data['x'].value

    if len(dataString) > 20:
        user_id = dataString[16:19]
        batch_id = dataString[19:21]

        whatCode = "51"     # 5 for the clearpixel listener, 1 for the 'page opened'
        ip = os.environ["REMOTE_ADDR"]

        # confirmation of a valid code, so save to the database.
        insertQuery = "INSERT INTO activity (what, user_id, batch_id, datetime, ip_address) VALUES (" \
                      + whatCode + ", " + str(int(user_id)) + ", " + str(int(batch_id)) + ", " + str(int(time.time())) \
                      + ", '" + ip + "')"

        db = database.Database()
        db.ExecuteInsert(insertQuery)
        db.Close()

# return the clearpixel image.
print("Location: http://listen.cybercrime-observatory.tech/clear.png\n\n")
