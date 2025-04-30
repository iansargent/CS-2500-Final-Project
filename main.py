## This is the file for using the database

# Importing necessary packages
import sqlite3
import csv
import math

from csv_loader import admissions_contents

##adding records to superintendent table
con = sqlite3.connect('private_schools.db', isolation_level=None)
cur = con.cursor()
list = []


#table is string, column is string
def mean(table, column):
    count_query = f"select COUNT({column}) from {table}"
    sum_query = f"select sum({column}) from {table}"
    count = cur.execute(count_query).fetchall()[0][0]
    sum = cur.execute(sum_query).fetchall()[0][0]
    avg = sum/count
    return avg


def standard_deviation(table, column):
    mean_value = mean(table, column)
    get_vals_query = f"select {column} from {table}"
    values = cur.execute(get_vals_query).fetchall()
    count_query = f"select COUNT({column}) from {table}"
    count = cur.execute(count_query).fetchall()[0][0]
    running_variance = 0
    for i in values:
        val = i[0]
        deviation = (val - mean_value)**2
        running_variance += deviation
    running_variance = running_variance/count
    standard_deviation_total = math.sqrt(running_variance)
    return  standard_deviation_total


def min(table, column):
    get_vals_query = f"select {column} from {table} order by {column} asc"
    vals = cur.execute(get_vals_query). fetchall()[0][0]
    return vals


def max(table, column):
    get_vals_query = f"select {column} from {table} order by {column} desc"
    vals = cur.execute(get_vals_query). fetchall()[0][0]
    return vals


def median(table, column):
    count_query = f"select COUNT({column}) from {table}"
    count = cur.execute(count_query).fetchall()[0][0]
    get_vals_query = f"select {column} from {table} order by {column} desc"
    vals = cur.execute(get_vals_query). fetchall()
    if count % 2 == 0:
         index = count//2
         index_1 = index
         index_2 = index + 1
         return (vals[index_1][0]+vals[index_2][0])/2

    else:
        index = count/2 + .5
        return vals[index][0]

def where_function():
    print(f"this creates a where statement. What this means is that you can"
          f"pick a column in a table, and then you filter the data based off of that column.\n"
          f"if is a numeric column, then you can choose a number, and filter the data based off of"
          f"where the value in that column is less than, equal, or greater than than the number you picked\n"
          f"if you picked a non-numeric column, then you can choose a value, and filter based off of whether or "
          f"not the data is equal to that value"
          f"after all this, you can then do a statistical summary with this new, filtered dataset")
    print(f"what table do you want: \n"
          f"admissions\n"
          f"demographics\n"
          f"finances\n"
          f"superintendents")
    table  = ""
    while table not in ["admissions", "demographics", "finances", "superintendents"]:
        table = input("choice: ")
    column = input("what column are you comparing to: ")
    sign_numeric = input("less than (a), equals (b), or greater than (c): ")
    sign_non_numeric = input("equals (a), not equals (b): ")
    statement = f" "
    return "hi"

def print_columns(table):
    columns_all = (cur.execute(f"pragma table_info({table})").fetchall())
    for i in columns_all:
        print(i[1])



def print_sample_data(table):
    sample_data_query = f"select * from {table}"
    sample_data = cur.execute(sample_data_query).fetchall()
    sample_data_list = []
    for i in sample_data:
        sample_data_list.append(i[0])
    return sample_data_list








print(min("admissions", "num_applicants"))
print(median("admissions", "num_applicants"))
print(mean("admissions", "num_applicants"))
print_columns("finances")



# Data Visualization Function

def data_visualization():
    
    data_viz_flag = True
    
    while data_viz_flag:

        table = input("Choose an category\na) Demographics\nb) Admissions\nc) Finances\n==> ")

        if table == "a":
            print("Printing available demographic variables")
            print_columns("demographics")
        
        elif table == "b":
            print("Printing available admission variables")
            print_columns("admissions")
        
        elif table == "c":
            print("Printing available financial variables")
            print_columns("finances")
        
        else:
            print("That is not a valid table option. Try Again.")
    