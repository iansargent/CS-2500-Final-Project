## This is the file for using the database

# Importing necessary packages
import sqlite3
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
        if table not in ["admissions", "demographics", "finances", "superintendents"]:
            print("choose a table")
    print("your column choices")
    for i in get_columns(table):
        print(i)
    column = input("what column are you comparing to: ")
    type = ""
    columns_all = (cur.execute(f"pragma table_info({table})").fetchall())
    for i in columns_all:
        if i[1] == column:
            if i[2] != "":
                type = "numeric"
            else:
                type = "not numeric"
    sign = "="
    if type == "numeric":
        sign_numeric = input("less than (a), equals (b), or greater than (c): ")
        if sign_numeric == "a":
            sign = "<"
        elif sign_numeric == "b":
            sign = "="
        else:
            sign = ">"
    else:
        sign_non_numeric = input("equals (a), not equals (b): ")
        if sign_non_numeric == "a":
            sign = "="
        if sign_non_numeric == "b":
            sign = "!="
    user_value = input("finally, choose your value to compare things to: ")
    statement = f"{table} WHERE {column} {sign} '{user_value}'"
    return statement

def get_columns(table):
    columns_all = (cur.execute(f"pragma table_info({table})").fetchall())
    columns_list = []
    for i in columns_all:
        columns_list.append(i[1])
    return columns_list


def print_sample_data(table):
    sample_data_query = f"select * from {table}"
    sample_data = cur.execute(sample_data_query).fetchall()
    sample_data_list = []
    for i in sample_data:
        sample_data_list.append(i[0])
    return sample_data_list

def get_column_type(table, column):
    type = ""
    columns_all = (cur.execute(f"pragma table_info({table})").fetchall())
    for i in columns_all:
        if i[1] == column:
            if i[2] != "":
                type = "numeric"
            else:
                type = "not numeric"
    return type

# Data Visualization Function

def data_visualization():
    
    data_viz_flag = True
    while data_viz_flag:

        table = input("Choose a category to investigate\na) Demographics\nb) Admissions\nc) Finances\n==> ")

        if table == 'a':
            table_name = "demographics"
        elif table == 'b':
            table_name = "admissions"
        elif table == 'c':
            table_name = "finances"
        else:
            print("Invalid choice. Please choose a valid category.")


        if table == "a":
            print(f"\nPrinting available {table_name} variables")
            dem_columns = get_columns("demographics")
            for column in dem_columns:
                print(column)
            column_of_interest = input("Which column would you like to investigate? ")
            column_type = get_column_type("demographics", column_of_interest)

            if column_type == "numeric":
                # Create a histogram
                print(f"Creating histogram for {column_of_interest} in demographics")
                histogram_query = f"SELECT {column_of_interest} FROM demographics"
                histogram_data = cur.execute(histogram_query).fetchall()
                histogram_data = pd.DataFrame(histogram_data, columns=[column_of_interest])
                plt.figure(figsize=(10, 6))
                sns.histplot(histogram_data[column_of_interest], bins=30, kde=True)
                plt.title(f"Histogram of {column_of_interest} in Demographics")
                plt.xlabel(column_of_interest)
                plt.ylabel("Frequency")
                plt.show()
                # Create a boxplot
                print(f"Creating boxplot for {column_of_interest} in demographics")
                boxplot_query = f"SELECT {column_of_interest} FROM demographics"
                boxplot_data = cur.execute(boxplot_query).fetchall()
                boxplot_data = pd.DataFrame(boxplot_data, columns=[column_of_interest])
                plt.figure(figsize=(10, 6))
                sns.boxplot(x=boxplot_data[column_of_interest])
                plt.title(f"Boxplot of {column_of_interest} in Demographics")
                plt.xlabel(column_of_interest)
                plt.show()
            
            elif column_type == "not numeric":
                # Create a count plot
                print(f"Creating count plot for {column_of_interest} in demographics")
                count_query = f"SELECT {column_of_interest}, COUNT(*) FROM demographics GROUP BY {column_of_interest}"
                count_data = cur.execute(count_query).fetchall()
                count_data = pd.DataFrame(count_data, columns=[column_of_interest, "Count"])
                plt.figure(figsize=(10, 6))
                sns.countplot(x=column_of_interest, data=count_data)
                plt.title(f"Count Plot of {column_of_interest} in Demographics")
                plt.xlabel(column_of_interest)
                plt.ylabel("Count")
                plt.show()
                # Create a pie chart
                print(f"Creating pie chart for {column_of_interest} in demographics")
                pie_query = f"SELECT {column_of_interest}, COUNT(*) FROM demographics GROUP BY {column_of_interest}"
                pie_data = cur.execute(pie_query).fetchall()
                pie_data = pd.DataFrame(pie_data, columns=[column_of_interest, "Count"])
                plt.figure(figsize=(10, 6))
                plt.pie(pie_data["Count"], labels=pie_data[column_of_interest], autopct='%1.1f%%', startangle=140)
                plt.title(f"Pie Chart of {column_of_interest} in Demographics")
                plt.axis('equal')
                plt.show()
            else:
                print("Invalid column type. Please choose a numeric or non-numeric column.")
                data_viz_flag = False
        
        elif table == "b":
            print("\nPrinting available Admission variables")
            dem_columns = get_columns("admissions")
            for column in dem_columns:
                print(column)
            column_of_interest = input("Which column would you like to investigate? ")
            column_type = get_column_type("admissions", column_of_interest)

            if column_type == "numeric":
                # Create a histogram
                print(f"Creating histogram for {column_of_interest} in admissions")
                histogram_query = f"SELECT {column_of_interest} FROM admissions"
                histogram_data = cur.execute(histogram_query).fetchall()
                histogram_data = pd.DataFrame(histogram_data, columns=[column_of_interest])
                plt.figure(figsize=(10, 6))
                sns.histplot(histogram_data[column_of_interest], bins=30, kde=True)
                plt.title(f"Histogram of {column_of_interest} in Admissions")
                plt.xlabel(column_of_interest)
                plt.ylabel("Frequency")
                plt.show()
                # Create a boxplot
                print(f"Creating boxplot for {column_of_interest} in admissions")
                boxplot_query = f"SELECT {column_of_interest} FROM admissions"
                boxplot_data = cur.execute(boxplot_query).fetchall()
                boxplot_data = pd.DataFrame(boxplot_data, columns=[column_of_interest])
                plt.figure(figsize=(10, 6))
                sns.boxplot(x=boxplot_data[column_of_interest])
                plt.title(f"Boxplot of {column_of_interest} in Admissions")
                plt.xlabel(column_of_interest)
                plt.show()
            
            elif column_type == "not numeric":
                # Create a count plot
                print(f"Creating count plot for {column_of_interest} in admissions")
                count_query = f"SELECT {column_of_interest}, COUNT(*) FROM admissions GROUP BY {column_of_interest}"
                count_data = cur.execute(count_query).fetchall()
                count_data = pd.DataFrame(count_data, columns=[column_of_interest, "Count"])
                plt.figure(figsize=(10, 6))
                sns.countplot(x=column_of_interest, data=count_data)
                plt.title(f"Count Plot of {column_of_interest} in Admissions")
                plt.xlabel(column_of_interest)
                plt.ylabel("Count")
                plt.show()
                # Create a pie chart
                print(f"Creating pie chart for {column_of_interest} in admissions")
                pie_query = f"SELECT {column_of_interest}, COUNT(*) FROM admissions GROUP BY {column_of_interest}"
                pie_data = cur.execute(pie_query).fetchall()
                pie_data = pd.DataFrame(pie_data, columns=[column_of_interest, "Count"])
                plt.figure(figsize=(10, 6))
                plt.pie(pie_data["Count"], labels=pie_data[column_of_interest], autopct='%1.1f%%', startangle=140)
                plt.title(f"Pie Chart of {column_of_interest} in Admissions")
                plt.axis('equal')
                plt.show()
            else:
                print("Invalid column type. Please choose a numeric or non-numeric column.")
                data_viz_flag = False

        elif table == "c":
            print("\nPrinting available financial variables")
            dem_columns = get_columns("finances")
            for column in dem_columns:
                print(column)
            column_of_interest = input("Which column would you like to investigate? ")
            column_type = get_column_type("finances", column_of_interest)

            if column_type == "numeric":
                # Create a histogram
                print(f"Creating histogram for {column_of_interest} in finances")
                histogram_query = f"SELECT {column_of_interest} FROM finances"
                histogram_data = cur.execute(histogram_query).fetchall()
                histogram_data = pd.DataFrame(histogram_data, columns=[column_of_interest])
                plt.figure(figsize=(10, 6))
                sns.histplot(histogram_data[column_of_interest], bins=30, kde=True)
                plt.title(f"Histogram of {column_of_interest} in Finances")
                plt.xlabel(column_of_interest)
                plt.ylabel("Frequency")
                plt.show()
                # Create a boxplot
                print(f"Creating boxplot for {column_of_interest} in finances")
                boxplot_query = f"SELECT {column_of_interest} FROM finances"
                boxplot_data = cur.execute(boxplot_query).fetchall()
                boxplot_data = pd.DataFrame(boxplot_data, columns=[column_of_interest])
                plt.figure(figsize=(10, 6))
                sns.boxplot(x=boxplot_data[column_of_interest])
                plt.title(f"Boxplot of {column_of_interest} in Finances")
                plt.xlabel(column_of_interest)
                plt.show()
            
            elif column_type == "not numeric":
                # Create a count plot
                print(f"Creating count plot for {column_of_interest} in Finances")
                count_query = f"SELECT {column_of_interest}, COUNT(*) FROM finances GROUP BY {column_of_interest}"
                count_data = cur.execute(count_query).fetchall()
                count_data = pd.DataFrame(count_data, columns=[column_of_interest, "Count"])
                plt.figure(figsize=(10, 6))
                sns.countplot(x=column_of_interest, data=count_data)
                plt.title(f"Count Plot of {column_of_interest} in Finances")
                plt.xlabel(column_of_interest)
                plt.ylabel("Count")
                plt.show()
                # Create a pie chart
                print(f"Creating pie chart for {column_of_interest} in Finances")
                pie_query = f"SELECT {column_of_interest}, COUNT(*) FROM finances GROUP BY {column_of_interest}"
                pie_data = cur.execute(pie_query).fetchall()
                pie_data = pd.DataFrame(pie_data, columns=[column_of_interest, "Count"])
                plt.figure(figsize=(10, 6))
                plt.pie(pie_data["Count"], labels=pie_data[column_of_interest], autopct='%1.1f%%', startangle=140)
                plt.title(f"Pie Chart of {column_of_interest} in Finances")
                plt.axis('equal')
                plt.show()
            else:
                print("Invalid column type. Please choose a numeric or non-numeric column.")
                data_viz_flag = False
        else:
            print("That is not a valid table option. Try Again.")

data_visualization()








# print(get_columns("finances"))
# where_function()
