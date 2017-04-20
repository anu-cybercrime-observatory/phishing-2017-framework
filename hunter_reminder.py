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
    if candidate.ID() is 2:
        email = candidate

if email:
    timestamp = int(time.time())
    batch_id = database.ExecuteInsert("INSERT INTO batch (email_id, datetime) VALUES (" +
                                      str(email.ID()) + ", " + str(timestamp) + ");")
    BatchManager.SendEmailToGroup(4, batch_id, email, people, database)
    BatchManager.SendEmailToGroup(3, batch_id, email, people, database)

database.Close()
