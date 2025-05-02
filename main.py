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
    vals = cur.execute(get_vals_query).fetchall()[0][0]
    return vals


def max(table, column):
    get_vals_query = f"select {column} from {table} order by {column} desc"
    vals = cur.execute(get_vals_query).fetchall()[0][0]
    return vals


def median(table, column):
    count_query = f"select COUNT({column}) from {table}"
    count = cur.execute(count_query).fetchall()[0][0]
    get_vals_query = f"select {column} from {table} order by {column} desc"
    vals = cur.execute(get_vals_query).fetchall()
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

#join statements

#this code does not do what its supposed to. it instead just finds the mean of the columns
def mean_of_columns(table):
    means = []
    columns = get_columns(table)
    for i in columns:
        if get_column_type(table, i) == "numeric":
            means.append(mean(table, i))
    return means

def median_of_columns(table):
    medians = []
    columns = get_columns(table)
    for i in columns:
        if get_column_type(table, i) == "numeric":
            medians.append(median(table, i))
    return medians

def std_of_columns(table):
    std = []
    columns = get_columns(table)
    for i in columns:
        if get_column_type(table, i) == "numeric":
            std.append(standard_deviation(table, i))
    return std

def min_of_columns(table):
    mins = []
    columns = get_columns(table)
    for i in columns:
        if get_column_type(table, i) == "numeric":
            mins.append(min(table, i))
    return mins

def max_of_columns(table):
    maxs = []
    columns = get_columns(table)
    for i in columns:
        if get_column_type(table, i) == "numeric":
            maxs.append(max(table, i))
    return maxs


# checking to see things work
# print("mean of each option below")
# print("number of applicants, percent admitted, incoming class size, average GPA, average SAT, percent STEM")
# print(max_of_columns("admissions"))



def mean_join_with_superintendents(table):
    super_join_admissions_statement = f"select superintendents.first_name, superintendents.last_name"

    columns = get_columns(table)
    for i in columns:
        if get_column_type(table, i) == "numeric":
            super_join_admissions_statement += f",sum({i})/count(school_id)"
    super_join_admissions_statement += f"from {table} left join superintendents on {table}.super_id == superintendents.super_id group by superintendents.super_id"
    return_statement = cur.execute(super_join_admissions_statement).fetchall()
    return return_statement

#testing to see if this works
# print(mean_join_with_superintendents("admissions"))

# modify data function (assuming only numeric data
#also assuming not superintendent
def modify_table_non_super(table):
    columns = get_columns(table)
    columns_numeric = [] #these are the columns that can be modified
    print("here are the columns you can modify")
    for i in columns:
        if get_column_type(table, i) == "numeric":
            columns_numeric.append(i)
            print(i)
    user_data_q = input("Hello user. Do you need access to the database to find the school id of the"
          "school you want modify (y/n): ")
    if user_data_q == 'y':
        print_sample_data(table)
    school_id_chosen = input("hello user. please enter the school id of the school whose data you want to modify: ")
    adding_new_info = True
    column = ""
    new_info = ""
    while adding_new_info:
        input_columns = True
        while input_columns == True:
            column = input("which info would you like to edit: ")
            if column not in columns_numeric:
                print("please input a column you can modify")
            else:
                input_columns = False
        new_info = input(f"what would you like to set {column} to: ")
        update_info_to = f"UPDATE {table} SET {column} = '{new_info}' WHERE school_id = '{school_id_chosen}';"
        try:
            cur.execute(update_info_to)
            adding_new_info = False
        except sqlite3.OperationalError:
            print("Data was entered incorrectly, try again")
    print(f"you updated {column} by making its new value {new_info} for the school with school id {school_id_chosen}")
    return "hi"

def modify_table_super():
    user_data_q = input("Hello user. do you need access to the database to find the super_id of the"
                        "superintendent you want modify (y/n): ")
    if user_data_q == 'y':
        print_sample_data("superintendents")
    columns_to_edit = ['first_name', 'last_name', 'city']
    print("here are the columns you can modify")
    for i in columns_to_edit:
        print(i)
    school_id_chosen = input("hello user. please enter the super_id of the superintendent whose data you want to modify: ")
    adding_new_info = True
    column = ""
    new_info = ""
    while adding_new_info:
        input_columns = True
        while input_columns:
            column = input("which info would you like to edit: ")
            if column not in columns_to_edit:
                print("please input a column you can modify")
            else:
                input_columns = False
        new_info = input(f"what would you like to set {column} to: ")
        update_info_to = f"UPDATE superintendent SET {column} = '{new_info}' WHERE school_id = '{school_id_chosen}';"
        try:
            cur.execute(update_info_to)
            adding_new_info = False
        except sqlite3.OperationalError:
            print("Data was entered incorrectly, try again")
    print(f"you updated {column} by making its new value {new_info} for the superintendent with super_id {school_id_chosen}")
    return "hi"



def add_row():
    return "poop :)"


def statistical_summary():
    table = input("Enter the table name (admissions, demographics, finances, superintendents): ")
    available_columns = get_columns(table)
    print("\nAvailable columns:\n_________________")

    for column in available_columns:
        print(column)

    column = input("\nEnter the column name: ")
    col_type = get_column_type(table, column)

    if col_type == "not numeric":
        print(f"\nStatistics for {column} in {table}:")
        print("_______________________________")
        print(f"\nCount: {cur.execute(f'SELECT COUNT({column}) FROM {table}').fetchone()[0]}")
        print(f"\nUnique Values: {cur.execute(f'SELECT COUNT(DISTINCT {column}) FROM {table}').fetchone()[0]}")
        print(f"\nMost Common Value: {cur.execute(f'SELECT {column}, COUNT(*) FROM {table} GROUP BY {column} ORDER BY COUNT(*) DESC LIMIT 1').fetchone()}")
        print(f"\nLeast Common Value: {cur.execute(f'SELECT {column}, COUNT(*) FROM {table} GROUP BY {column} ORDER BY COUNT(*) ASC LIMIT 1').fetchone()}\n")

    elif col_type == "numeric":
        print(f"\nStatistics for {column} in {table}:")
        print("_______________________________")
        print(f"\nMean: {mean(table, column)}")
        print(f"\nStandard Deviation: {standard_deviation(table, column):.2f}")
        print(f"\nMinimum: {min(table, column)}")
        print(f"\nMaximum: {max(table, column)}")
        print(f"\nMedian: {median(table, column)}\n")

    else:
        print("Invalid column type. Please choose a numeric or non-numeric column.")

# Data Visualization Function
def data_visualization():
    # Flag to exit the loop once comepleted
    data_viz_flag = True
    while data_viz_flag:
        
        # User input for the table of interest
        table = input("Choose a category to investigate\na) Demographics\nb) Admissions\nc) Finances\nd) Superintendents\nd==> ")

        # Reassign input selection to the table name
        if table == 'a':
            table_name = "demographics"
        elif table == 'b':
            table_name = "admissions"
        elif table == 'c':
            table_name = "finances"
        elif table == 'd':
            table_name = "superintendents"
        else:
            print("Invalid choice. Please choose a valid category.")
        
        # Get the columns of the selected table
        available_columns = get_columns(table_name)
        
        # Print the columns
        print("\nAvailable columns:\n_________________")
        for column in available_columns:
            print(column)
        
        # User input for the column of interest
        column_of_interest = input("\nWhich column would you like to investigate? ")
        # Confirm selected column type for the correct plots to show
        column_type = get_column_type(table_name, column_of_interest)

        # For the numeric column, create a histogram and boxplot
        if column_type == "numeric":
            # Creating a dataframe for the histogram and boxplot
            num_plot_query = f"SELECT {column_of_interest} FROM {table_name}"
            num_plot_data = cur.execute(num_plot_query).fetchall()
            num_plot_data = pd.DataFrame(num_plot_data, columns=[column_of_interest])
            
            # Create the histogram
            plt.figure(figsize=(10, 6))
            sns.histplot(num_plot_data[column_of_interest], bins=30, kde=True)
            plt.title(f"Histogram of {column_of_interest} in {table_name}")
            plt.xlabel(column_of_interest)
            plt.ylabel("Frequency")
            plt.show()
            
            # Create the boxplot
            plt.figure(figsize=(10, 6))
            sns.boxplot(x=num_plot_data[column_of_interest])
            plt.title(f"Boxplot of {column_of_interest} in {table_name}")
            plt.xlabel(column_of_interest)
            plt.show()

            # Exiting the loop
            data_viz_flag = False    

        elif column_type == "not numeric":
            
            # Creating a dataframe for the count plot and pie chart
            count_query = f"SELECT {column_of_interest}, COUNT(*) FROM {table_name} GROUP BY {column_of_interest}"
            count_data = cur.execute(count_query).fetchall()
            count_data = pd.DataFrame(count_data, columns=[column_of_interest, "Count"])
            
            # Create the count plot
            plt.figure(figsize=(10, 6))
            sns.countplot(x=column_of_interest, data=count_data)
            plt.title(f"Count Plot of {column_of_interest} in {table_name}")
            plt.xlabel(column_of_interest)
            plt.ylabel("Count")
            plt.show()
            
            # Create the pie chart
            plt.figure(figsize=(10, 6))
            plt.pie(count_data["Count"], labels=count_data[column_of_interest], autopct='%1.1f%%', startangle=140)
            plt.title(f"Pie Chart of {column_of_interest} in {table_name}")
            plt.axis('equal')
            plt.show()

            # Exiting the loop
            data_viz_flag = False
        
        else:
            print("Invalid column type. Please choose a numeric or non-numeric column.")
            
        
if __name__ == "__main__":
    main_flag = True
    while main_flag:
        print("Welcome to the Private School Data Analysis Tool!")
        print("1. Modify Data")
        print("2. Statistics")
        print("3. Data Visualization")
        print("4. Exit")
        choice = input("Please choose an option (1-4): ")

        if choice == '1':
            print("hello")
            # modify_table()

        elif choice == '2':
            statistical_summary()

        elif choice == '3':
            data_visualization()

        elif choice == '4':
            data_viz_flag = False
            print("Exiting the program. Goodbye!")

        else:
            print("Invalid choice. Please try again.")