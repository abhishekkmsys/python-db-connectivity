import unittest
import json 
import pyodbc
import config
import logging 
from helper_functions import load_json, setup_logging
import db_connection 


class TestMSysObjects(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.input_data = load_json('input_data/input_object_data.json')
        setup_logging('logs/test_objects.log')

    def setUp(self):

        try:
            # create connection
            self.connection = db_connection.create_connection()

            # create cursor object
            self.bucket_cursor = self.connection.cursor()
            self.object_cursor = self.connection.cursor()

            self.bucket_cursor.execute("SELECT * from Msys_buckets")
            self.bucket_rows = self.bucket_cursor.fetchall() 

            self.object_cursor.execute("SELECT * from Msys_Objects")
            self.object_rows = self.object_cursor.fetchall() 

        except pyodbc.Error as err:
            logging.error("Database Connectivity Failed. %s", err) 
            self.skipTest(f"Failed to connect to database. Error message: {err}")

        except Exception as err:
            logging.error(f"An error occurred while connecting to the database. {err}")
            self.skipTest(f"Failed to connect to database. Error message: {err}")

    def test_bucket_name_from_input_file(self):
        try:
            logging.info("Logging for test_bucket_name_from_input_file")
            logging.info("To check for the existence of Bucket Names from Input JSON Data File") 
            Input_BucketNames = [i["BucketName"] for i in self.input_data] 
            Table_BucketNames = [i[1] for i in self.bucket_rows] 
            for element in Input_BucketNames:
                with self.subTest(element = element):
                    # self.assertIn(element, Table_BucketNames, "Bucket Name {element} Not found in Table") 
                    # logging.info(f"Bucket name '{element}' found in table.")
                    if element not in Table_BucketNames:
                        logging.error(f"Bucket name '{element}' not found in table.")
                    self.assertIn(element, Table_BucketNames) 
                    logging.info(f"Bucket name '{element}' found in table.")
        except AssertionError as e:
            logging.error(f"Assertion error: {e}")
            raise e 
        
    def test_object_file(self):
        try:
            logging.info("Logging for test_object_file")
            logging.info("Checking for Object File Names from Input Json Data file.")
            Table_ObjectNames = [i[1] for i in self.object_rows]
            logging.info(f"{Table_ObjectNames}")
            InputData_ObjectNames = [i["ObjectName"] for i in self.input_data]
            Table_ObjectNames_set = set(Table_ObjectNames)
            InputData_ObjectNames = set(InputData_ObjectNames)
            self.assertSetEqual(Table_ObjectNames_set, InputData_ObjectNames)
        except AssertionError as e:
            logging.error(f"Assertion error: {e}")
            raise e
        

    def test_objectID(self):
        try:
            logging.info("Logging for test_objectID")
            logging.info("Checking ObjectID generated value is not NUll")
            self.user_ObjectID = [i[0] for i in self.object_rows]
            for element in self.user_ObjectID:
                with self.subTest(element = element):
                    self.assertIsNotNone(element)
        except AssertionError as e:
            logging.error(f"Assertion error: {e}")
            raise e 
    

    def test_creationTimeStamp(self):
        try:
            logging.info("Logging for test_creationTimeStamp")
            logging.info("Checking TimeStamp generated value is not NUll")
            self.user_timeID = [i[2] for i in self.object_rows]
            for element in self.user_timeID:
                with self.subTest(element = element):
                    self.assertIsNotNone(element) 
        except AssertionError as e:
            logging.error(f"Assertion error: {e}")
            raise e 
        
    def test_bucketID(self):
        try:
            logging.info("Logging for test_bucketID")
            logging.info("Checking for Comparision of BucketID from Msys_Buckets Table and BucketID from Msys_Objects Table") 
            Bucket_Table_Bucket_ID = [i[0] for i in self.bucket_rows]
            Object_Table_Bucket_ID = [i[-1] for i in self.object_rows]
            for element in Object_Table_Bucket_ID:
                with self.subTest(element = element):
                    if element not in Bucket_Table_Bucket_ID:
                        logging.error(f"Bucketid '{element}' from Objects Table not found in Buckets table.")
                    self.assertIn(element, Bucket_Table_Bucket_ID) 
                    logging.info(f"Bucketid '{element}' from Objects Table found in Buckets table.")
        except AssertionError as e:
            logging.error(f"Assertion error: {e}")
            raise e 

if __name__ == '__main__':
    unittest.main()

