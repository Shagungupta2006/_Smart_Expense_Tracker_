import streamlit as st

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Smart Expense Tracker")
st.subheader("Manage your income and expenses efficiently")

st.markdown("---")

st.markdown("""
### 📌 Features
- ➕ Add Income & Expenses
- 📊 Dashboard with Summary
- 📈 Expense Analytics & Charts
- 🎯 Budget Planning
- 📄 Download Reports
- ✏️ Edit & Delete Transactions
- 📋 Yearly Dashboard
- 🔎 Search Expenses
- 🛍️ Can I Buy This?

👈 **Use the sidebar to navigate between pages.**
""")

st.info("Start by opening **'Add Transaction'** from the sidebar and entering your first record.")