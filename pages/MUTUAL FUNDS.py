import pandas as pd
import streamlit as st
import time
import yfinance as yf
import datetime
from datetime import datetime, timedelta

# def fetch_data_from_google_sheets_d(_secrets):
#     with st.spinner("Fetching data from Google Sheets..."):
#         try:
#             client = gspread.service_account_from_dict({
#                 "type": _secrets["connections"]["gsheets_d"]["type"],
#                 "project_id": _secrets["connections"]["gsheets_d"]["project_id"],
#                 "private_key_id": _secrets["connections"]["gsheets_d"]["private_key_id"],
#                 "private_key": _secrets["connections"]["gsheets_d"]["private_key"],
#                 "client_email": _secrets["connections"]["gsheets_d"]["client_email"],
#                 "client_id": _secrets["connections"]["gsheets_d"]["client_id"],
#                 "auth_uri": _secrets["connections"]["gsheets_d"]["auth_uri"],
#                 "token_uri": _secrets["connections"]["gsheets_d"]["token_uri"],
#                 "auth_provider_x509_cert_url": _secrets["connections"]["gsheets_d"]["auth_provider_x509_cert_url"],
#                 "client_x509_cert_url": _secrets["connections"]["gsheets_d"]["client_x509_cert_url"]
#             })
#             spreadsheet_key = _secrets["connections"]["gsheets_d"]["spreadsheet"]
            
#             all_data = {}
#             for cmp_symbol in _secrets["connections"]["gsheets"]["worksheets"].values():
#                 sheet = client.open_by_key(spreadsheet_key).worksheet(cmp_symbol)
#                 data = sheet.get_all_values()
#                 df = pd.DataFrame(data)
#                 df = pd.DataFrame(data[1:], columns=data[0])
#                 all_data[cmp_symbol] = df
            
#             return all_data
        
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
#             st.stop()

# def fetch_data_from_google_sheets_m(_secrets):
#     with st.spinner("Fetching data from Google Sheets..."):
#         try:
#             client = gspread.service_account_from_dict({
#                 "type": _secrets["connections"]["gsheets_m"]["type"],
#                 "project_id": _secrets["connections"]["gsheets_m"]["project_id"],
#                 "private_key_id": _secrets["connections"]["gsheets_m"]["private_key_id"],
#                 "private_key": _secrets["connections"]["gsheets_m"]["private_key"],
#                 "client_email": _secrets["connections"]["gsheets_m"]["client_email"],
#                 "client_id": _secrets["connections"]["gsheets_m"]["client_id"],
#                 "auth_uri": _secrets["connections"]["gsheets_m"]["auth_uri"],
#                 "token_uri": _secrets["connections"]["gsheets_m"]["token_uri"],
#                 "auth_provider_x509_cert_url": _secrets["connections"]["gsheets_m"]["auth_provider_x509_cert_url"],
#                 "client_x509_cert_url": _secrets["connections"]["gsheets_m"]["client_x509_cert_url"]
#             })
#             spreadsheet_key = _secrets["connections"]["gsheets_m"]["spreadsheet"]
            
#             all_data = {}
#             for cmp_symbol in _secrets["connections"]["gsheets"]["worksheets"].values():
#                 sheet = client.open_by_key(spreadsheet_key).worksheet(cmp_symbol)
#                 data = sheet.get_all_values()
#                 df = pd.DataFrame(data)
#                 df = pd.DataFrame(data[1:], columns=data[0])
#                 all_data[cmp_symbol] = df
            
#             return all_data
        
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
#             st.stop()

# def fetch_data_from_google_sheets_h(_secrets):
#     with st.spinner("Fetching data from Google Sheets..."):
#         try:
#             client = gspread.service_account_from_dict({
#                 "type": _secrets["connections"]["gsheets_h"]["type"],
#                 "project_id": _secrets["connections"]["gsheets_h"]["project_id"],
#                 "private_key_id": _secrets["connections"]["gsheets_h"]["private_key_id"],
#                 "private_key": _secrets["connections"]["gsheets_h"]["private_key"],
#                 "client_email": _secrets["connections"]["gsheets_h"]["client_email"],
#                 "client_id": _secrets["connections"]["gsheets_h"]["client_id"],
#                 "auth_uri": _secrets["connections"]["gsheets_h"]["auth_uri"],
#                 "token_uri": _secrets["connections"]["gsheets_h"]["token_uri"],
#                 "auth_provider_x509_cert_url": _secrets["connections"]["gsheets_h"]["auth_provider_x509_cert_url"],
#                 "client_x509_cert_url": _secrets["connections"]["gsheets_h"]["client_x509_cert_url"]
#             })
#             spreadsheet_key = _secrets["connections"]["gsheets_h"]["spreadsheet"]
            
#             all_data = {}
#             for cmp_symbol in _secrets["connections"]["gsheets"]["worksheets"].values():
#                 sheet = client.open_by_key(spreadsheet_key).worksheet(cmp_symbol)
#                 data = sheet.get_all_values()
#                 df = pd.DataFrame(data)
#                 df = pd.DataFrame(data[1:], columns=data[0])
#                 all_data[cmp_symbol] = df
            
#             return all_data
        
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
#             st.stop()

# def fetch_data_from_google_sheets(_secrets):
#     with st.spinner("Fetching data from Google Sheets..."):
#         try:
#             client = gspread.service_account_from_dict({
#                 "type": _secrets["connections"]["gsheets"]["type"],
#                 "project_id": _secrets["connections"]["gsheets"]["project_id"],
#                 "private_key_id": _secrets["connections"]["gsheets"]["private_key_id"],
#                 "private_key": _secrets["connections"]["gsheets"]["private_key"],
#                 "client_email": _secrets["connections"]["gsheets"]["client_email"],
#                 "client_id": _secrets["connections"]["gsheets"]["client_id"],
#                 "auth_uri": _secrets["connections"]["gsheets"]["auth_uri"],
#                 "token_uri": _secrets["connections"]["gsheets"]["token_uri"],
#                 "auth_provider_x509_cert_url": _secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
#                 "client_x509_cert_url": _secrets["connections"]["gsheets"]["client_x509_cert_url"]
#             })
#             spreadsheet_key = _secrets["connections"]["gsheets"]["spreadsheet"]
            
#             all_data = {}
#             for cmp_symbol in _secrets["connections"]["gsheets"]["worksheets"].values():
#                 sheet = client.open_by_key(spreadsheet_key).worksheet(cmp_symbol)
#                 data = sheet.get_all_values()
#                 df = pd.DataFrame(data)
#                 df = pd.DataFrame(data[1:], columns=data[0])
#                 all_data[cmp_symbol] = df
            
#             return all_data
        
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
#             st.stop()


# user = st.selectbox("Select User",options = [None,'Amit','Deepti','Mridul','Hemank'])
# if 'all_data' not in st.session_state:
#     st.session_state.all_data = 0
# if 'user' not in st.session_state:
#     st.session_state.user = 0
# if user == 'Amit':
#     all_data = fetch_data_from_google_sheets(st.session_state.secrets)
#     st.session_state.all_data = all_data
#     st.session_state.user = 'Amit'
# elif user == 'Deepti':
#     all_data_d = fetch_data_from_google_sheets_d(st.session_state.secrets)
#     st.session_state.all_data = all_data_d
#     st.session_state.user = 'Deepti'
# elif user == 'Mridul':
#     all_data_m = fetch_data_from_google_sheets_m(st.session_state.secrets)
#     st.session_state.all_data = all_data_m
#     st.session_state.user = 'Mridul'
# elif user == 'Hemank':
#     all_data_h = fetch_data_from_google_sheets_h(st.session_state.secrets)
#     st.session_state.all_data = all_data_h
#     st.session_state.user = 'Hemank'

def highlight_gain_condition(s):
    if s.name == 'Down_PD%':
        return s.apply(lambda x: highlight_single_gain(x))
    else:
        return [''] * len(s)
def highlight_single_gain(value):
    if value < 0:
        color = 'rgba(255, 0, 0, 0.8)'  # Red with 50% opacity
    elif 0 <= value <= 5:
        color = 'rgba(255, 255, 0, 0.7)'  # Yellow with 50% opacity
    elif 5 < value:
        color = 'rgba(63, 255, 0,1)'  # Green with 50% opacity
    else:
        color = ''  # No highlighting if not in specified ranges
    return 'background-color: %s' % color

def get_cmp_price(cmp_symbol):
    
    try:
        cmp_data = yf.Ticker(cmp_symbol)
        cmp_price = cmp_data.history(period="1d")["Close"].iloc[-1]
        return cmp_price
    except Exception as e:
        st.error(f"Failed to fetch cmp price: {e}")
        return None
    
def get_prev_price(cmp_symbol):
    try:
        cmp_data = yf.Ticker(cmp_symbol)
        cmp_price = cmp_data.history(period="2d")["Close"].iloc[-2]
        return cmp_price
    except Exception as e:
        st.error(f"Failed to fetch prev day price: {e}")
        return None

st.title("Mutual Funds")

mutual_funds = {"0P0001KR2R":"Nifty Smallcap 250","0P0001LMCR":"Nifty Midcap 150","0P0001MSVD":"Navi Nifty 50","0P0001ODHD": "Navi US Total Stock Market","0P0001OK0H": "Navi NASDAQ 100"}			

st.session_state.last_analysis_time = time.time() - 110
summary_mf = st.empty()
while True:
    summary = pd.DataFrame(columns=['Mutual Fund', 'Down_PD%', 'CMP','Prev_day Price'])
    if time.time() - st.session_state.last_analysis_time > 100:
        for mf in mutual_funds.keys():
            time.sleep(1)
            cmp = get_cmp_price(mf+".BO")
            prev = get_prev_price(mf+".BO")
            down_pd = round((cmp - prev)/prev * 100,2)
            if down_pd < 0:
                color = 'rgba(255, 0, 0, 0.8)'
            elif down_pd >= 0 and down_pd < 5:
                color = 'rgba(255, 255, 0, 0.7)'
            else:
                color = 'rgba(63, 255, 0,1)'
            new_res = pd.DataFrame({'Mutual Fund': [mutual_funds[mf]], 'Down_PD%': [down_pd],'CMP': [cmp],'Prev_day Price': [prev]})
            summary = pd.concat([summary, new_res], ignore_index=True)
        format_dict1 = {'Down_PD%': '{:.2f}', 'CMP': '{:.2f}', 'Prev_day Price': '{:.2f}'}
        summary_styled = summary.sort_values('Down_PD%').style.format(format_dict1).apply(highlight_gain_condition, subset=['Down_PD%'], axis=0)
        summary_mf.dataframe(summary_styled)
