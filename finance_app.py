import streamlit as st
import pandas as pd
import plotly.express as px
import oracledb
from datetime import datetime

oracledb.init_oracle_client(lib_dir=r"C:\oraclexe\app\oracle\product\11.2.0\server\bin")
def get_database_connection():
    connection = oracledb.connect(
    user="SYSTEM",
    password="10CGPAkasapna",
    host="localhost",
    port=1521,       
    service_name="XE"
)
    return connection

def main():
    st.title("Personal Finance Manager")
    
    page = st.sidebar.selectbox(
        "Select Page",
        ["Dashboard", "Add Transaction", "View Transactions"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Add Transaction":
        add_transaction_page()
    else:
        view_transactions()

def show_dashboard():
    conn = get_database_connection()
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN type = 'INCOME' THEN amount ELSE 0 END) as total_income,
            SUM(CASE WHEN type = 'EXPENSE' THEN amount ELSE 0 END) as total_expense
        FROM transactions
        WHERE date_time >= ADD_MONTHS(SYSDATE, -1)
    """)
    income, expense = cursor.fetchone()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Income", f"₹{income:,.2f}")
    col2.metric("Monthly Expenses", f"₹{expense:,.2f}")
    col3.metric("Net Savings", f"₹{income - expense:,.2f}")
    
    cursor.execute("""
        SELECT category, SUM(amount) as total
        FROM transactions
        WHERE type = 'EXPENSE'
        GROUP BY category
    """)
    df_categories = pd.DataFrame(cursor.fetchall(), columns=['Category', 'Amount'])
    
    fig = px.pie(df_categories, values='Amount', names='Category', 
                 title='Expense Distribution by Category')
    st.plotly_chart(fig)

def add_transaction_page():
    st.header("Add New Transaction")
    
    amount = st.number_input("Amount", min_value=0.0)
    category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Entertainment", "Other"])
    description = st.text_input("Description")
    trans_type = st.selectbox("Type", ["INCOME", "EXPENSE"])
    
    if st.button("Add Transaction"):
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.callproc("add_transaction", [amount, category, description, trans_type])
        conn.commit()
        st.success("Transaction added successfully!")

def view_transactions():
    st.header("Transaction History")
    
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date_time, amount, category, description, type
        FROM transactions
        ORDER BY date_time DESC
    """)
    
    df = pd.DataFrame(cursor.fetchall(), 
                     columns=['Date', 'Amount', 'Category', 'Description', 'Type'])
    st.dataframe(df)

if __name__ == "__main__":
    main()