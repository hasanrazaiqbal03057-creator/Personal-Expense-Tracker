
import streamlit as st
from datetime import date

# --------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Personal Expense Tracker")
st.header("Manage Your Daily Expenses")

# --------------------------------
# 2. SESSION STATE
# --------------------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "next_id" not in st.session_state:
    st.session_state.next_id = 1

categories = ["Food", "Travel", "Shopping", "Bills", "Other"]


# --------------------------------
# 3. ADD EXPENSE FUNCTION
# --------------------------------

def add_expense(name, amount, category, expense_date):

    expense = {
        "ID": st.session_state.next_id,
        "Expense Name": name,
        "Amount": amount,
        "Category": category,
        "Date": expense_date.strftime("%Y-%m-%d")
    }

    st.session_state.expenses.append(expense)
    st.session_state.next_id += 1


# --------------------------------
# 4. ADD EXPENSE FORM
# --------------------------------

st.subheader("➕ Add New Expense")

with st.form("expense_form"):

    expense_name = st.text_input("Expense Name")

    amount = st.number_input(
        "Amount (Rs.)",
        min_value=0.01,
        value=100.0,
        step=10.0
    )

    category = st.selectbox(
        "Category",
        categories
    )

    expense_date = st.date_input(
        "Expense Date",
        value=date.today()
    )

    submit = st.form_submit_button("Add Expense")

    if submit:

        if expense_name.strip() == "":
            st.error("Please enter an expense name.")

        else:
            add_expense(
                expense_name.strip(),
                amount,
                category,
                expense_date
            )

            st.success("Expense added successfully!")


# --------------------------------
# 5. DELETE EXPENSE
# --------------------------------

st.subheader("🗑️ Delete Expense")

if st.session_state.expenses:

    for expense in list(st.session_state.expenses):

        if st.button(
            f"Delete: {expense['Expense Name']} - Rs. {expense['Amount']}",
            key=f"delete_{expense['ID']}"
        ):

            st.session_state.expenses.remove(expense)

            st.success("Expense deleted successfully!")
            break

else:
    st.warning("No expenses available to delete.")


# --------------------------------
# 6. SIDEBAR SEARCH AND FILTERS
# --------------------------------

st.sidebar.header("Search & Filters")

search_name = st.sidebar.text_input(
    "Search Expense"
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + categories
)

# Find maximum expense amount

if st.session_state.expenses:

    max_amount = max(
        expense["Amount"]
        for expense in st.session_state.expenses
    )

else:
    max_amount = 1000.0

amount_range = st.sidebar.slider(
    "Filter by Amount (Rs.)",
    min_value=0.0,
    max_value=float(max_amount),
    value=(0.0, float(max_amount)),
    step=1.0
)


# --------------------------------
# 7. FILTER EXPENSES
# --------------------------------

def filter_expenses(expenses):

    filtered = []

    for expense in expenses:

        # Search filter

        if search_name.lower() not in expense["Expense Name"].lower():
            continue

        # Category filter

        if selected_category != "All":
            if expense["Category"] != selected_category:
                continue

        # Amount filter

        if not (
            amount_range[0]
            <= expense["Amount"]
            <= amount_range[1]
        ):
            continue

        filtered.append(expense)

    return filtered


filtered_expenses = filter_expenses(
    st.session_state.expenses
)


# --------------------------------
# 8. DASHBOARD SUMMARY
# --------------------------------

st.header("📊 Dashboard Summary")

all_expenses = st.session_state.expenses

total_expenses = sum(
    expense["Amount"]
    for expense in all_expenses
)

total_transactions = len(all_expenses)

if all_expenses:

    highest_expense = max(
        all_expenses,
        key=lambda expense: expense["Amount"]
    )

    highest_amount = highest_expense["Amount"]

else:
    highest_amount = 0


st.metric(
    "Total Expenses",
    f"Rs. {total_expenses:,.2f}"
)

st.metric(
    "Total Transactions",
    total_transactions
)

st.metric(
    "Highest Expense",
    f"Rs. {highest_amount:,.2f}"
)


# --------------------------------
# 9. EXPENSE RECORDS TABLE
# --------------------------------

st.header("📋 Expense Records")

if filtered_expenses:

    display_records = []

    for expense in filtered_expenses:

        display_records.append({
            "Expense Name": expense["Expense Name"],
            "Amount": f"Rs. {expense['Amount']:,.2f}",
            "Category": expense["Category"],
            "Date": expense["Date"]
        })

    st.dataframe(
        display_records,
        use_container_width=True,
        hide_index=True
    )

else:

    if all_expenses:
        st.warning("No expenses match your search or filters.")

    else:
        st.warning("No expense records available. Add your first expense!")


# --------------------------------
# 10. CATEGORY-WISE EXPENSE SUMMARY
# --------------------------------

st.header("📂 Category-wise Expense Summary")

if all_expenses:

    for cat in categories:

        category_total = sum(
            expense["Amount"]
            for expense in all_expenses
            if expense["Category"] == cat
        )

        st.metric(
            cat,
            f"Rs. {category_total:,.2f}"
        )

else:

    st.warning("No category data available yet.")


# --------------------------------
# 11. FINAL MESSAGE
# --------------------------------

st.success("Personal Expense Tracker is running successfully!")
