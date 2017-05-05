#!/usr/bin/python3

import os
import cgi
import sys
import time
import database

# ISIS landing page listener
# If no form submit detected, record ACTIVITY 1 in the database ("Open listening page")
# and display the ISIS template.
# If form submit detected, record ACTIVITY 2 in the database ("Form submitted")
# and redirect to the cyber landing page.
ip          = os.environ["REMOTE_ADDR"]
activity    = ""
batch       = ""
participant = ""
redirection = False

data        = cgi.FieldStorage()
dataString  = ""
dataValid   = False

if 'form_submit' in data:
    # extract the data, save to the database, and redirect to the landing page.
    activity    = data['activity_id'].value
    batch       = data['batch_id'].value
    participant = data['participant_id'].value

    redirection = True
    dataValid   = True

else:
    # extract the data, save to the database, and display the ISIS template.
    if 'cmd' in data:
        dataString  = data['cmd'].value
        participant = dataString[0:3]
        activity    = dataString[3]
        batch       = dataString[4:6]
        hash        = "c30bb76b355a39dcd9e73bfb934b380d"
        hashHalf    = dataString[6:]

        if hash == hashHalf:
            dataValid = True
        else:
            redirection = True
    else:
        # passed a shitty URL, so redirect to the landing page
        redirection = True


if dataValid:
    try:
        # finally
        # confirmation of a valid code, so save to the database.
        insertQuery = "INSERT INTO activity (what, user_id, batch_id, datetime, ip_address) VALUES (" \
                      + str(int(activity)) + ", " + str(int(participant)) + ", " + str(int(batch)) + ", " + str(int(time.time())) \
                      + ", '" + ip + "')"

        db = database.Database()
        db.ExecuteInsert(insertQuery)
        db.Close()

    except Exception as e:
        # @todo remove this code before the site goes live
        print("Content-Type: text/html")  # HTML is following
        print()  # blank line, end of headers
        print(str(e))
        exit(0)
        pass


if redirection:
    redirection = "http://www.cybercrime-observatory.tech/landing.html"
    print("Location: " + redirection + "\n\n")
else:
    # load the ISIS.html template
    # substitute
    # print
    # Print the template out to the screen.

    print("Content-Type: text/html")  # HTML is following
    print()  # blank line, end of headers

    with open("ISIS.html") as inputFile:
        lines = inputFile.readlines()

    for line in lines:
        line = line.strip()
        line = line.replace("<PARTID>", participant)
        line = line.replace("<BATCHID>", batch)

        print(line)
