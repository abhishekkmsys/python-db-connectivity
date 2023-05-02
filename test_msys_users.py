import unittest
import pyodbc
import config
import logging
from helper_functions import load_json, setup_logging
import db_connection 

class TestMsysUsers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.input_data = load_json('input_data/input_user_data.json')
        setup_logging('logs/test_users.log')

    def setUp(self):
        try:
            # create connection
            self.connection = db_connection.create_connection()

            # create cursor object
            self.cursor = self.connection.cursor()

            # execute SQL query to retrieve data from Msys_Users table
            self.cursor.execute('SELECT * FROM Msys_Users')
            self.users_table_rows = self.cursor.fetchall()

            # execute SQL query to retrieve data from Msys_Accounts table
            self.cursor.execute('SELECT * FROM Msys_Accounts')
            self.accounts_table_rows = self.cursor.fetchall()

        except pyodbc.Error as err:
            logging.error(f"Database Connectivity Failed. {err}") 
            self.skipTest(f"Failed to connect to database. Error message: {err}")

        except Exception as err:
            logging.error(f"An error occurred while connecting to the database. {err}")
            self.skipTest(f"Failed to connect to database. Error message: {err}")

    
    def tearDown(self):
        # close cursor and connection
        self.cursor.close()
        self.connection.close()

    def test_check_accountID(self):
        logging.info("Test method test_check_accountID checks for AccountID from users table is present in Msys_Accounts Table")
        logging.warning("Test method test_check_accountID to get passed , AccountId from Users table should be present in Accounts Table.")
        try: 
            account_table_accountIDs = [i[0] for i in self.accounts_table_rows]
            users_table_accountIds = [i[-1] for i in self.users_table_rows]
            # Check if every accountId in user table is present in account table
            for accountId in users_table_accountIds:
                with self.subTest(accountId = accountId):
                    if accountId not in users_table_accountIds:
                        logging.error(f"{accountId} not found in {users_table_accountIds}")
                    self.assertIn(accountId, account_table_accountIDs, msg=f"{accountId} not found in accountIds!")
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e    
        except Exception as e:
            logging.error(f"Error : {e}")
            raise e    

    def test_check_accountName(self):
        logging.info("Test method check_accountName to check for existence of account Name in AccountName from input data")
        try:
            AccountTable_accountNames = [i[1] for i in self.accounts_table_rows] 
            InputData_accountNames = [i["AccountName"] for i in self.input_data]
            # Check if every accountName in input data file is present in account table
            for accountName in InputData_accountNames:
                with self.subTest(accountName = accountName):
                    if accountName not in AccountTable_accountNames:
                        logging.error(f"{accountName} not found in {AccountTable_accountNames}")
                    self.assertIn(accountName, AccountTable_accountNames, msg=f"{accountName} not found in accountIds!")
        except AssertionError as e:
            logging.error(f"Assertion error: {e}")
            raise e 
        except Exception as e:
            logging.error(f"Error : {e}")
            raise e 
        
    def test_userName(self):
        try:
            self.cursor.execute("""
            SELECT Msys_Accounts.accountName, Msys_Users.userName, Msys_Users.accountId FROM Msys_Accounts INNER JOIN Msys_Users ON Msys_Accounts.accountId = Msys_Users.accountId
            """)
            rows = self.cursor.fetchall() 
            table_data = {}
            for accountName, userName, accountId in rows:
                table_data.setdefault(accountName, []).append(userName) 

            input_data = {item['AccountName']: item['UserName'] for item in self.input_data}

            for key in input_data:
                with self.subTest(key=key):
                    try:
                        if key not in table_data.keys():
                            logging.error(f"Account {key} not found in Account Table Data")
                        self.assertEqual(sorted(input_data[key]), sorted(table_data[key]), "UserNames doesn't match")
                    except AssertionError as e:
                        logging.error(f"Assertion Error for account {key}: {e}")
                        raise e          
        except Exception as e:
            logging.error(f"Error : {e}")
            raise e 

    def test_userID(self):
        logging.info("Test method test userID checks for Userid is not Null")
        logging.warning("Test method test_userID to get passed , userId generated is not NUll") 
        try:
            self.user_ID_list = [i[0] for i in self.users_table_rows]
            for element in self.user_ID_list:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 
        except Exception as e:
            logging.error(f"Error : {e}")
            raise e 

    def test_arn(self):
        logging.info("Test method test_arn checks for arn generated is not Null")
        logging.warning("Test method test_arn to get passed , test_arn generated is not NUll") 
        try:
            self.arn_list = [i[2] for i in self.users_table_rows]
            for element in self.arn_list:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 
        except Exception as e:
            logging.error(f"Error : {e}")
            raise e

    def test_timestamp(self):
        logging.info("Test method test_timestamp checks for timestamp generated is not Null")
        logging.warning("Test method test_arn to get passed , timestamp generated is not NUll") 
        try:
            self.timestamp_list = [i[3] for i in self.users_table_rows]   
            for element in self.timestamp_list:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 
        except Exception as e:
            logging.error(f"Error : {e}")
            raise e

    def test_path(self):
        logging.info("Test method test_path checks for path generated is not Null")
        logging.warning("Test method test_path to get passed , path generated is not NUll") 
        try:
            self.test_path_list = [i[4] for i in self.users_table_rows]
            for element in self.test_path_list:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 
        except Exception as e:
            logging.error(f"Error : {e}")
            raise e

    def test_accountId_isNotNUll(self):
        logging.info("Test method test_accountID checks for accountID generated is not Null")
        logging.warning("Test method test_accountID to get passed , test_accountID generated is not NUll") 
        try:
            self.test_accountID_list = [i[5] for i in self.users_table_rows]
            for element in self.test_accountID_list:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion Error : {e}") 
            raise e 
        except Exception as e:
            logging.error(f"Error : {e}")
            raise e

if __name__ == '__main__':
    unittest.main()
