import participant
import emailer
import time
import sys


def SendEmailToPerson(personId, email, db):
    """
    Sends this email to one specific person. Loads up the person from the database...

    :param personId: The person to receive this email.
    :param email: The email object to transmit.
    :param db: The database connection.
    :return:
    """
    query = "SELECT * FROM user WHERE id = " + str(personId)
    results = db.ExecuteSelectQuery(query)
    target = participant.CreateFromSQL(results[0])
    emailer.SendEmail(target, email, 0)
    timestamp = int(time.time())
    db.ExecuteQuery("INSERT INTO activity (what, user_id, batch_id, datetime) VALUES (" +
                    "0, " + str(target._id) + ", 0, " + str(timestamp) + ");")

    print(" sent to " + str(target._id) + "!")
    sys.stdout.flush()


def SendEmailToGroup(group_id, batch_id, email, people, db):
    """
    Sends the given email to all participants in this group.

    :param group_id: The group to send the email to.
    :param batch_id: The ID number of the batch of emails that is going out
    :param email: The email template object.
    :param people: The participants in this experiment, as a list.
    :param db: The open connection to the database.
    :return:
    """
    if batch_id is not 0:
        db.ExecuteQuery("INSERT INTO batch_group (batch_id, group_id) VALUES ("
                        + str(batch_id) + ", " + str(group_id) + ");")

    for person in people:
        if person.group_id is group_id and person.Active():
            emailer.SendEmail(person, email, batch_id)
            timestamp = int(time.time())
            db.ExecuteQuery("INSERT INTO activity (what, user_id, batch_id, datetime) VALUES (" +
                            "0, " + str(person._id) + ", " + str(batch_id) + ", " + str(timestamp) + ");")

            print(" sent to " + str(person._id) + "!")
            sys.stdout.flush()


def SendEmailToAll(groups, batch_id, email, people, db):
    """
    Sends the given email to all participants in the experiment.

    :param groups: The set of all groups to send to. This is a shit workaround.
    :param batch_id: The ID number of the batch of emails that is going out
    :param email: The email template object.
    :param people: The participants in this experiment, as a list.
    :param db: The open connection to the database.
    :return:
    """
    for group_id in groups:
        db.ExecuteQuery("INSERT INTO batch_group (batch_id, group_id) VALUES ("
                        + str(batch_id) + ", " + str(group_id) + ");")

        for person in people:
            if person.group_id is group_id and person.Active():
                emailer.SendEmail(person, email, batch_id)
                timestamp = int(time.time())
                db.ExecuteQuery("INSERT INTO activity (what, user_id, batch_id, datetime) VALUES (" +
                                "0, " + str(person._id) + ", " + str(batch_id) + ", " + str(timestamp) + ");")
