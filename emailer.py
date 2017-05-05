import Email
import socket
import sys
import time


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

    return


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
                                       + email_object.Body()

    email_template['to'] = participant.Email()

    aaa = '0' * (3 - len(str(participant._id))) + str(participant._id)
    b = str(1)
    c = '0' * (2 - len(str(batch_number))) + str(batch_number)

    listener = "http://isis.anu.edu.au.cybercrime-observatory.tech/psp/sscsprod/?cmd="\
               + aaa + b + c + "c30bb76b355a39dcd9e73bfb934b380d&aa=0010-100100100-10100-1001-010F"

    # substitute in the variables into the HTML component
    email_template['html_component'] \
        = email_template['html_component'].replace("<FIRSTNAME>", participant.first_name)
    email_template['html_component'] \
        = email_template['html_component'].replace("<FULLNAME>", participant.full_name)
    email_template['html_component'] \
        = email_template['html_component'].replace("<UID>", participant.uid)
    email_template['html_component'] \
        = email_template['html_component'].replace("<LISTENER>", listener)

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

