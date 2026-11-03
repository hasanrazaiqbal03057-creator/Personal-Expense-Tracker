import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")
st.title("💰 Personal Expense Tracker")
st.write("Manage Your Daily Expenses")

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

with st.sidebar:
    st.header("Search & Filters")
    st.text_input("Search Expense")
    st.selectbox("Select Category", ["All", "Food", "Transport", "Shopping", "Bills", "Fees", "Other"])
    st.slider("Filter by Amount (Rs.)", 0.0, 1000.0, (0.0, 1000.0))

st.header("Add New Expense")
c1, c2 = st.columns(2)
with c1:
    amount = st.number_input("Amount (PKR)", min_value=1.0, step=10.0)
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Fees", "Other"])
with c2:
    desc = st.text_input("Description")
    date = st.date_input("Date", datetime.now())

if st.button("Add Expense", type="primary"):
    st.session_state.expenses.append({"Amount": amount, "Category": category, "Description": desc, "Date": str(date)})
    st.success("Added!")
    st.rerun()

st.header("Dashboard Summary")
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    total = df["Amount"].sum()
    st.write(f"**Total Spent: Rs. {total}**")
    st.write(f"**Total Records: {len(df)}**")
    st.subheader("Expense Records")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No expenses yet. Add from above!")
    st.subheader("Expense Records")
    st.write("No data")
