import pandas as pd
import streamlit as st
import time
import yfinance as yf
from datetime import datetime
import toml
import math
import datetime
from datetime import timedelta
# from app import fetch_data_from_google_sheets, fetch_data_from_google_sheets_d

title = st.empty()
res_place = st.empty()
res = st.session_state.all_data["MAFANG"]
secrets = st.session_state.secrets
if 'res' not in st.session_state:
    st.session_state.res = res
st.session_state.res = res
def highlight_gain_condition(s):
    if s.name == 'Gain%':
        return s.apply(lambda x: highlight_single_gain(x))
    else:
        return [''] * len(s)

def highlight_single_gain(value):
    if value < 0:
        color = 'rgba(255, 0, 0, 0.8)'  # Red with 50% opacity
    elif 0 <= value <= 2:
        color = 'rgba(255, 255, 0, 0.7)'  # Yellow with 50% opacity
    elif 2 < value <= 3:
        color = 'rgba(255, 140, 0, 1)'  # Orange with 50% opacity
    elif 3 < value:
        color = 'rgba(63, 255, 0,1)'  # Green with 50% opacity
    else:
        color = ''  # No highlighting if not in specified ranges
    return 'background-color: %s' % color

def get_cmp_price(cmp_symbol):
    try:
        cmp_data = yf.Ticker(cmp_symbol+".NS")
        cmp_price = cmp_data.history(period="1d")["Close"].iloc[-1]
        return cmp_price
    except Exception as e:
        st.error(f"Failed to fetch cmp price: {e}")
        return None
if 'Price' in st.session_state.res.columns and 'Qty.' in st.session_state.res.columns:
    st.session_state.res['Price'] = st.session_state.res['Price'].str.replace(',', '').astype(float) if st.session_state.res['Price'].dtype == 'object' else st.session_state.res['Price']
    st.session_state.res['Qty.'] = st.session_state.res['Qty.'].str.replace(',', '').astype(float) if st.session_state.res['Qty.'].dtype == 'object' else st.session_state.res['Qty.']
    st.session_state.res['Buy Value'] = st.session_state.res['Price'] * st.session_state.res['Qty.']
    st.session_state.res['Age'] = (datetime.datetime.now() - pd.to_datetime(res['Date'])).dt.days
else:
    st.error("Columns 'Price' and/or 'Qty.' not found in the DataFrame.")

while True:
    if time.time() - st.session_state.last_analysis_time >= 10:
        st.session_state.last_analysis_time = time.time()

        st.session_state.res['CMP'] = round(get_cmp_price(secrets["connections"]["gsheets"]["worksheets"]['MAFANG']),2)
        st.session_state.res['Current Value'] = st.session_state.res['Qty.'] * st.session_state.res['CMP']
        st.session_state.res['Gain%'] = round(((res['Current Value'] - st.session_state.res['Buy Value']) / st.session_state.res['Buy Value']) * 100,2)
        st.session_state.res['Amount'] = st.session_state.res['Current Value'] - st.session_state.res['Buy Value']
        # st.session_state.res = res
        title.title('')
        title.title(f'Data for MAFANG')
        res_place.text('')
        res_rounded = st.session_state.res.round(2)
        format_dict = {'Price': '{:.2f}', 'CMP': '{:.2f}', 'Buy Value': '{:.2f}', 'Qty.': '{:.0f}',
        'Current Value': '{:.2f}', 'Gain%': '{:.2f}', 'Amount': '{:.2f}'}
        total_place = st.empty()
        summary_place = st.empty()
        styled_res = res_rounded.sort_values('Date').style.format(format_dict).apply(highlight_gain_condition, subset=['Gain%'], axis=0)
        res_place.dataframe(styled_res)