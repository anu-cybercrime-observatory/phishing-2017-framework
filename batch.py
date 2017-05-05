import datetime


class Batch:
    """
    This class represents one batch of emails that has been sent out to one or more groups.
    """
    table_name = "batch"
    __fields = [
        "id",
        "email_id",
        "datetime"
    ]

    def __init__(self):
        self.id = 0
        self.email_id = 0
        self.timestamp = 0
        self.groups = []
        self.activityLog = dict()


    def __repr__(self):
        values = [
            self._id,
            self.email_id,
            datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        ]
        combined = [f + " = " + str(v) for f, v in zip(Batch.__fields, values)]
        return "\n".join(combined)


    """
    Getter functions
    """
    def ID(self):
        return self._id

    def Groups(self):
        return self.groups

    def Activities(self):
        res = dict()
        for key in self.activityLog:
            res[key] = len(self.activityLog[key].keys())

        return res

    """
    Setter functions
    """
    def SetId(self, id):
        self._id = id()

    def SetEmailId(self, email_id):
        self.email_id = email_id

    def SetTimeStamp(self, timestamp):
        self.timestamp = timestamp

    def AddGroup(self, group_id):
        self.groups.append(group_id)

    def AddActivity(self, activity_type, user_id):
        if activity_type not in self.activityLog:
            self.activityLog[activity_type] = dict()

        self.activityLog[activity_type][user_id] = True


    def InsertSQL(self):
        """
        Generate the SQL needed to insert this object into the database.

        :return:
        """
        fields = [f for f in Batch.__fields if f is not "id"]
        values = [
            str(self.email_id),
            str(self.timestamp),
        ]

        return "INSERT INTO " + Batch.table_name \
               + " (" + ", ".join(fields) \
               + ") VALUES (" \
               + ", ".join(values) \
               + ");"

    def LoadFromSQL(self, sqlData):
        (self._id, self.email_id, self.timestamp) = sqlData


def Create(key, email_id, timestamp):
    result = Batch()
    result.SetId(key)
    result.SetEmailId(email_id)
    result.SetTimeStamp(timestamp)

    return result


def CreateFromSQL(sqlData):
    result = Batch()
    result.LoadFromSQL(sqlData)
    return result


def LoadAll(db):
    """
    Loads all the batch data from the database and returns it as a dictionary indexed by ID.

    :param db: A database object
    :return:
    """
    batches = db.LoadFromDatabase(Batch.table_name, CreateFromSQL)
    batch_index = dict()
    for batch in batches:
        batch_index[batch.ID()] = batch
    return batch_index
