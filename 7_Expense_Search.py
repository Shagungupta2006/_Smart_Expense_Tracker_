import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Expense Search",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Expense Search & Spending Analysis")

EXPENSE_FILE = "data/expenses.csv"

# -----------------------------------
# Check File
# -----------------------------------
if not os.path.exists(EXPENSE_FILE):
    st.error("❌ expenses.csv not found inside data folder.")
    st.stop()

df = pd.read_csv(EXPENSE_FILE)

if df.empty:
    st.warning("No expense data available.")
    st.stop()

# -----------------------------------
# Prepare Data
# -----------------------------------
df["Date"] = pd.to_datetime(df["Date"])

df["Type"] = (
    df["Type"]
    .astype(str)
    .str.lower()
    .str.strip()
)

expense_df = df[df["Type"] == "expense"].copy()

expense_df["Month"] = expense_df["Date"].dt.strftime("%B")

months_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

# =====================================================
# SEARCH BY CATEGORY
# =====================================================

st.subheader("🔎 Search Expenses")

categories = sorted(expense_df["Category"].unique())

selected_category = st.selectbox(
    "Select Category",
    ["All"] + categories
)

if selected_category == "All":
    filtered = expense_df
else:
    filtered = expense_df[
        expense_df["Category"] == selected_category
    ]

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# MONTH OF HIGHEST SPENDING
# =====================================================

st.markdown("---")

month_total = (
    expense_df
    .groupby("Month")["Amount"]
    .sum()
)

month_total = month_total.reindex(months_order).fillna(0)

highest_month = month_total.idxmax()
highest_amount = month_total.max()

col1, col2 = st.columns(2)

col1.metric(
    "📅 Highest Spending Month",
    highest_month
)

col2.metric(
    "💸 Amount",
    f"₹{highest_amount:,.2f}"
)

# =====================================================
# HIGHEST SPENDING CATEGORY
# =====================================================

category_total = (
    expense_df
    .groupby("Category")["Amount"]
    .sum()
)

top_category = category_total.idxmax()
top_amount = category_total.max()

col1, col2 = st.columns(2)

col1.metric(
    "🛒 Highest Spending Category",
    top_category
)

col2.metric(
    "💰 Amount",
    f"₹{top_amount:,.2f}"
)

# =====================================================
# TOP 5 CATEGORIES
# =====================================================

st.markdown("---")

st.subheader("🏆 Top 5 Expense Categories")

top5 = (
    category_total
    .sort_values(ascending=False)
    .head(5)
)

st.dataframe(
    top5.reset_index().rename(
        columns={
            "Category": "Category",
            "Amount": "Total Amount"
        }
    ),
    use_container_width=True,
    hide_index=True
)

# =====================================================
# HIGHEST CATEGORY FOR EACH MONTH
# =====================================================

st.markdown("---")
st.subheader("📊 Highest Spending Category Month-wise")

result = []

for month in months_order:

    temp = expense_df[
        expense_df["Month"] == month
    ]

    if temp.empty:
        continue

    grp = (
        temp
        .groupby("Category")["Amount"]
        .sum()
    )

    result.append({
        "Month": month,
        "Highest Spending Category": grp.idxmax(),
        "Amount": grp.max()
    })

summary_df = pd.DataFrame(result)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# BAR GRAPH
# =====================================================

st.subheader("📈 Highest Spending Amount by Month")

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    summary_df["Month"],
    summary_df["Amount"]
)

ax.set_xlabel("Month")
ax.set_ylabel("Amount (₹)")
ax.set_title("Highest Spending Category Amount by Month")

plt.xticks(rotation=45)

st.pyplot(fig)

# =====================================================
# BIGGEST SINGLE EXPENSE
# =====================================================

st.markdown("---")

st.subheader("💥 Biggest Single Expense")

largest = expense_df.loc[
    expense_df["Amount"].idxmax()
]

st.success(
    f"""
📅 Date: {largest['Date'].date()}

🛒 Category: {largest['Category']}

💰 Amount: ₹{largest['Amount']:,.2f}
"""
)

# =====================================================
# AUTOMATIC OVERSPENDING DETECTION
# =====================================================

st.markdown("---")

st.subheader("🚨 Automatic Overspending Detection")

average = expense_df["Amount"].mean()

overspend = expense_df[
    expense_df["Amount"] >= average * 2
]

if overspend.empty:

    st.success("✅ No unusually high expenses detected.")

else:

    st.error("⚠️ Unusually high expense entries detected!")

    st.dataframe(
        overspend[
            [
                "Date",
                "Category",
                "Amount"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# DOWNLOAD CSV
# =====================================================

st.markdown("---")

csv = summary_df.to_csv(index=False)

st.download_button(
    label="📥 Download Monthly Expense Summary",
    data=csv,
    file_name="monthly_expense_summary.csv",
    mime="text/csv"
)