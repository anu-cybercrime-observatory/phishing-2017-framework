import participant
import random
import math

"""
A file to parse the data in the participant CSV files and insert it into the databases.
Only needs to be called once to rebuild the user table of the database.
"""

def GetPeople():
    with open("Participant Keys.csv") as inputFile:
        lines = inputFile.readlines()

    people = dict()
    for line in lines:
        bits = line.strip().split(",")

        id = int(bits[0])
        namebits = bits[1].split(" ")
        firstName = namebits[0]
        lastName = namebits[-1]
        uid = bits[2]

        person = participant.Create(id, firstName, lastName, uid)
        people[id] = person

    with open("Participants.csv") as inputFile:
        lines = inputFile.readlines()

    unAllocatedGroup = []
    for line in lines:
        bits = line.strip().split(",")
        key = int(bits[0])
        isCrim = bits[1]

        if isCrim is not '':
            people[key].SetGroup(1)
        else:
            unAllocatedGroup.append(people[key])

    # compute the number of hunters to add to this experiment
    generator = random.Random()
    numToAllocate = math.floor(len(unAllocatedGroup) / 2)
    for person in unAllocatedGroup:
        if generator.randint(1, 2) is 2 and numToAllocate > 0:
            person.SetGroup(3)
            numToAllocate -= 1
        else:
            person.SetGroup(2)

    return people
