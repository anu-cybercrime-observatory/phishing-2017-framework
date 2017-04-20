import BatchManager
import database
import participant
import Email
import time


database = database.Database()

emails = Email.LoadAll(database)
people = participant.LoadAll(database)

email = emails[0]
timestamp = int(time.time())
batch_id = database.ExecuteInsert("INSERT INTO batch (email_id, datetime) VALUES (" +
                                  str(email.ID()) + ", " + str(timestamp) + ");")
BatchManager.SendEmailToGroup(4, batch_id, email, people, database)

database.Close()
