# app/main.py

import streamlit as st
import pandas as pd
import os

# Optional: Load types and wattages from CSV if exists, else use default dict
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'types_watts.csv')
if os.path.exists(DATA_PATH):
    types_df = pd.read_csv(DATA_PATH)
    type_watts = {row['Type']: row['Watts'] for _, row in types_df.iterrows()}
    type_list = types_df['Type'].tolist()
else:
    type_watts = {
        'Refrigerator': 120,
        'LED Bulb': 9,
        'TV': 80,
        'Fan': 50,
        'Laptop': 60,
        'Washing Machine': 500,
        'Air Conditioner': 1500,
        'Custom': None
    }
    type_list = list(type_watts.keys())

st.set_page_config(page_title="Electricity Usage Calculator", layout="wide")
st.title("Monthly Electricity Usage Calculator")

# Session state to store items
if 'data' not in st.session_state:
    st.session_state['data'] = []

# Data entry form
with st.form(key="entry_form"):
    col1, col2, col3, col4 = st.columns(4)
    item = col1.text_input("Item Name")
    type_choice = col2.selectbox("Type", type_list)
    default_watts = type_watts[type_choice] if type_watts[type_choice] is not None else 0
    watts = col3.number_input("Watts", min_value=1, value=default_watts)
    hours = col4.number_input("Hours per day", min_value=0.0, value=1.0)
    submitted = st.form_submit_button("Add Item")

    if submitted and item:
        kwh = (watts * hours * 30) / 1000
        st.session_state['data'].append({
            'Item': item,
            'Type': type_choice,
            'Watts': watts,
            'Hours per day': hours,
            'Total KWH for a month': round(kwh, 2)
        })

df = pd.DataFrame(st.session_state['data'])
st.write("### Items List")
st.dataframe(df, use_container_width=True)

if not df.empty:
    total = df['Total KWH for a month'].sum()
    st.success(f"### Total Monthly Usage: {total:.2f} KWH")

    csv = df.to_csv(index=False).encode()
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="electricity_usage.csv",
        mime="text/csv"
    )
