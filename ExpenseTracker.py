from ClassStructures import *

exp = Expense()
inc = Income()

print("Welcome to Personal Expense Tracker\n")

while True:
    print("1. Input Income\n"
          "2. Add Expense\n"
          "3. View All Expenses\n"
          "4. View Summary\n"
          "5. Edit/Delete Entry\n"
          "6. Save Data\n"
          "7. Save and Exit\n"
          "--------------------")

    int_inp = validate(0)  # 0 for select action
                           # 1,2 for integer
                           # 3 for category
                           # -1 for filtering
                           # 5 for edit/delete
                           # 8 for entry choice
                           # 9 for sure
    if int_inp == 1:
        income_inp = validate(1)
        desc = input("Enter Description (Optional): ")
        date_time = time()
        inc.incomes.append([income_inp, date_time, desc])
        print("Income added\n"
              "------------")
    elif int_inp == 2:
        expense_inp = validate(2)
        category = validate(3)
        desc = input("Enter Description (Optional): ")
        date_time = time()
        exp.expenses.append([expense_inp, date_time, category, desc])
        new_df = pd.DataFrame([[expense_inp, date_time, category, desc]],
                                      columns=["Amount", "Date", "Category", "Description"])
        if exp.df.empty:
            exp.df = new_df
        else:
            exp.df = pd.concat([exp.df, new_df], ignore_index=True)

        print("Expense added\n"
              "-------------")
    elif int_inp == 3:
        exp.filter_exps()
    elif int_inp == 4:
        total_exp = 0
        total_inc = 0
        for row in exp.expenses:
            total_exp += float(row[0])
        for row in inc.incomes:
            total_inc += float(row[0])
        balance = total_inc - total_exp
        exp.df["Amount"] = exp.df["Amount"].astype(float)
        cat_sum = exp.df.groupby("Category")["Amount"].sum().round(2)
        print(f"REMAINING BALANCE: {balance}\n")
        if not cat_sum.empty:
            print("SPENDING BREAKDOWN OF EACH CATEGORY\n"
                  "-----------------------------------")
            print(cat_sum.to_string(index=True, name=False), "\n")
        else:
            print("No expenses..\n")
    elif int_inp == 5:
        df = exp.filter_exps()
        while True:
            if df is not None:
                indexes = df.index.tolist()
                entry_num = validate(8,indexes)
                edit_del = validate(5)
                if edit_del == 1:
                    current_row = df.loc[entry_num]
                    print(f"Editing Entry {entry_num}..\n"
                          "*** Leave blank to keep the current data! ***\n"
                          "------------------------------------\n",
                          current_row.to_string(index = True, name = False), "\n",sep="")
                    new_amount = str(validate(1,-99))  # -99 for blank inputs
                    new_cat = validate(3, -99)
                    new_desc = input("Enter Description (Optional): ")
                    exp.df.at[entry_num, 'Amount'] = new_amount if new_amount.strip() else current_row['Amount']
                    exp.df.at[entry_num, 'Category'] = new_cat if new_cat.strip() else current_row['Category']
                    exp.df.at[entry_num, 'Description'] = new_desc if new_desc.strip() else current_row['Description']
                    exp.expenses = exp.df.values.tolist()
                    print(f"Entry {entry_num} updated!\n")
                    break
                else:
                    print("------------------------------------\n",
                          df.loc[entry_num].to_string(index = True, name = False),sep="")
                    answer = validate(9,entry_num)
                    if answer:
                        exp.df.drop(entry_num, inplace=True)
                        exp.df.reset_index(drop=True, inplace=True)
                        exp.expenses = exp.df.values.tolist()
                        print(f"Entry {entry_num} deleted!\n")
                        break
                    else:
                        continue
            else:
                print("No entries to edit or delete..\n")
                break
    elif int_inp == 6:
        print("Saving data...")
        exp.save_exp()
        inc.save_incomes()
        print("Data Saved!\n")
    elif int_inp == 7:
        print("Saving data...")
        exp.save_exp()
        inc.save_incomes()
        print("Data Saved!\n")
        print("Exiting the application. Thank you!")
        break












