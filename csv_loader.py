##this is the file for loading the csv data into a sql database.

import sqlite3
import csv


con = sqlite3.connect('private_schools.db', autocommit = True)
cur = con.cursor()
#remove table during subsequent runs
cur.execute("DROP TABLE IF EXISTS superintendents;")
cur.execute("DROP TABLE IF EXISTS admissions;")
cur.execute("DROP TABLE IF EXISTS finances;")
cur.execute("DROP TABLE IF EXISTS demographics;")

#create superintendents table
create_table_super = '''CREATE TABLE superintendents('super_id', 'first_name', 'last_name', 'city')'''
cur.execute(create_table_super)
#put table into database
super_file = open('CSVs/superintendents.csv')
super_contents = csv.reader(super_file)
header = next(super_contents)  ## throw away headers
insert_records_super = "INSERT INTO superintendents('super_id', 'first_name', 'last_name', 'city') VALUES(?, ?, ?, ?)"
cur.executemany(insert_records_super, super_contents)

#create admissions table
create_table_admissions = '''CREATE TABLE admissions('super_id', 'school_id', 'school_name', 'num_applicants', 'pct_accepted', 'incoming_class_size', 'avg_gpa', 'avg_SAT', 'pct_STEM')'''
cur.execute(create_table_admissions)
#put table into database
admissions_file = open('CSVs/admissions_updated.csv')
admissions_contents = csv.reader(admissions_file)
header = next(admissions_contents)  ## throw away headers
insert_records_admissions = "INSERT INTO admissions('super_id', 'school_id', 'school_name', 'num_applicants', 'pct_accepted', 'incoming_class_size', 'avg_gpa', 'avg_SAT', 'pct_STEM') VALUES(?,?,?,?,?,?,?,?,?)"
cur.executemany(insert_records_admissions, admissions_contents)


#create finances table
create_table_finance = '''CREATE TABLE finances('super_id', 'school_id', 'endowment', 'annual_expenses', 'debt', 'avg_faculty_salary')'''
cur.execute(create_table_finance)
#put table into database
finance_file = open('CSVs/finances.csv')
finance_contents = csv.reader(finance_file)
header = next(finance_contents)  ## throw away headers
insert_records_finance = "INSERT INTO finances('super_id', 'school_id', 'endowment', 'annual_expenses', 'debt', 'avg_faculty_salary') VALUES(?,?,?,?,?,?)"
cur.executemany(insert_records_finance, finance_contents)


#create demographics table
create_table_demographic = '''CREATE TABLE Demographics ('super_id', 'school_id', 'num_undergrad', 'num_grad', 'pct_low_income', 'pct_international', 'pct_female', 'pct_male')'''
cur.execute(create_table_demographic)
#put table into database
demographic_file = open('CSVs/demographics.csv')
demographic_contents = csv.reader(demographic_file)
header = next(demographic_contents)  ## throw away headers
insert_records_demographic = "INSERT INTO Demographics ('super_id', 'school_id', 'num_undergrad', 'num_grad', 'pct_low_income', 'pct_international', 'pct_female', 'pct_male') VALUES(?,?,?,?,?,?,?,?)"
cur.executemany(insert_records_demographic, demographic_contents)
