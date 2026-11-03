import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Expense Tracker", page_icon="💰")
st.title("💰 Personal Expense Tracker")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

with st.form("expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
        amount = st.number_input("Amount (Rs.)", min_value=1)
    with col2:
        notes = st.text_input("Notes")
        date = st.date_input("Date", datetime.now())
    
    submit = st.form_submit_button("Add Expense")
    if submit:
        st.session_state.expenses.append([str(date), category, amount, notes])
        st.success("Expense Added! ✅")

st.divider()

if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses, columns=["Date", "Category", "Amount", "Notes"])
    st.subheader("Expense History")
    st.dataframe(df, use_container_width=True)
    st.metric("Total Kharcha", f"Rs. {df['Amount'].sum()}")
else:
    st.info("No expenses yet. Add one above!")
