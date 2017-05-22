#!/usr/bin/python3

import os
import cgi
import time
import database


# the data we want is encoded in the following format:
# AAABCC<md5 hash of AAA>
# where AAA is the user identifier and
# B is the activity to record
# CC is the batch number
data = cgi.FieldStorage()
dataString = ""
if 'z' in data:
    dataString = data['z'].value
else:
    print("Location: http://www.cybercrime-observatory.tech/landing.html\n\n")
    exit(0)

try:
    uid = dataString[0:3]
    tid = dataString[3]
    bid = dataString[4:6]
    ip = os.environ["REMOTE_ADDR"]
    hash = "c30bb76b355a39dcd9e73bfb934b380d"
    hashHalf = dataString[6:]

    # 1st digit is a '1' for the landing page - this listener - so add 10 to the whatcode.
    what = str(10 + int(tid))

    if hashHalf == hash:
        # finally
        # confirmation of a valid code, so save to the database.
        insertQuery = "INSERT INTO activity (what, user_id, batch_id, datetime, ip_address) VALUES (" \
                      + what + ", " + str(int(uid)) + ", " + str(int(bid)) + ", " + str(int(time.time())) \
                      + ", '" + ip + "')"

        db = database.Database()
        db.ExecuteInsert(insertQuery)
        db.Close()

except Exception as e:
    print("Content-Type: text/html")  # HTML is following
    print()  # blank line, end of headers
    print(str(e))
    exit(0)
    pass

if 'url' in data:
    destination = data['url'].value
else:
    destination = "http://www.cybercrime-observatory.tech/landing.html"

print("Location: " + destination + "\n\n")
