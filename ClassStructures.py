from datetime import datetime as dt
import csv, os
import pandas as pd

class Income:
    def __init__(self,amount = "",date= "",description = ""):
        self.date = date
        self.amount = amount
        self.description = description
        self.incomes = []  # amount, date, desc
        if not os.path.exists("incomes.csv"):
            with open("incomes.csv", "w", newline="") as file:
                spam_writer = csv.writer(file, delimiter=",")
                spam_writer.writerow(["Amount", "Date", "Description"])
                file.close()
        with open("incomes.csv", newline="") as file:
            spam_reader = csv.reader(file, delimiter=",")
            next(spam_reader)  # Skips the first row (header)
            for row in spam_reader:
                row_list = []
                for i in row:
                    row_list.append(i)
                self.incomes.append(row_list)
            file.close()
    def save_incomes(self):
        with open("incomes.csv", "w", newline="") as file:
            spam_writer = csv.writer(file, delimiter=",")
            spam_writer.writerow(["Amount", "Date", "Description"])
            for row in self.incomes:
                spam_writer.writerow(row)
    def __str__(self):
        if self.description.strip():
            description = f"\nDescription: {self.description}"
        else:
            description = ""
        return (f"---------------------\n"
                f"Amount: {self.amount}\n"
                f"Date & Time: {self.date}"
                f"{description}")

class Expense:
    def __init__(self,amount = "",date = "",category = "",description = ""):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description
        self.expenses = []  # amount, date, category, desc
        if not os.path.exists("expenses.csv"):
            with open("expenses.csv", "w", newline="") as file:
                spam_writer = csv.writer(file, delimiter=",")
                spam_writer.writerow(["Amount", "Date", "Category", "Description"])
                file.close()
        with open("expenses.csv", newline="") as file:
            spam_reader = csv.reader(file, delimiter=",")
            next(spam_reader)  # Skips the first row (header)
            for row in spam_reader:
                row_list = []
                for i in row:
                    row_list.append(i)
                self.expenses.append(row_list)
        self.df = pd.DataFrame(self.expenses, columns=["Amount", "Date", "Category", "Description"])

    def save_exp(self):
        with open("expenses.csv", "w", newline="") as file:
            spam_writer = csv.writer(file, delimiter=",")
            spam_writer.writerow(["Amount", "Date", "Category", "Description"])
            for row in self.expenses:
                spam_writer.writerow(row)
    def filter_exps(self):
        filt_type, filt = validate(-1)
        if filt_type == "Category":
            filt_df = self.df[self.df.Category == filt]
        elif filt_type == "Date":
            filt_df = self.df[(self.df.Date.str[:2] == filt[0]) & (self.df.Date.str[3:5] == filt[1]) \
                         & (self.df.Date.str[6:10] == filt[2])]
        else:
            filt_df = self.df

        print("EXPENSES TABLE\n----------------------------------------------------")
        if filt_df.empty:
            print("No Expenses\n")
            return None
        else:
            print(filt_df, "\n")
            return filt_df

    def __str__(self):
        if self.description.strip():
            description = f"\nDescription: {self.description}"
        else:
            description = ""
        return (f"---------------------\n"
                f"Amount: {self.amount}\n"
                f"Date & Time: {self.date}\n"
                f"Category: {self.category}"
                f"{description}")

def validate(action, num=None):
    if 0 < action < 3:
        inp = None
        while True:
            amount_inp = input("Enter Amount: ")
            if (not amount_inp.strip()) and num == -99:
                return ""
            try:
                inp = float(amount_inp)
            except (ValueError, TypeError):
                print("Please enter an integer or a floating number using dot")
                continue
            break
        return round(inp, 2)
    elif action == 0:
        int_inp2 = None
        while True:
            user_input = input("Select Action: ")
            try:
                int_inp2 = int(user_input)
            except (ValueError, TypeError):
                print("Please enter an integer")
                continue
            if not 0 < int_inp2 < 8:
                print("Please enter a number from 1 to 7")
                continue
            else:
                break
        return int_inp2
    elif action == 3:
        while True:
            category = input("Enter Category: ")
            if (not category.strip()) and num == -99:
                return ""
            elif not category.strip():
                print("Please enter a category")
                continue
            elif not any(char.isalpha() for char in category):
                print("Please enter a text")
                continue
            else:
                break
        return category
    elif action == -1:
        while True:
            filt_inp = input("Enter \"Date\" (D-M-Y) or \"Category\" to Filter Expenses (Optional): ")
            if not filt_inp.strip():
                return False, ""
            else:
                inp_type, inp = is_date_cat(filt_inp)
                if inp_type == 1:
                    return "Category", inp
                elif inp_type == 2:
                    return "Date", inp
                else:
                    print("Please enter an appropriate date or text")
                    continue
    elif action == 5:
        int_inp3 = None
        while True:
            user_input = input("Edit (1)/Delete (2): ")
            try:
                int_inp3 = int(user_input)
            except (ValueError, TypeError):
                print("Please enter an integer")
                continue
            if not 0 < int_inp3 < 3:
                print("Please enter 1 or 2")
                continue
            else:
                break
        return int_inp3
    elif action == 8:
        int_inp4 = None
        while True:
            user_inp = input("Choose an entry number: ")
            try:
                int_inp4 = int(user_inp)
            except (ValueError, TypeError):
                print("Please enter an integer")
                continue
            if not int_inp4 in num:
                if len(num) > 10:
                    print("Please enter a number among appropriate numbers..")
                else:
                    print(f"Please enter a number among {[i for i in num]}")
                continue
            else:
                break
        return int_inp4
    elif action == 9:
        while True:
            user_inp = input(f"------------------------------------\n"
                             f"Are you sure deleting entry {num}? (y/n): ")
            if user_inp.lower() == "y":
                return True
            elif user_inp.lower() == "n":
                return False
            else:
                print("Please enter y or n")
                continue
def time():
    now = dt.now()
    if len(str(now.month)) == 1:
        month = f"0{now.month}"
    else:
        month = now.month
    if len(str(now.day)) == 1:
        day = f"0{now.day}"
    else:
        day = now.day
    if len(str(now.hour)) == 1:
        hour = f"0{now.hour}"
    else:
        hour = now.hour
    if len(str(now.minute)) == 1:
        minute = f"0{now.minute}"
    else:
        minute = now.minute
    if len(str(now.second)) == 1:
        second = f"0{now.second}"
    else:
        second = now.second
    return f"{day}/{month}/{now.year} - {hour}:{minute}:{second}"
def format_time(time_inp):

    if len(time_inp[0]) == 1:
        day = f"0{time_inp[0]}"
    else:
        day = time_inp[0]
    if len(time_inp[1]) == 1:
        month = f"0{time_inp[1]}"
    else:
        month = time_inp[1]
    return [day,month,time_inp[2]]
def is_date_cat(inp):
    dash = inp.split("-")
    slash = inp.split("/")
    dot = inp.split(".")
    if len(dash) == 3:
        dates = dash
    elif len(slash) == 3:
        dates = slash
    elif len(dot) == 3:
        dates = dot
    else:
        dates = [-1,-1,-1]

    if 0 < int(dates[0]) < 32 and 0 < int(dates[1]) < 13 and 0 < int(dates[2]) < 10000:
        dates = format_time(dates)
        return 2, dates
    elif any(char.isalpha() for char in inp):
        return 1, inp
    else:
        return False, False









