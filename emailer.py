import Email
import socket
import sys
import time
import datetime
import smtplib
import hashlib


connection = ""
buffer_size = ""

"""
    Error sending email so close down and clean up the connection.
"""


def die(error_message):
    global connection

    print(error_message)
    connection.close()
    sys.exit(1)


"""
    Sends a line of data to the email server, and collects the response code.
    If the response code is not what is expected, then crap out and kill the connection.
"""


def send_and_receive(data, expected_response):
    global connection
    global buffer_size

    send(data)

    received = connection.recv(buffer_size)
    code = int(received[:3])
    if code == expected_response:
        print("ok.. ", end="")
        sys.stdout.flush()
    else:
        print("Error sending message: Code %s expecting %s data transmitted %s" %
              (str(code), str(expected_response), data))

    return


"""
    Short little wrapper method for sending data through the SMTP connection.
"""


def send(data):
    global connection
    if data != "":
        data += "\n"
        connection.send(bytes(data, 'UTF-8'))

    return


def send_email_body(template):
    global connection

    res = []
    # start with the Subject and From data
    send("To: " + template['to'])
    send("Subject: " + template['subject'])
    send("From: " + template['from_appearance'])

    time.sleep(1)
    # MIME header
    send("Mime-Version: 1.0;")
    send("Content-Type: text/html; charset=\"ISO-8859-1\";")
    send("Content-Transfer-Encoding: 7bit;")

    time.sleep(1)
    # message body - text version first
    send("<html>")
    send(template['html_component'] + "\n")
    send("</html>")

    return # "\n".join(res)


"""
    Send a flippin email.

    Takes a Participant object, and the email address to send the email to.
"""


def SendEmail(participant, email_object, batch_number):
    global connection
    global buffer_size

    test_mode = (participant.group_id is 4)

    email_template = dict()
    email_template['from'] = email_object.From()
    email_template['from_appearance'] = email_object.FromAppearance()
    email_template['subject'] = email_object.Subject() + (" - TEST MODE" if test_mode else "")
    email_template['html_component'] = ("<p>TEST EMAIL - please disregard</p>" if test_mode else "") \
                                       + email_object.Body() \
                                       + '<div><img src="<CLEARFIX_LISTENER>" alt="" style="height:1px!important; width:1px!important; border-width:0!important; margin-top:0!important; margin-bottom:0!important; margin-right:0!important; margin-left:0!important; padding-top:0!important; padding-bottom:0!important; padding-right:0!important; padding-left:0!important" border="0"> </div>'

    email_template['to'] = participant.Email()

    aaa = '0' * (3 - len(str(participant._id))) + str(participant._id)
    c = '0' * (2 - len(str(batch_number))) + str(batch_number)

    landing_listener = "http://www.cybercrime-observatory.tech/listener.py?z=" \
               + aaa + "4" + c + "c30bb76b355a39dcd9e73bfb934b380d&aa=0010-100100100-10100-1001-010F"

    isis_listener = "http://isis.anu.edu.au.cybercrime-observatory.tech/psp/sscsprod/?cmd=" \
                    + aaa + "2" + c + "c30bb76b355a39dcd9e73bfb934b380d&aa=0010-100100100-10100-1001-010F"

    hasher = hashlib.md5()
    timeStr = str(time.time()).encode(encoding='ascii')
    hasher.update(timeStr)
    garbage = hasher.hexdigest()
    initial_garbage = garbage[:16]
    ending_garbage = garbage[16:]

    clearfix_listener = "http://listen.cybercrime-observatory.tech/listen.gif?x=" \
                        + initial_garbage + aaa + c + ending_garbage

    anusa_ed_listener = "http://anusa.com.au.cybercrime-observatory.tech/anusa.py?x=" \
                        + initial_garbage + aaa + c + "01" + ending_garbage

    anusa_afl_listener = "http://anusa.com.au.cybercrime-observatory.tech/anusa.py?x=" \
                         + initial_garbage + aaa + c + "02" + ending_garbage

    currTime = datetime.datetime.now().strftime("%b %d, %Y, %I:%m%p")

    # substitute in the variables into the HTML component
    email_template['html_component'] \
        = email_template['html_component'].replace("<FIRSTNAME>", participant.first_name)
    email_template['html_component'] \
        = email_template['html_component'].replace("<FULLNAME>", participant.full_name)
    email_template['html_component'] \
        = email_template['html_component'].replace("<UID>", participant.uid)
    email_template['html_component'] \
        = email_template['html_component'].replace("<LANDING_LISTENER>", landing_listener)
    email_template['html_component'] \
        = email_template['html_component'].replace("<ISIS_LISTENER>", isis_listener)
    email_template['html_component'] \
        = email_template['html_component'].replace("<CLEARFIX_LISTENER>", clearfix_listener)
    email_template['html_component'] \
        = email_template['html_component'].replace("<ANUSA_ED_LISTENER>", anusa_ed_listener)
    email_template['html_component'] \
        = email_template['html_component'].replace("<ANUSA_AFL_LISTENER>", anusa_afl_listener)
    email_template['html_component'] \
        = email_template['html_component'].replace("<CURRENT_TIME>", currTime)

    # set up the connection
    TCP_IP = '130.56.66.51'
    TCP_PORT = 25
    buffer_size = 1024

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((TCP_IP, TCP_PORT))

    send_and_receive("", 220)
    send_and_receive("HELO anu.edu.au", 250)
    send_and_receive("MAIL FROM:" + email_template['from'], 250)
    send_and_receive("RCPT TO:" + email_template['to'], 250)
    send_and_receive("DATA", 354)

    send_email_body(email_template)

    send_and_receive(".", 250)
    send_and_receive("QUIT", 221)

    connection.close()

