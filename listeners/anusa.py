#!/usr/bin/python3

"""
listen.py

Listener for activities on our fake ANUSA pages.

Listener id: 6
Activity id: 1 and 2.
Extra information: PageId - the fake page to serve up, since this listener is used across multiple fake pages.
"""


import os
import cgi
import time
import database


# the data we want is encoded in the following format:
# <16 bytes of junk>AAACCPP<more junk>
#
# where AAA is the user identifier and
# CC is the batch number
# PP is the page number - the page to load up.

destination = "http://www.cybercrime-observatory.tech/landing.html"
data = cgi.FieldStorage()
dataString = ""

if 'form_submit' in data:
    # extract the data, save to the database, and redirect to the landing page.
    batch       = int(data['batch_id'].value)
    participant = int(data['user_id'].value)

    # Form submit! So save that and redirect to landing page.
    whatCode = "62"
    destination = "http://www.cybercrime-observatory.tech/landing.html"

    try:
        ip = os.environ["REMOTE_ADDR"]

        # confirmation of a valid code, so save to the database.
        insertQuery = "INSERT INTO activity (what, user_id, batch_id, datetime, ip_address) VALUES (" \
                      + whatCode + ", " + str(participant) + ", " + str(batch) + ", " + str(int(time.time())) \
                      + ", '" + ip + "')"

        db = database.Database()
        db.ExecuteInsert(insertQuery)
        db.Close()

        # redirect to the destination location
        print("Location: " + destination + "\n\n")
        exit()

    except Exception as e:
        pass

elif 'x' in data:
    dataString = data['x'].value

    if len(dataString) > 22:
        user_id = int(dataString[16:19])
        batch_id = int(dataString[19:21])
        page_id = int(dataString[21:23])

        # Page ID will determine what to do here.
        whatCode = None
        if page_id == 1:
            # Giveaway for Ed tickets.
            whatCode = "61"
            destination = "ed_sheerhan.html"

        elif page_id == 2:
            # Giveaway for AFL tickets.
            whatCode = "61"
            destination = "grand_finals.html"

        if whatCode:
            ip = os.environ["REMOTE_ADDR"]

            # confirmation of a valid code, so save to the database.
            insertQuery = "INSERT INTO activity (what, user_id, batch_id, datetime, ip_address) VALUES (" \
                          + whatCode + ", " + str(user_id) + ", " + str(batch_id) + ", " + str(int(time.time())) \
                          + ", '" + ip + "')"

            db = database.Database()
            db.ExecuteInsert(insertQuery)
            db.Close()

            # load the contents of the destination
            # apply BATCH_ID and USER_ID to the template.
            print("Content-Type: text/html")  # HTML is following
            print()  # blank line, end of headers

            with open(destination) as inputFile:
                lines = inputFile.readlines()

            for line in lines:
                line = line.strip()
                line = line.replace("<USER_ID>", str(user_id))
                line = line.replace("<BATCH_ID>", str(batch_id))

                print(line)

            exit()

print("Location: http://www.cybercrime-observatory.tech/landing.html\n\n")
