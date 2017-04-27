import emailer
import time


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
    db.ExecuteQuery("INSERT INTO batch_group (batch_id, group_id) VALUES ("
                    + str(batch_id) + ", " + str(group_id) + ");")

    for person in people:
        if person.group_id is group_id and person.Active():
            emailer.SendEmail(person, email, batch_id)
            timestamp = int(time.time())
            db.ExecuteQuery("INSERT INTO activity (what, user_id, batch_id, datetime) VALUES (" +
                            "0, " + str(person._id) + ", " + str(batch_id) + ", " + str(timestamp) + ");")


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
