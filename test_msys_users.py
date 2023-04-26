import unittest
import json 
import pyodbc
import config
import logging

class TestMsysUsers(unittest.TestCase):

    # input_data = ''

    @classmethod
    def setUpClass(cls):
        with open('input_user_data.json') as f:
            cls.input_data = json.load(f)

    # set up the logging configuration
        logging.basicConfig(filename='test_users.log', level=logging.INFO, filemode='w', format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

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
            self.cursor.execute('SELECT * FROM Msys_Users')
            self.rows = self.cursor.fetchall()

            # create cursor object
            self.cursor = self.connection.cursor()

        except pyodbc.Error as err:
            logging.error("Database Connectivity Failed. %s", err) 
            self.skipTest(f"Failed to connect to database. Error message: {err}")

    
    def tearDown(self):
        # close cursor and connection
        self.cursor.close()
        self.connection.close()

    
    def test_userName(self):
        logging.info("Test Method test_userName checks for the existence of user Names in db table and compare with input user data file")
        try: 
            self.input_usernames = set(self.input_data['UserName'])

            self.db_UserNames = set()
            for row in self.rows:
                self.db_UserNames.add(row[1])

            self.assertSetEqual(self.db_UserNames, self.input_usernames)
        
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 

    
    def test_userID(self):
        logging.info("Test method test userID checks for Userid is not Null")
        logging.warning("Test method test_userID to get passed , userId generated is not NUll") 
        try:
            self.user_ID_list = [i[0] for i in self.rows]
            for element in self.user_ID_list:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 

    def test_arn(self):
        logging.info("Test method test_arn checks for arn generated is not Null")
        logging.warning("Test method test_arn to get passed , test_arn generated is not NUll") 
        try:
            self.arn_list = [i[2] for i in self.rows]
            # print(self.arn_list)   
            for element in self.arn_list:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 

    def test_timestamp(self):
        logging.info("Test method test_timestamp checks for timestamp generated is not Null")
        logging.warning("Test method test_arn to get passed , timestamp generated is not NUll") 
        try:
            self.timestamp_list = [i[3] for i in self.rows]
            print(self.timestamp_list)   
            for element in self.timestamp_list:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 

    def test_path(self):
        logging.info("Test method test_path checks for path generated is not Null")
        logging.warning("Test method test_path to get passed , path generated is not NUll") 
        try:
            self.test_path_list = [i[4] for i in self.rows]
            print(self.test_path_list)
            for element in self.test_path_list:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 

    def test_accountId(self):
        logging.info("Test method test_accountID checks for accountID generated is not Null")
        logging.warning("Test method test_accountID to get passed , test_accountID generated is not NUll") 
        try:
            self.test_accountID_list = [i[5] for i in self.rows]
            print(self.test_accountID_list)
            for element in self.test_accountID_list:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 

    
if __name__ == '__main__':
    unittest.main()

    