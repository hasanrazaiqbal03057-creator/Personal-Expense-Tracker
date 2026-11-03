import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Expense Tracker", page_icon="💰")
st.title("💰 Personal Expense Tracker")

FILE = "expenses.csv"

# File load karo
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])

# Form
with st.form("expense_form"):
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
        amount = st.number_input("Amount", min_value=1)
    with col2:
        notes = st.text_input("Notes (e.g. Biryani)")
        date = st.date_input("Date", datetime.now())
    
    submit = st.form_submit_button("Add Expense")

    if submit:
        new_data = pd.DataFrame([[date, category, amount, notes]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("Expense Added & Saved Forever! ✅")
        st.rerun()

st.divider()
st.subheader("Expense History")

if not df.empty:
    st.dataframe(df, use_container_width=True)
    st.metric("Total Kharcha", f"Rs. {df['Amount'].sum()}")
else:
    st.info("No expenses yet.")

if st.button("Clear All Data"):
    if os.path.exists(FILE):
        os.remove(FILE)
    st.rerun()
