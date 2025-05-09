## This is the file for loading the csv data into a sql database.

# Importing necessary packages
import sqlite3
import csv

# Connect to the database and create the cursor
con = sqlite3.connect('private_schools.db', isolation_level = None)
cur = con.cursor()

# Remove table during subsequent runs
cur.execute("DROP TABLE IF EXISTS superintendents;")
cur.execute("DROP TABLE IF EXISTS admissions;")
cur.execute("DROP TABLE IF EXISTS finances;")
cur.execute("DROP TABLE IF EXISTS demographics;")

# Create superintendents table
create_table_super = '''CREATE TABLE superintendents('first_name', 'last_name','super_id', 'city')'''
cur.execute(create_table_super)

# Put table into database
super_file = open('CSVs/superintendents.csv')
super_contents = csv.reader(super_file)
header = next(super_contents)  ## throw away headers
insert_records_super = "INSERT INTO superintendents('first_name', 'last_name', 'super_id', 'city') VALUES(?, ?, ?, ?)"
cur.executemany(insert_records_super, super_contents)



# Create admissions table
create_table_admissions = '''CREATE TABLE admissions('super_id', 'school_id', 'school_name', 'num_applicants' INTEGER, 'pct_accepted' REAL, 'incoming_class_size' INTEGER, 'avg_gpa' REAL, 'avg_SAT' REAL, 'pct_STEM' REAL)'''
cur.execute(create_table_admissions)

# Put table into database
admissions_file = open('CSVs/admissions.csv')
admissions_contents = csv.reader(admissions_file)
header = next(admissions_contents)  ## throw away headers
insert_records_admissions = "INSERT INTO admissions('super_id', 'school_id', 'school_name', 'num_applicants', 'pct_accepted', 'incoming_class_size', 'avg_gpa', 'avg_SAT', 'pct_STEM') VALUES(?,?,?,?,?,?,?,?,?)"
cur.executemany(insert_records_admissions, admissions_contents)



# Create finances table
create_table_finance = '''CREATE TABLE finances('super_id', 'school_id', 'endowment' REAL, 'annual_expenses' REAL, 'debt' REAL, 'avg_faculty_salary' REAL)'''
cur.execute(create_table_finance)

# Put table into database
finance_file = open('CSVs/finances.csv')
finance_contents = csv.reader(finance_file)
header = next(finance_contents)  ## throw away headers
insert_records_finance = "INSERT INTO finances('super_id', 'school_id', 'endowment', 'annual_expenses', 'debt', 'avg_faculty_salary') VALUES(?,?,?,?,?,?)"
cur.executemany(insert_records_finance, finance_contents)



# Create demographics table
create_table_demographic = '''CREATE TABLE demographics ('super_id', 'school_id', 'num_undergrad' INTEGER, 'num_grad' INTEGER, 'pct_low_income' REAL, 'pct_international' REAL, 'pct_female' REAL, 'pct_male' REAL)'''
cur.execute(create_table_demographic)

# Put table into database
demographic_file = open('CSVs/demographics.csv')
demographic_contents = csv.reader(demographic_file)
header = next(demographic_contents)  ## throw away headers
insert_records_demographic = "INSERT INTO Demographics ('super_id', 'school_id', 'num_undergrad', 'num_grad', 'pct_low_income', 'pct_international', 'pct_female', 'pct_male') VALUES(?,?,?,?,?,?,?,?)"
cur.executemany(insert_records_demographic, demographic_contents)
