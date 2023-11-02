import streamlit as st
import pandas as pd
import numpy as np
from google.cloud import firestore

add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)
st.title('Farmers Market Data')
st.metric(label="Debit", value="₹ 5000", delta="₹ 200")
st.metric(label="loan", value="₹ 5000", delta="₹ 200")
st.markdown("<h1 style='text-align: center; color: white;'>My Dashboard</h1>", unsafe_allow_html=True)



db = firestore.Client.from_service_account_json("firestore-key.json")


users_ref = db.collection("users")

data_list = []

all_expenses = []

for user_doc in users_ref.stream():
    user_data = user_doc.to_dict()
    user_id = user_data.get('uid')  

    # Create a reference to the 'expense' subcollection for the current user.
    expense_collection_ref = users_ref.document(user_id).collection('expense')

    # Iterate through the 'expense' subcollection for the current user.
    user_expenses = []

    for expense_doc in expense_collection_ref.stream():
        expense_data = expense_doc.to_dict()
        user_expenses.append(expense_data)

    # Append the user's expenses to the list of all expenses.
    all_expenses.extend(user_expenses)

exp_data = []
in_data = []
for expense in all_expenses:
    if (expense.get('isIncome') == 'Income'):
        in_data.append(expense)
    else :
        exp_data.append(expense)
    # st.write(expense)
   
    # st.write(in_data)

# st.write(exp_data)
st.write(in_data)
exp_list = [item["amount"] for item in exp_data]
user_list = [item["id"] for item in exp_data]
ch_dt = pd.DataFrame(exp_list)
st.line_chart(ch_dt)