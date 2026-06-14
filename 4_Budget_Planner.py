import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Savings Planner", page_icon="💰")

st.title("💰 Monthly Savings Planner")

EXPENSE_FILE = "data/expenses.csv"
PLAN_FILE = "data/savings_plan.csv"

# ----------------------------
# Load or create savings plan
# ----------------------------
if not os.path.exists(PLAN_FILE):
    pd.DataFrame(
        columns=["Month", "Income", "Savings_Goal"]
    ).to_csv(PLAN_FILE, index=False)

plan = pd.read_csv(PLAN_FILE)

# ----------------------------
# Load expenses
# ----------------------------
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

# ----------------------------
# Month selector
# ----------------------------
months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

selected_month = st.selectbox(
    "📅 Select Month",
    months
)

row = plan[plan["Month"] == selected_month]

# ==================================================
# FIRST TIME -> SAVE PLAN
# ==================================================
if row.empty:

    st.info("Set your income and savings goal for this month.")

    income = st.number_input(
        "💰 Monthly Income",
        min_value=0.0,
        step=500.0
    )

    saving = st.number_input(
        "🎯 Savings Goal",
        min_value=0.0,
        step=500.0
    )

    if st.button("💾 Save Plan"):

        plan.loc[len(plan)] = [
            selected_month,
            income,
            saving
        ]

        plan.to_csv(
            PLAN_FILE,
            index=False
        )

        st.success("Plan saved successfully!")
        st.rerun()

# ==================================================
# PLAN EXISTS
# ==================================================
else:

    income = float(row.iloc[0]["Income"])
    saving = float(row.iloc[0]["Savings_Goal"])

    st.subheader("📌 Current Plan")

    col1, col2 = st.columns(2)

    col1.metric("Income", f"₹{income:,.2f}")
    col2.metric("Savings Goal", f"₹{saving:,.2f}")

    st.markdown("---")

    # ----------------------------
    # Edit Plan
    # ----------------------------

    new_income = st.number_input(
        "Edit Income",
        value=income,
        step=500.0
    )

    new_saving = st.number_input(
        "Edit Savings Goal",
        value=saving,
        step=500.0
    )

    if st.button("✏️ Update Plan"):

        plan.loc[
            plan["Month"] == selected_month,
            "Income"
        ] = new_income

        plan.loc[
            plan["Month"] == selected_month,
            "Savings_Goal"
        ] = new_saving

        plan.to_csv(
            PLAN_FILE,
            index=False
        )

        st.success("Plan updated successfully!")
        st.rerun()

    # ----------------------------
    # Calculate spending
    # ----------------------------

    spending_limit = income - saving

    month_number = months.index(selected_month) + 1

    if expenses.empty:
        spent = 0

    else:
        spent = expenses[
            (expenses["Date"].dt.month == month_number)
            &
            (expenses["Type"] == "expense")
        ]["Amount"].sum()

    remaining = spending_limit - spent

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💳 Spending Limit",
        f"₹{spending_limit:,.2f}"
    )

    c2.metric(
        "💸 Total Expenses",
        f"₹{spent:,.2f}"
    )

    c3.metric(
        "🏦 Remaining",
        f"₹{remaining:,.2f}"
    )

    if spending_limit > 0:
        progress = min(spent / spending_limit, 1.0)
        st.progress(progress)

    st.markdown("---")

    # ----------------------------
    # Alerts
    # ----------------------------

    if spent > spending_limit:

        st.error(
            f"""
🚨 ALERT!

You wanted to save ₹{saving:,.2f} this month.

Income: ₹{income:,.2f}

Allowed Spending: ₹{spending_limit:,.2f}

Actual Spending: ₹{spent:,.2f}

You exceeded your spending limit by
₹{spent - spending_limit:,.2f}.
"""
        )

    elif spent >= 0.9 * spending_limit:

        st.warning(
            f"""
⚠️ Warning!

You have already used 90% of your spending limit.

Only ₹{remaining:,.2f} is left before your savings goal is affected.
"""
        )

    else:

        st.success(
            f"""
✅ Great!

Your savings goal is safe.

You can still spend ₹{remaining:,.2f}
without affecting your target savings.
"""
        )

# ----------------------------
# Saved Plans
# ----------------------------

st.markdown("---")

st.subheader("📋 Saved Monthly Plans")

st.dataframe(
    plan,
    use_container_width=True
)



#=========================
#"can i buy this product?"
#==========================

st.markdown("---")
st.subheader("🛍️ Can I Buy This?")

product_name = st.text_input("Which product do you want to purchase?")

product_price = st.number_input(
    "Product Price (₹)",
    min_value=0.0,
    step=100.0
)

if st.button("Check"):

    future_spending = spent + product_price
    remaining_budget = spending_limit - future_spending

    # Purchase fits within spending limit
    if future_spending <= spending_limit:

        st.success(
            f"""
✅ You can buy **{product_name}**.

After purchasing it:

• Total spending: ₹{future_spending:,.2f}
• Remaining spending limit: ₹{remaining_budget:,.2f}
"""
        )

    # Purchase exceeds spending limit
    else:

        extra_needed = future_spending - spending_limit

        st.error(
            f"""
❌ You don't have enough spending capacity to buy **{product_name}**.

You would exceed your spending limit by ₹{extra_needed:,.2f}.
"""
        )

        use_savings = st.radio(
            "Do you want to purchase it using your savings?",
            ["No", "Yes"],
            key="use_savings_option"
        )

        if use_savings == "Yes":

            remaining_savings = saving - extra_needed

            if remaining_savings >= 0:

                st.warning(
                    f"""
You chose to use your savings.

After purchasing:

• Savings left: ₹{remaining_savings:,.2f}
• Savings used: ₹{extra_needed:,.2f}
"""
                )

            else:

                st.error(
                    f"""
Even after using all your planned savings, you would still be short by ₹{-remaining_savings:,.2f}.

This purchase exceeds both your spending limit and your savings goal.
"""
                )

        else:

            st.success(
                f"""
👏 Good decision!

You chose not to buy **{product_name}**.

Your planned savings of ₹{saving:,.2f} remain protected.
"""
            )