import pymysql


class Database:
    """
    DATABASE CONNECTION CONFIGURATION
    """
    __host     = "localhost"
    __user     = "phisher"
    __password = "N1@htL1@ht"
    __database = "phish2017"

    def __init__(self):
        """
        Connect to the database.
        """
        self.db = pymysql.Connect(host=Database.__host,
                                  user=Database.__user,
                                  database=Database.__database,
                                  password=Database.__password)

    def Close(self):
        """
        Terminates the connection to the database!
        :return:
        """
        self.db.close()

    def LoadFromDatabase(self, tableName, anonFunc):
        """
        Loads all the things of a certain type from the database.
        :param database:
        :param tableName:
        :return:
        """
        results = []
        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM " + tableName)
        for row in cursor.fetchall():
            item = anonFunc(row)
            results.append(item)

        return results

    def ExecuteQuery(self, query):
        """
        Executes an INSERT, UPDATE or DELETE command on the database.

        :param database: The database to work on.
        :param query: The query to execute.
        :return:
        """
        cursor = self.db.cursor()
        try:
            cursor.execute(query)
            self.db.commit()
        except Exception as e:
            print(str(e))
            self.db.rollback()

    def ExecuteQueries(self, queryList):
        """
        Executes a list of SQL INSERT, UPDATE or DELETE commands.

        :param database: The database to transact upon.
        :param queryList: The list of queries to execute.
        :return:
        """
        cursor = self.db.cursor()
        try:
            for query in queryList:
                cursor.execute(query)
            self.db.commit()
        except Exception as e:
            print(str(e))
            self.db.rollback()

    def ExecuteInsert(self, query):
        """
        Executes an SQL INSERT command, and gets and returns the primary key
        of the object thus inserted.

        :param query: The command to execute
        :return: The primary key of the newly created record. Returns 0 on error.
        """
        cursor = self.db.cursor()
        returnValue = 0
        try:
            cursor.execute(query)
            self.db.commit()
            returnValue = cursor.lastrowid
        except Exception as e:
            print(str(e))
            self.db.rollback()

        return returnValue


def SQLString(string):
    return "'" + string.replace("'", "\\'") + "'"
