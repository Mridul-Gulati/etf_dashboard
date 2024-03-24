import gspread
import streamlit as st
from datetime import datetime
import pandas as pd
secrets = st.session_state.secrets
try:
    all_data = st.session_state.all_data
except:
    st.error("Please run the app from the main page.")
selected_tab = st.selectbox("Select ETF", options=list(all_data.keys()), key='ETF')
row_num = st.number_input("Number of rows to be deleted", value=0.0, key='Row Number')
if st.session_state.user == 'Amit':
    spreadsheet_id = secrets["connections"]["gsheets"]["spreadsheet"]
else:
    spreadsheet_id = secrets["connections"]["gsheets_d"]["spreadsheet"]
def overwrite_worksheet_with_df(worksheet, df):
    try:
        worksheet.clear()

        values = df.values.tolist()

        worksheet.update("A1", values)
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Main code
if st.button("Delete") and row_num > 0:
    with st.spinner("Deleting..."):
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

            # Open the spreadsheet
            spreadsheet = client.open_by_key(spreadsheet_id)

            worksheet = spreadsheet.worksheet(selected_tab)

            # Get all values as DataFrame
            df = pd.DataFrame(worksheet.get_all_values(), columns=None)

            df = df[:-int(row_num)]

            overwrite_worksheet_with_df(worksheet, df)

            # Provide success message
            st.success(f"Deleted {row_num} rows successfully from the bottom of the worksheet '{selected_tab}'.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        