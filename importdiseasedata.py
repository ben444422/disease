
import MySQLdb
import sys
import csv



# Open database connection
db = MySQLdb.connect("127.0.0.1","root","root","disease" )

# prepare a cursor object using cursor() method
cursor = db.cursor()



with open('some.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row

        









# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print "Database version : %s " % data


for line in 
