import BatchManager
import database
import participant
import Email
import time


database = database.Database()

emails = Email.LoadAll(database)
people = participant.LoadAll(database)

# hard coded the value of the reminder email, because I suck.
email = None
for candidate in emails:
    if candidate.ID() is 10:
        email = candidate

if email:
    suppress_batch = True

    timestamp = int(time.time())
    if suppress_batch:
        batch_id = 0
    else:
        batch_id = database.ExecuteInsert("INSERT INTO batch (email_id, datetime) VALUES (" +
                                          str(email.ID()) + ", " + str(timestamp) + ");")

    BatchManager.SendEmailToPerson(144, email, database)
    # BatchManager.SendEmailToGroup(4, batch_id, email, people, database)
    # BatchManager.SendEmailToGroup(3, batch_id, email, people, database)
    # BatchManager.SendEmailToGroup(2, batch_id, email, people, database)
    # BatchManager.SendEmailToGroup(1, batch_id, email, people, database)


database.Close()
