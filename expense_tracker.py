from expense import Expense
import datetime
import calendar
import matplotlib.pyplot as plt
import pandas as pd

def plot_expenses(expense_file_name):
    # Load data from CSV file
    df = pd.read_csv(expense_file_name, names=["name", "amount", "category"])

    # Aggregate expenses by category
    expense_summary = df.groupby('category').amount.sum().reset_index()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(expense_summary['category'], expense_summary['amount'], color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Amount Spent')
    plt.title('Expenses by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    print(f" 🎯 Running Expense Tracker!")
    expense_file_name = "expenses.csv"
    income = int(input("Enter Your Yearly Income: \n"))
    budget = income / 12


    while True:
        # Ask user if they want to reset
        action = input("Type '1' if you want to add an expense, '2' to reset, '3' to quit\n")
        
        if action == "1":
            # User input for expense
            expense = get_user_expense()

            # Write their expense to a file
            save_expense_to_file(expense, expense_file_name)

            # Read file, summarize expenses, and plot
            summarize_expenses(expense_file_name, budget)

            show_plot = input("Do you want to see a graph of your expenses? (yes/no)\n").lower()
            if show_plot == "yes":
                plot_expenses(expense_file_name)


        elif action == "2":
            reset_expenses(expense_file_name)
        elif action == "3":
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid input! Please try again.")


def get_user_expense():
    print(f" 🎯 Getting User Expense") 
    expense_name = input("Enter expense name: \n")
    print(f"You've entered {expense_name}")
    
    expense_cost = float(input("Enter expense cost: \n"))
    expense_categories = [
        '🛒 Groceries', 
        '🍔 Fast Food', 
        '💼 Work', 
        '🎉 Fun', 
        '✨ Misc'
        ]

    while True:
        print("Select a category: ")
        for i,category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")    
         
        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number:{value_range}\n"))- 1#may need a user experience fix later
        
        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name = expense_name, category=selected_category, amount=expense_cost  )
            return new_expense
        else:
            print("Value out of range! Please try again.")
 


        
    
def save_expense_to_file(expense: Expense,expense_file_name):
     print(f" 🎯 Saving User Expense: {expense} to {expense_file_name}")
     with open(expense_file_name, "a") as f:
         f.write(f"{expense.name}, {expense.amount}, {expense.category}\n")
         
     

def summarize_expenses(expense_file_name, budget):
    print(f" 🎯 Summarizing User Expense")
    expenses: list[Expense] = []
    with open(expense_file_name, "r") as f:
       lines = f.readlines()
       for line in lines:
           expense_name, expense_amount, expense_category = line.strip().split(",")
           line_expense = Expense(name=expense_name, amount=float(expense_amount), category= expense_category,)
           expenses.append(line_expense)
           
    
     
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key]+= expense.amount
        else: 
            amount_by_category[key] = expense.amount
    
    print("Expenses By Category: 📈")
    for key,amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")
    
    total_spent = sum([x.amount for x in expenses])
    print(f"💵 You've spent ${total_spent:.2f} this month")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")
    
    now = datetime.datetime.now()

    
    days_in_month = calendar.monthrange(now.year, now.month)[1]


    remaining_days = days_in_month - now.day


    daily_budget = remaining_budget / remaining_days
    print(f"👉 Budget Per Day: ${daily_budget:.2f}")
    if remaining_budget / budget < 0.1:
        print(" 🚨 You have used more than 90% of your budget.")
        print(f"👉 To stay within your budget, you can only spend ${daily_budget:.2f} per day for the rest of the month.")
    elif remaining_budget / budget < 0.25:
        print("⚠️ You have used more than 75% of your budget.")
    elif remaining_budget / budget < 0.5:
        print("🔔 You have used more than 50% of your budget.")
    
    if remaining_budget < 0:
        print("🚨 You've exceeded your budget! Consider reducing non-essential expenses.")

def reset_expenses(expense_file_name):
    with open(expense_file_name, "w") as f:
        f.write("")  # Overwrite the file with nothing
    print(f" 🔄 Expenses have been reset.")





if __name__ == "__main__":
    main()

