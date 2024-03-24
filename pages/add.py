import gspread
import streamlit as st
from datetime import datetime
import datetime

secrets = st.session_state.secrets

try:
    all_data = st.session_state.all_data
except:
    st.error("Please run the app from the main page.")
selected_tab = st.selectbox("Select ETF", options=list(all_data.keys()), key='ETF')
price = st.number_input("Price", value=0.0, key='Price')
qty = st.number_input("Qty.", value=0.0, key='Qty.')

if st.button("Add") and price > 0 and qty > 0:
    with st.spinner("Adding..."):
        if st.session_state.user == 'Amit':
            try:
                client = gspread.service_account_from_dict({
                    "type": secrets["connections"]["gsheets"]["type"],
                    "project_id": secrets["connections"]["gsheets"]["project_id"],
                    "private_key_id": secrets["connections"]["gsheets"]["private_key_id"],
                    "private_key": secrets["connections"]["gsheets"]["private_key"],
                    "client_email": secrets["connections"]["gsheets"]["client_email"],
                    "client_id": secrets["connections"]["gsheets"]["client_id"],
                    "auth_uri": secrets["connections"]["gsheets"]["auth_uri"],
                    "token_uri": secrets["connections"]["gsheets"]["token_uri"],
                    "auth_provider_x509_cert_url": secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
                    "client_x509_cert_url": secrets["connections"]["gsheets"]["client_x509_cert_url"]
                })
                spreadsheet_key = secrets["connections"]["gsheets"]["spreadsheet"]
                worksheet_name = secrets["connections"]["gsheets"]["worksheets"][selected_tab]
                sheet = client.open_by_key(spreadsheet_key).worksheet(worksheet_name)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.stop()
        else:
            try:
                client = gspread.service_account_from_dict({
                    "type": secrets["connections"]["gsheets_d"]["type"],
                    "project_id": secrets["connections"]["gsheets_d"]["project_id"],
                    "private_key_id": secrets["connections"]["gsheets_d"]["private_key_id"],
                    "private_key": secrets["connections"]["gsheets_d"]["private_key"],
                    "client_email": secrets["connections"]["gsheets_d"]["client_email"],
                    "client_id": secrets["connections"]["gsheets_d"]["client_id"],
                    "auth_uri": secrets["connections"]["gsheets_d"]["auth_uri"],
                    "token_uri": secrets["connections"]["gsheets_d"]["token_uri"],
                    "auth_provider_x509_cert_url": secrets["connections"]["gsheets_d"]["auth_provider_x509_cert_url"],
                    "client_x509_cert_url": secrets["connections"]["gsheets_d"]["client_x509_cert_url"]
                })
                spreadsheet_key = secrets["connections"]["gsheets_d"]["spreadsheet"]
                worksheet_name = secrets["connections"]["gsheets"]["worksheets"][selected_tab]
                sheet = client.open_by_key(spreadsheet_key).worksheet(worksheet_name)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.stop()
    row_data = [str(datetime.date.today()), qty, price]
    sheet.append_row(row_data)
    st.success("Added successfully!")