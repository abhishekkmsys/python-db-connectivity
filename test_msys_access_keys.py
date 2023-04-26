import unittest
import json 
import pyodbc
import config
import logging 

class TestMsysAccessKeys(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # set up the logging configuration
        logging.basicConfig(filename='test_accesskeys.log', level=logging.INFO, filemode='w', format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


    def setUp(self):
        self.server = config.server
        self.database = config.database
        self.username = config.username
        self.password = config.password

        try:
            # set up connection and connect to server
            self.connection = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}}; SERVER={self.server}; DATABASE={self.database};UID={self.username};PWD={self.password}")
            self.cursor = self.connection.cursor()


            # execute SQL query to retrieve data from Msys_Accounts table
            self.cursor.execute('SELECT * FROM Msys_Access_Keys')
            self.rows = self.cursor.fetchall()

            # create cursor object
            self.cursor = self.connection.cursor()

        except pyodbc.Error as err:
            logging.error(f"Database Connectivity Failed. {err}") 
            self.skipTest(f"Failed to connect to database. Error message: {err}")

        
    def tearDown(self):
        # close cursor and connection
        self.cursor.close()
        self.connection.close()

    def test_access_secret_acc_id(self):
        logging.info("Test Method : test_access_secret_acc_id checks for whether unique generated between Access id, Account id and secret id, Account id") 
        try: 
            self.db_id_list = [(row[0], row[1], row[5]) for row in self.rows]
            # for  i in self.db_id_list:
            #     print(i)
            for i in self.db_id_list:
                with self.subTest(i = i):
                    access_id = (i[0])[6:]
                    secret_id = (i[1])[6:]
                    acc_id = (i[2][3:])
                    # self.assertEqual(access_id, secret_id)
                    self.assertEqual(access_id, acc_id)
                    self.assertEqual(secret_id, acc_id)
        except AssertionError as err:
            logging.error(f"Assertion Error : {err}")
            raise err 


    def test_creationTimestamp(self):
        logging.info("Test Method : test_creationTimestamp Checks for generated Timestamp is not null")
        try:
            self.creationTimestamp = [row[2] for row in self.rows]
            for element in self.creationTimestamp:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as err:
            logging.error(f"Assertion Error : {err}")
            raise err 
 

    def test_lastUsedTimestamp(self):
        logging.info("Test Method : test_lastUsedTimeStamp Checks for generated last used Timestamp is not null")
        try:
            self.lastUsedTimestamp = [row[3] for row in self.rows]
            for element in self.lastUsedTimestamp:
                with self.subTest(element = element):
                    self.assertIsNotNone(element)
        except AssertionError as err:
            logging.error(f"Assertion Error : {err}")
            raise err 

    def test_status(self):
        logging.info("Test Method : test_status checks whether status of access Key is ACTIVE or not..")
        try:
            self.status = [row[4] for row in self.rows]
            for element in self.status:
                with self.subTest(element = element):
                    self.assertEqual(element, "ACTIVE")
        except AssertionError as err:
            logging.error(f"Assertion Error : {err}")
            raise err 


    def test_userID(self):
        logging.info("Test Method: test_userID checks whether userID created is NUll or Not") 
        try:
            self.userID = [row[6] for row in self.rows]
            print(self.userID)
            for element in self.userID:
                with self.subTest(element = element):
                    self.assertIsNone(element) 
        except AssertionError as err:
            logging.error(f"Assertion Error : {err}")
            raise err 

        

if __name__ == '__main__':
    unittest.main()
