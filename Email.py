from database import SQLString
import os


"""

Note: Refactoring this class so that the **template filename** matches the primary key ID in the database.
The field 'filename' is now used as the 'template name' text representation only..
"""
class Email:
    table_name = "email"
    __template_path = "/var/www/html/phish2017/Emails/"
    __fields = [
        "id",
        "subject",
        "filename",
        "originating_name",
        "originating_email"
    ]

    def __init__(self):
        """
        Initialises the fields that this object will hold.
        """
        self._id = 0
        self._template_file = ""
        self._subject = ""
        self._originating_name = ""
        self._originating_email = ""

    def __repr__(self):
        fields = Email.__fields + ["From", "From (appearance)", "Body"]
        values = [
            self._id,
            self._subject,
            self._template_file,
            self._originating_name,
            self._originating_email,
            self.From(),
            self.FromAppearance(),
            self.Body()
        ]
        combined = [f + " = " + str(v) for f, v in zip(fields, values)]
        return "\n".join(combined)


    """
    Getter functions - note that the Get view differs from the Set view.
    """
    def ID(self):
        return self._id

    def From(self):
        return self.FromAppearance().replace(" ", "")

    def FromAppearance(self):
        return self._originating_name + " <" + self._originating_email + ">"

    def Subject(self):
        return self._subject

    def OriginatingName(self):
        return self._originating_name

    def OriginatingEmail(self):
        return self._originating_email


    def _templateFilename(self):
        return Email.__template_path + str(self._id) + ".txt"

    """
    Refactored this - "template file" now refers to the template name, not a filename.
    """
    def Name(self):
        return self._template_file

    def Body(self):
        if not os.path.exists(self._templateFilename()):
            # with open(self._templateFilename(), "w") as outputFile:
            #     outputFile.write("\n")
            print("file not found")

        with open(self._templateFilename()) as inputFile:
            lines = inputFile.readlines()
        return "".join(lines)


    """
    Setter functions.
    """
    def SetID(self, ID):
        self._id = ID

    def SetOriginatingName(self, name):
        self._originating_name = name

    def SetOriginatingEmail(self, email):
        self._originating_email = email

    def SetSubject(self, subject):
        self._subject = subject

    def SetName(self, template):
        self._template_file = template

    def SetBody(self, body):
        with open(self._templateFilename(), "w") as outputFile:
            outputFile.write(body)


    """
    Database functions
    """
    def InsertSQL(self):
        """
        :return: The SQL query to create this object in the database. Note that the value of _id is disregarded!
        """
        fields = [f for f in Email.__fields if f is not "id"]
        values = [
            SQLString(self._subject),
            SQLString(self._template_file),
            SQLString(self._originating_name),
            SQLString(self._originating_email)
        ]

        return "INSERT INTO " + Email.table_name \
               + " (" + ", ".join(fields) \
               + ") VALUES (" \
               + ", ".join(values) \
               + ");"

    def UpdateSQL(self):
        """
        :return: The SQL query to update this object in the database - it matches on ID
        """
        fields = [f for f in Email.__fields if f is not "id"]
        values = [
            SQLString(self._subject),
            SQLString(self._template_file),
            SQLString(self._originating_name),
            SQLString(self._originating_email)
        ]

        updatedFields = [f + "=" + v for f, v in zip(fields, values)]

        return "UPDATE " + Email.table_name \
               + " SET " \
               + ", ".join(updatedFields) \
               + " WHERE id=" + str(self._id) + ";"

    def LoadFromSQL(self, sqlData):
        (self._id, self._subject, self._template_file,
         self._originating_name, self._originating_email) = sqlData


def CreateFromSQL(sqlData):
    result = Email()
    result.LoadFromSQL(sqlData)
    return result


def LoadAll(database):
    """
    Loads all the participants data from the database and returns it as a list.

    :param database: A database object
    :return:
    """
    emails = database.LoadFromDatabase(Email.table_name, CreateFromSQL)
    return emails
