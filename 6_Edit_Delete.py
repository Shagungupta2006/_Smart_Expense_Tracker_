import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Edit & Delete", page_icon="✏️")

st.title("✏️ Edit & Delete Transactions")

DATA_FILE = "data/expenses.csv"

# Check if file exists
if not os.path.exists(DATA_FILE):
    st.error("No transactions found.")
    st.stop()

# Read data
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

# Filter by selected month
filtered_df = df[df["Date"].dt.month == month_map[selected_month]]

st.subheader(f"Transactions for {selected_month}")

if filtered_df.empty:
    st.info(f"No transactions found for {selected_month}.")
    st.stop()

# Show transactions
display_df = filtered_df.copy()
display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

st.dataframe(display_df, use_container_width=True)

# Select transaction
row_index = st.selectbox(
    "Select Transaction",
    options=filtered_df.index,
    format_func=lambda i: (
        f"{df.loc[i, 'Date'].strftime('%Y-%m-%d')} | "
        f"{df.loc[i, 'Category']} | ₹{df.loc[i, 'Amount']}"
    )
)

row = df.loc[row_index]

st.markdown("---")
st.subheader("Edit Transaction")

new_date = st.date_input("Date", value=row["Date"])

new_type = st.selectbox(
    "Type",
    ["Expense", "Income"],
    index=0 if row["Type"] == "Expense" else 1
)

new_category = st.text_input(
    "Category",
    value=str(row["Category"])
)

new_amount = st.number_input(
    "Amount",
    min_value=0.0,
    value=float(row["Amount"])
)

new_description = st.text_input(
    "Description",
    value=str(row["Description"])
)

new_payment = st.text_input(
    "Payment Method",
    value=str(row["Payment Method"])
)

col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Update"):
        df.loc[row_index, "Date"] = str(new_date)
        df.loc[row_index, "Type"] = new_type
        df.loc[row_index, "Category"] = new_category
        df.loc[row_index, "Amount"] = new_amount
        df.loc[row_index, "Description"] = new_description
        df.loc[row_index, "Payment Method"] = new_payment

        df.to_csv(DATA_FILE, index=False)

        st.success("✅ Transaction updated successfully!")
        st.rerun()

with col2:
    if st.button("🗑️ Delete"):
        df = df.drop(row_index).reset_index(drop=True)
        df.to_csv(DATA_FILE, index=False)

        st.success("✅ Transaction deleted successfully!")
        st.rerun()