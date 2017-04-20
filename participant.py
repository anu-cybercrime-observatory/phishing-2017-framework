"""

    A little construct that holds all the data relating to a participant in this experiment.

"""


class Participant:
    def __init__(self):
        self._id = 0
        self.uid = ""
        self.group_id = 0
        self.gender = 0
        self.first_name = ""
        self.full_name = ""
        self.enabled = 0

    def Email(self):
        return self.uid + "@anu.edu.au"

    def Active(self):
        return self.enabled is 1

    def SetName(self, first, last):
        first = first.replace("'", "\\'")
        last = last.replace("'", "\\'")

        self.first_name = first
        self.full_name = first + " " + last

    def SetUID(self, uid):
        self.uid = uid

    def SetId(self, id):
        self._id = id

    def SetGroup(self, group):
        self.group_id = group

    def __repr__(self):
        return self.uid + "," + self.first_name + "," + self.full_name + ", group " + str(self.group_id)

    def InsertSQL(self):
        fields = [
            "firstname",
            "fullname",
            "groupId",
            "UID"
        ]

        values = [
            "'" + self.first_name + "'",
            "'" + self.full_name + "'",
            str(self.group_id),
            "'" + self.uid + "'"
        ]
        return "INSERT INTO user (" + ", ".join(fields) + ") VALUES (" + ", ".join(values) + ");"

    def LoadFromSQL(self, sqlData):
        (self._id, self.first_name,
         self.full_name, self.gender,
         self.group_id, self.uid, self.enabled) = sqlData


def Create(key, firstName, surName, UID):
    result = Participant()
    result.SetId(key)
    result.SetName(firstName, surName)
    result.SetUID(UID)

    return result


def CreateFromSQL(sqlData):
    result = Participant()
    result.LoadFromSQL(sqlData)
    return result


def LoadAll(database):
    """
    Loads all the participants data from the database and returns it as a list.

    :param database: A database object
    :return:
    """
    people = database.LoadFromDatabase("user", CreateFromSQL)
    return people
