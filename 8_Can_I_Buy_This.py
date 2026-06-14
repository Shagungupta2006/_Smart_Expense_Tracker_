import streamlit as st
import pandas as pd

st.set_page_config(page_title="Can I Buy This?", page_icon="🛍️")

# ==========================
# Load Files
# ==========================
PLAN_FILE = "data/savings_plan.csv"
EXPENSE_FILE = "data/expenses.csv"

plans = pd.read_csv(PLAN_FILE)
expenses = pd.read_csv(EXPENSE_FILE)

expenses["Date"] = pd.to_datetime(expenses["Date"])
expenses["Type"] = (
    expenses["Type"]
    .astype(str)
    .str.lower()
    .str.strip()
)

months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

st.title("🛍️ Can I Buy This?")

selected_month = st.selectbox(
    "📅 Select Month",
    months
)

row = plans[plans["Month"] == selected_month]

if row.empty:
    st.warning("No savings plan found for this month.")
    st.stop()

income = float(row.iloc[0]["Income"])
saving = float(row.iloc[0]["Savings_Goal"])

month_number = months.index(selected_month) + 1

spent = expenses[
    (expenses["Date"].dt.month == month_number)
    &
    (expenses["Type"] == "expense")
]["Amount"].sum()

spending_limit = income - saving

st.info(f"""
Income: ₹{income:,.2f}

Savings Goal: ₹{saving:,.2f}

Current Expenses: ₹{spent:,.2f}

Available Spending Limit: ₹{max(spending_limit - spent, 0):,.2f}
""")

# ==========================
# Product Input
# ==========================

product_name = st.text_input(
    "🛒 Which product do you want to purchase?"
)

product_price = st.number_input(
    "💰 Product Price",
    min_value=0.0,
    step=100.0
)

# Remember check state
if "checked" not in st.session_state:
    st.session_state.checked = False

if st.button("🔍 Check"):
    st.session_state.checked = True

# ==========================
# Result
# ==========================

if st.session_state.checked:

    future_spending = spent + product_price

    if future_spending <= spending_limit:

        money_left = spending_limit - future_spending

        st.success(f"""
✅ You can buy **{product_name}**.

After purchasing:

• Total Expenses: ₹{future_spending:,.2f}

• Spending Limit Left: ₹{money_left:,.2f}

🎉 Your savings goal will remain safe.
""")

    else:

        extra_needed = future_spending - spending_limit

        st.error(f"""
❌ You don't have enough spending limit.

You need an extra ₹{extra_needed:,.2f}.

Do you want to buy it using your savings?
""")

        col1, col2 = st.columns(2)

        with col1:

            if st.button("💰 Yes, Use Savings"):

                remaining_savings = saving - extra_needed

                if remaining_savings >= 0:

                    st.warning(f"""
✅ Purchase Successful!

Product: {product_name}

Savings Used: ₹{extra_needed:,.2f}

Savings Remaining: ₹{remaining_savings:,.2f}
""")

                else:

                    shortage = abs(remaining_savings)

                    st.error(f"""
❌ Even after using all your savings,
you are still short by ₹{shortage:,.2f}.
""")

        with col2:

            if st.button("❌ No, Don't Buy"):

                st.success(f"""
👏 Great decision!

You chose not to buy **{product_name}**.

You protected your planned savings of ₹{saving:,.2f}.
""")