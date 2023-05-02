import unittest
import json 
import pyodbc
import config
import logging 
from helper_functions import load_json, setup_logging
import db_connection 

class TestMsysBuckets(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.input_data = load_json('input_data/input_bucket_data.json')
        setup_logging('logs/test_buckets.log')

    def setUp(self):

        try:
            # create connection
            self.connection = db_connection.create_connection()

            # create cursor object
            self.access_key_Table_cursor = self.connection.cursor()

            self.access_key_Table_cursor.execute("""
            SELECT access_key.accessKeyId, access_key.secretKey, bucket_key.accountId
            FROM Msys_Access_Keys access_key
            JOIN Msys_Buckets bucket_key
            ON access_key.accountId = bucket_key.accountId
            """)

            self.access_rows = self.access_key_Table_cursor.fetchall()


            self.bucket_table_cursor = self.connection.cursor()
            self.bucket_table_cursor.execute("SELECT * from Msys_Buckets")
            self.bucket_table_rows = self.bucket_table_cursor.fetchall()

        except pyodbc.Error as err:
            logging.error(f"Database Connectivity Failed. {err}") 
            self.skipTest(f"Failed to connect to database. Error message: {err}")

        except Exception as err:
            logging.error(f"An error occurred while connecting to the database. {err}")
            self.skipTest(f"Failed to connect to database. Error message: {err}")


    def test_bucketAccID_accessID_secretkey(self):
        logging.info("Test Method : test_bucketAccID_accessID_secretkey , to map bucket Account Id with Access Key Id and secret Id") 
        try:
            for i in self.access_rows:
                with self.subTest(i = i):
                    access_id = (i[0])[6:]
                    secret_id = (i[1])[6:]
                    Acc_Bucket_id = (i[2][3:])
                    self.assertEqual(Acc_Bucket_id, access_id)
                    self.assertEqual(Acc_Bucket_id, secret_id) 
        except AssertionError as err:
            logging.error(f"AssertionError : {err}") 


    def test_bucketID(self):
        logging.info("Test Method : test_bucketID to check for generated Bucket Id is not null")
        try:
            self.bucketID = [i[0] for i in self.bucket_table_rows]
            for element in self.bucketID:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as err:
            logging.error(f"AssertionError : {err}")
            raise err

    def test_arn(self):
        logging.info("Test Method : test_arn to check for generated arn is not null")
        try:
            self.test_arn = [i[2] for i in self.bucket_table_rows]
            for element in self.test_arn:
                with self.subTest(element=element):
                    self.assertIsNotNone(element) 
        except AssertionError as err:
            logging.error(f"AssertionError : {err}")
            raise err

    def test_creationTimestamp(self):
        logging.info("Test Method : test_creationTimestamp to check for creation Time stamp is not null")
        try:
            self.creationTimestamp = [i[3] for i in self.bucket_table_rows]
            for element in self.creationTimestamp:
                with self.subTest(element=element):
                    self.assertIsNotNone(element)
        except AssertionError as err:
            logging.error(f"AssertionError : {err}")
            raise err
    
    def test_bucketName(self):
        logging.info("Test Method: test_bucketName to compare for bucket Names present in db Table with Input User Data")
        try:
            self.input_usernames = set(self.input_data['bucketName'])
            self.db_bucketNames = set()
            for row in self.bucket_table_rows:
                self.db_bucketNames.add(row[1])
            self.assertSetEqual(self.db_bucketNames, self.input_usernames)
        except AssertionError as err:
            logging.error(f"AssertionError : {err}")
            raise err 
    

if __name__ == '__main__':
    unittest.main()
