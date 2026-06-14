import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Reports", page_icon="📄")

st.title("📄 Monthly Reports")

DATA_FILE = "data/expenses.csv"

if not os.path.exists(DATA_FILE):
    st.error("No data file found.")
    st.stop()

df = pd.read_csv(DATA_FILE)

if df.empty:
    st.info("No transactions available.")
    st.stop()

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Month selector
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

selected_month = st.selectbox("📅 Select Month", months)

# Filter data
filtered_df = df[df["Date"].dt.month == month_map[selected_month]]

st.subheader(f"Report for {selected_month}")

if filtered_df.empty:
    st.info(f"No transactions found for {selected_month}.")
else:
    income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
    expense = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Income", f"₹{income:.2f}")
    col2.metric("💸 Expense", f"₹{expense:.2f}")
    col3.metric("🏦 Balance", f"₹{balance:.2f}")

    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Monthly Report (CSV)",
        data=csv,
        file_name=f"{selected_month}_expense_report.csv",
        mime="text/csv",
    )