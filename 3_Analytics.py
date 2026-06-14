import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Analytics", page_icon="📈")

st.title("📈 Monthly Expense Analytics")

DATA_FILE = "data/expenses.csv"

if not os.path.exists(DATA_FILE):
    st.warning("No data found.")
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

# Filter selected month
monthly_df = df[df["Date"].dt.month == month_map[selected_month]]

# Keep only expenses for chart
expense_df = monthly_df[monthly_df["Type"] == "Expense"]

if expense_df.empty:
    st.info(f"No expense data available for {selected_month}.")
    st.stop()

# Category-wise total
category_sum = expense_df.groupby("Category")["Amount"].sum()

st.subheader(f"Expense Breakdown - {selected_month}")

fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(
    category_sum,
    labels=category_sum.index,
    autopct="%1.1f%%",
)
ax.set_title(f"{selected_month} Expenses")

st.pyplot(fig)

st.subheader("Summary")

st.write(f"**Total Expenses:** ₹{expense_df['Amount'].sum():.2f}")
st.write(f"**Number of Transactions:** {len(expense_df)}")

st.subheader("Transactions")

st.dataframe(
    expense_df.sort_values(by="Date", ascending=False),
    use_container_width=True
)