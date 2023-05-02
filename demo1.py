import unittest 
import pyodbc
import json 
import db_connection

with open("input_user_data.json") as f:
    input_data = json.load(f)

# print(input_data) 
# for i in input_data:
#     print(i) 

connection = db_connection.create_connection()

cursor = connection.cursor()

cursor.execute("""
SELECT Msys_Accounts.accountName, Msys_Users.userName, Msys_Users.accountId FROM Msys_Accounts INNER JOIN Msys_Users ON Msys_Accounts.accountId = Msys_Users.accountId
""")

rows = cursor.fetchall()
# print(rows) 
table_data = {}
for accountName, userName, accountId in rows:
    table_data.setdefault(accountName, []).append(userName) 
print(table_data)
print()

# print(input_data)

input_data = {item['AccountName']: item['UserName'] for item in input_data}

print(input_data) 

