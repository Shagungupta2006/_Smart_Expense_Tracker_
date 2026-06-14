import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Add Transaction", page_icon="➕")

st.title("➕ Add Transaction")

DATA_FILE = "data/expenses.csv"

# Create CSV if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(
        columns=[
            "Date",
            "Type",
            "Category",
            "Amount",
            "Description",
            "Payment Method",
        ]
    )
    df.to_csv(DATA_FILE, index=False)

with st.form("transaction_form"):
    trans_date = st.date_input("Date", value=date.today())

    trans_type = st.selectbox(
        "Transaction Type",
        ["Expense", "Income"]
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Entertainment",
            "Education",
            "Health",
            "Salary",
            "Other",
        ]
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=1.0
    )

    description = st.text_input("Description")

    payment = st.selectbox(
        "Payment Method",
        ["Cash", "UPI", "Card", "Bank Transfer"]
    )

    submitted = st.form_submit_button("Save Transaction")

if submitted:
    new_data = pd.DataFrame(
        [[
            str(trans_date),
            trans_type,
            category,
            amount,
            description,
            payment
        ]],
        columns=[
            "Date",
            "Type",
            "Category",
            "Amount",
            "Description",
            "Payment Method",
        ],
    )

    existing = pd.read_csv(DATA_FILE)
    updated = pd.concat([existing, new_data], ignore_index=True)
    updated.to_csv(DATA_FILE, index=False)

    st.success("✅ Transaction saved successfully!")