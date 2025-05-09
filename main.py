# Names: Ian Sargent and Atticus Tarleton
# Class: CS 2500 Intro to Database Systems
# Date: May 2nd, 2025
# Final Project

# Description: This program is a database management system for universities. 
# It allows users to modify data, perform statistical analysis, and visualize data from the database.


# Importing necessary packages
import sqlite3
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math


# Adding records to superintendent table
con = sqlite3.connect('private_schools.db', isolation_level=None)
cur = con.cursor()
list = []


# Table is string, column is string
def mean(table, column):
    count_query = f"SELECT COUNT({column}) from {table}"
    sum_query = f"SELECT sum({column}) from {table}"
    count = cur.execute(count_query).fetchall()[0][0]
    sum = cur.execute(sum_query).fetchall()[0][0]
    avg = sum/count
    return avg

# Standard deviation function
def standard_deviation(table, column):
    mean_value = mean(table, column)
    get_vals_query = f"SELECT {column} FROM {table}"
    values = cur.execute(get_vals_query).fetchall()
    count_query = f"SELECT COUNT({column}) FROM {table}"
    count = cur.execute(count_query).fetchall()[0][0]
    running_variance = 0
    for i in values:
        val = i[0]
        deviation = (val - mean_value)**2
        running_variance += deviation
    running_variance = running_variance/count
    standard_deviation_total = math.sqrt(running_variance)
    return  standard_deviation_total

# Minimum and Maximum functions
def min(table, column):
    get_vals_query = f"SELECT {column} FROM {table} ORDER BY {column} ASC"
    vals = cur.execute(get_vals_query).fetchall()[0][0]
    return vals


def max(table, column):
    get_vals_query = f"SELECT {column} FROM {table} ORDER BY {column} DESC"
    vals = cur.execute(get_vals_query).fetchall()[0][0]
    return vals

# Median function
def median(table, column):
    count_query = f"SELECT COUNT({column}) FROM {table}"
    count = cur.execute(count_query).fetchall()[0][0]
    get_vals_query = f"SELECT {column} FROM {table} ORDER BY {column} DESC"
    vals = cur.execute(get_vals_query).fetchall()
    if count % 2 == 0:
         index = count//2
         index_1 = index
         index_2 = index + 1
         return (vals[index_1][0]+vals[index_2][0])/2

    else:
        index = count/2 + .5
        return vals[int(index)][0]


# Function to prodice "where" statement queries
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
    column = input("What column are you comparing to: ")
    type = ""
    columns_all = (cur.execute(f"PRAGMA table_info({table})").fetchall())
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
    user_value = input("Finally, choose your value to compare things to: ")
    statement = f"{table} WHERE {column} {sign} '{user_value}'"
    return statement


# Function returning the columns of a table
def get_columns(table):
    columns_all = (cur.execute(f"PRAGMA table_info({table})").fetchall())
    columns_list = []
    for i in columns_all:
        columns_list.append(i[1])
    return columns_list


# Function to print sample data from a table
def print_sample_data(table):
    sample_data_query = f"SELECT * FROM {table}"
    sample_data = cur.execute(sample_data_query).fetchall()
    sample_data_list = []
    print("Column Names: ", end = "  ")
    for i in get_columns(table):
        print(i, end=" ")
    print("")
    for i in sample_data:
        sample_data_list.append(i)
        print(i)
    return sample_data_list


# Function to get the type of a column
def get_column_type(table, column):
    type = ""
    columns_all = (cur.execute(f"PRAGMA table_info({table})").fetchall())
    for i in columns_all:
        if i[1] == column:
            if i[2] != "":
                type = "numeric"
            else:
                type = "not numeric"
    return type


# Allows for all tables to be joined with superintendents and calls the mean of all numeric columns
def mean_join_with_superintendents(table):
    super_join_admissions_statement = f"SELECT superintendents.first_name, superintendents.last_name"

    columns = get_columns(table)
    
    for i in columns:
        if get_column_type(table, i) == "numeric":
            super_join_admissions_statement += f",ROUND(SUM({i})/COUNT(school_id), 2)"
    
    super_join_admissions_statement += f"FROM {table} LEFT JOIN superintendents ON {table}.super_id == superintendents.super_id GROUP BY superintendents.super_id"
    return_statement = cur.execute(super_join_admissions_statement).fetchall()
    
    print("These are the averages of each column: ", end="  ")
    
    for i in get_columns(table):
        print(i, end=" ")
    print("for each superintendent")
    
    for i in return_statement:
        print(i)
    
    return return_statement


# Modify data function for non superintendent table (assuming only numeric data)
def modify_table_non_super(table):
    columns = get_columns(table)
    columns_numeric = [] #these are the columns that can be modified
    print("Here are the columns you can modify")
    for i in columns:
        if get_column_type(table, i) == "numeric":
            columns_numeric.append(i)
            print(i)
    user_data_q = input("Hello user. Do you need access to the database to find the school id of the"
          " school you want modify (y/n): ")
    if user_data_q == 'y':
        print_sample_data(table)
    school_id_chosen = input("Hello user. Please enter the school id of the school whose data you want to modify: ")
    adding_new_info = True
    column = ""
    new_info = ""
    while adding_new_info:
        input_columns = True
        while input_columns == True:
            column = input("Which info would you like to edit: ")
            if column not in columns_numeric:
                print("Please input a column you can modify")
            else:
                input_columns = False
        new_info = input(f"what would you like to set {column} to: ")
        update_info_to = f'''UPDATE {table} SET {column} = "{new_info}" WHERE school_id = "{school_id_chosen}";'''
        try:
            cur.execute(update_info_to)
            adding_new_info = False
        except sqlite3.OperationalError:
            print("Data was entered incorrectly. Please try again.")
    print(f"You updated {column} by making its new value {new_info} for the school with school id {school_id_chosen}")
    
    return "hi"


# Modify data function for superintendent table
def modify_table_super():
    user_data_query = input("Hello user. Do you need access to the database to find the super_id of the"
                        " superintendent you want modify? (y/n): ")
    if user_data_query == 'y':
        print_sample_data("superintendents")
    columns_to_edit = ['first_name', 'last_name', 'city']
    print("Here are the columns you can modify")
    for i in columns_to_edit:
        print(i)
    super_id = input("Hello user. Please enter the super_id of the superintendent whose data you want to modify: ")
    adding_new_info = True
    column = ""
    while adding_new_info:
        input_columns = True
        while input_columns:
            column = input("which column would you like to edit: ")
            if column not in columns_to_edit:
                print("Please input a column you can modify")
            else:
                input_columns = False
        new_value = input(f"What would you like to set {column} to: ")
        try:
            # This uses parameter substitution to avoid syntax issues and SQL injection
            query = f"UPDATE superintendents SET {column} = ? WHERE super_id = ?"
            cur.execute(query, (new_value, super_id))
            print(f"Updated {column} to '{new_value}' for superintendents with super_id {super_id}.")
            break
        except sqlite3.OperationalError as e:
            print("OperationalError occurred:", e)
            print("Please double-check your input and try again.")



def add_row(table):
    add_row = input("Do you want to add a row y/n: ")
    
    if add_row == "y":
        cols = get_columns(table)
        user_inputs = []
        make_new_line = (f"INSERT INTO {table}(")
        
        for i in cols:
            user_input = input(f"Input a value for column {i}: ")
            make_new_line += f"{i},"
            user_inputs.append(user_input)
        make_new_line = make_new_line[:-1]
        make_new_line += ") VALUES ("
        
        for i in user_inputs:
            make_new_line += f"'{i}',"
        make_new_line = make_new_line[:-1]
        make_new_line+=")"
        cur.execute(make_new_line)
    
    return "poop :)"

def remove_row(table):
    remove_rows = input("Do you want to remove a row y/n: ")
    if table == "superintendent":
        super_id = input("enter the super_id of the person you want to remove: ")
        remove_rows_query = f"DELETE FROM {table} where super_id = '{super_id}'"
    else:
        school_id = input("enter the school of the school you want to remove: ")
        remove_rows_query = f"DELETE FROM {table} where school_id = '{school_id}'"
    cur.execute(remove_rows_query)




# Statistical summary function
def statistical_summary():
    print("\nChoose a table to analyze:\n1. Admissions\n2. Demographics\n3. Finances\n4. Superintendents")
    # User input for the table of interest
    table_choice = input("\nEnter the number corresponding to your choice (1-4): ")
    # Reassign input selection to the table name
    if table_choice == '1': 
        table = "admissions"
    elif table_choice == '2':
        table = "demographics"
    elif table_choice == '3':
        table = "finances"
    elif table_choice == '4':
        table = "superintendents"
    else:
        print("Invalid choice. Please choose a valid table.")
    
    # Print the columns of the selected table
    available_columns = get_columns(table)
    # Printing available columns
    print("\nAvailable columns:\n_________________")
    for column in available_columns:
        print(column)
    
    # User input for the column of interest
    column = input("\nEnter the column you want to analyze: ")
    # Get column type for tailored statistics
    col_type = get_column_type(table, column)
    
    # If the column is non-numeric, calculate and print categorical statistics (using sqlite3 queries)
    if col_type == "not numeric":
        print(f"\nStatistics for {column} in {table}:")
        print("-------------------------------")
        print(f"Count: {cur.execute(f'SELECT COUNT({column}) FROM {table}').fetchone()[0]}")
        print(f"Unique Values: {cur.execute(f'SELECT COUNT(DISTINCT {column}) FROM {table}').fetchone()[0]}")
        print(f"Most Common Value: {cur.execute(f'SELECT {column}, COUNT(*) FROM {table} GROUP BY {column} ORDER BY COUNT(*) DESC LIMIT 1').fetchone()}")
        print(f"Least Common Value: {cur.execute(f'SELECT {column}, COUNT(*) FROM {table} GROUP BY {column} ORDER BY COUNT(*) ASC LIMIT 1').fetchone()}\n")

    # If the column is numeric, calculate and print numerical statistics
    elif col_type == "numeric":
        print(f"\nStatistics for {column} in {table}:")
        print("--------------------------------")
        print(f"Mean: {mean(table, column)}")
        print(f"Standard Deviation: {standard_deviation(table, column):.2f}")
        print(f"Minimum: {min(table, column)}")
        print(f"Maximum: {max(table, column)}")
        print(f"Median: {median(table, column)}\n")
    
    # If the column type is neither numeric nor non-numeric, print an error message (not likely)
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
        print("\nAvailable columns:\n-----------------")
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

        # For the non-numeric column, create a count plot and pie chart
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
        
        # Invalid column type (not likely)
        else:
            print("Invalid column type. Please choose a numeric or non-numeric column.")
            

# The main function to run the program
def main():
    # Boolean flag to control the main loop
    main_flag = True
    # Print the welcome message and options
    while main_flag:
        print("Welcome to the Private School Data Analysis Tool!")
        print("1. Modify Data")
        print("2. Statistics")
        print("3. Data Visualization")
        print("4. Exit")
        
        # User input for the action choice
        choice = input("Please choose an option (1-4): ")

        # Reassign input selection to the table name
        if choice == '1':
            table = input("\nWhich table would you like to modify?\n1. Admissions\n2. Demographics\n3. Finances\n4. Superintendents\n==> ")
            if table == '1':
                table = "admissions"
            elif table == '2':
                table = "demographics"
            elif table == '3':
                table = "finances"
            elif table == '4':
                table = "superintendents"
            else:
                print("Invalid choice. Please choose a valid table.")

            # If the table is "superintendents", call the modify_table_super function and add_row
            if table == "superintendents":
                modify_table_super()
                add_row(table)
            
            # Otherwise, call the modify_table_non_super function and add_row
            else:
                modify_table_non_super(table)
                add_row(table)

        # If the user chooses statistics, call the statistical_summary function
        elif choice == '2':
            statistical_summary()
            table = input(
                "\nWhich table would you like to join to superintendents?\n1. Admissions\n2. Demographics\n3. Finances\n==> ")
            if table == '1':
                table = "admissions"
            elif table == '2':
                table = "demographics"
            elif table == '3':
                table = "finances"
            else:
                print("Invalid choice. Please choose a valid table.")
            mean_join_with_superintendents(table)

        
        # If the user chooses data visualization, call the data_visualization function
        elif choice == '3':
            data_visualization()

        # If the user chooses to exit, set the main_flag to False
        elif choice == '4':
            main_flag = False
            print("Exiting the program. Goodbye!")

        # Input validation for invalid choices
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # Run the main function
    main()
    # Close the database connection
    con.close()