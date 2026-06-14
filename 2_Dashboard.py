import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 Monthly Dashboard")

DATA_FILE = "data/expenses.csv"

# Check if file exists
if not os.path.exists(DATA_FILE):
    st.warning("No transactions found.")
    st.stop()

# Read CSV
df = pd.read_csv(DATA_FILE)

# Check if empty
if df.empty:
    st.info("No data available.")
    st.stop()

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Month names
months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

month_map = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}

# Month selector
selected_month = st.selectbox("📅 Select Month", months)

# Filter data for selected month
filtered_df = df[df["Date"].dt.month == month_map[selected_month]]

# Calculate totals
income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
expense = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
balance = income - expense

# Show metrics
col1, col2, col3 = st.columns(3)

col1.metric("💰 Income", f"₹{income:.2f}")
col2.metric("💸 Expense", f"₹{expense:.2f}")
col3.metric("🏦 Balance", f"₹{balance:.2f}")

st.markdown("---")

st.subheader(f"📋 Transactions for {selected_month}")

if filtered_df.empty:
    st.info(f"No transactions found for {selected_month}.")
else:
    # Sort newest first
    filtered_df = filtered_df.sort_values(by="Date", ascending=False)

    # Show date in readable format
    filtered_df["Date"] = filtered_df["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(filtered_df, use_container_width=True)