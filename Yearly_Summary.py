import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Yearly Summary",
    page_icon="📊"
)

st.title("📊 Yearly Financial Summary")

EXPENSE_FILE = "data/expenses.csv"
PLAN_FILE = "data/savings_plan.csv"

# -----------------------------
# Load Expenses
# -----------------------------
if os.path.exists(EXPENSE_FILE):
    expenses = pd.read_csv(EXPENSE_FILE)

    if not expenses.empty:
        expenses["Date"] = pd.to_datetime(expenses["Date"])
        expenses["Type"] = (
            expenses["Type"]
            .astype(str)
            .str.strip()
            .str.lower()
        )
else:
    expenses = pd.DataFrame()

# -----------------------------
# Load Savings Plan
# -----------------------------
if os.path.exists(PLAN_FILE):
    plans = pd.read_csv(PLAN_FILE)
else:
    plans = pd.DataFrame(
        columns=["Month", "Income", "Savings_Goal"]
    )

# -----------------------------
# Calculate Totals
# -----------------------------
if not plans.empty:
    total_income = plans["Income"].sum()
    total_savings_goal = plans["Savings_Goal"].sum()
else:
    total_income = 0
    total_savings_goal = 0

if not expenses.empty:
    total_expenses = expenses[
        expenses["Type"] == "expense"
    ]["Amount"].sum()
else:
    total_expenses = 0

# -----------------------------
# Month Names
# -----------------------------
months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

# -----------------------------
# Best Saving Month
# -----------------------------
best_month = "N/A"
best_saved = float("-inf")

for month in months:

    row = plans[
        plans["Month"] == month
    ]

    if row.empty:
        continue

    income = float(
        row.iloc[0]["Income"]
    )

    month_num = months.index(month) + 1

    spent = 0

    if not expenses.empty:

        spent = expenses[
            (expenses["Date"].dt.month == month_num)
            &
            (expenses["Type"] == "expense")
        ]["Amount"].sum()

    saved = income - spent

    if saved > best_saved:
        best_saved = saved
        best_month = month

# -----------------------------
# Highest Spending Month
# -----------------------------
highest_month = "N/A"
highest_spending = 0

for month in months:

    month_num = months.index(month) + 1

    spent = 0

    if not expenses.empty:

        spent = expenses[
            (expenses["Date"].dt.month == month_num)
            &
            (expenses["Type"] == "expense")
        ]["Amount"].sum()

    if spent > highest_spending:
        highest_spending = spent
        highest_month = month

# -----------------------------
# Actual Savings
# -----------------------------
actual_saved = total_income - total_expenses

# -----------------------------
# Savings Rate
# -----------------------------
if total_income > 0:
    savings_rate = (
        actual_saved / total_income
    ) * 100
else:
    savings_rate = 0

# -----------------------------
# Dashboard Metrics
# -----------------------------
col1, col2 = st.columns(2)

col1.metric(
    "💰 Total Income",
    f"₹{total_income:,.2f}"
)

col2.metric(
    "💸 Total Expenses",
    f"₹{total_expenses:,.2f}"
)

col3, col4 = st.columns(2)

col3.metric(
    "🎯 Total Savings Goal",
    f"₹{total_savings_goal:,.2f}"
)

col4.metric(
    "💵 Actual Money Saved",
    f"₹{actual_saved:,.2f}"
)

col5, col6 = st.columns(2)

col5.metric(
    "📈 Savings Rate",
    f"{savings_rate:.2f}%"
)

col6.metric(
    "🏆 Best Saving Month",
    best_month
)

st.metric(
    "📉 Highest Spending Month",
    highest_month
)

st.markdown("---")

# -----------------------------
# Financial Health Message
# -----------------------------
if savings_rate >= 30:

    st.success(
        "🌟 Excellent! Your savings rate is above 30%."
    )

elif savings_rate >= 15:

    st.info(
        "👍 Good job! You are maintaining a healthy savings rate."
    )

else:

    st.warning(
        "⚠️ Your savings rate is below 15%. Consider reducing expenses."
    )

# -----------------------------
# Summary Table
# -----------------------------
st.markdown("## 📋 Yearly Overview")

summary = pd.DataFrame({
    "Metric": [
        "Total Income",
        "Total Expenses",
        "Total Savings Goal",
        "Actual Money Saved",
        "Savings Rate",
        "Best Saving Month",
        "Highest Spending Month"
    ],
    "Value": [
        f"₹{total_income:,.2f}",
        f"₹{total_expenses:,.2f}",
        f"₹{total_savings_goal:,.2f}",
        f"₹{actual_saved:,.2f}",
        f"{savings_rate:.2f}%",
        best_month,
        highest_month
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)
# -----------------------------
# Create Yearly Summary CSV
# -----------------------------
download_df = pd.DataFrame({
    "Metric": [
        "Total Income",
        "Total Expenses",
        "Total Savings Goal",
        "Actual Money Saved",
        "Savings Rate (%)",
        "Best Saving Month",
        "Highest Spending Month"
    ],
    "Value": [
        total_income,
        total_expenses,
        total_savings_goal,
        actual_saved,
        round(savings_rate, 2),
        best_month,
        highest_month
    ]
})

# -----------------------------
# Download Button
# -----------------------------
csv = download_df.to_csv(index=False)

st.download_button(
    label="📥 Download Yearly Summary (CSV)",
    data=csv,
    file_name="yearly_financial_summary.csv",
    mime="text/csv"
)