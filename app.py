import gspread
import pandas as pd
import streamlit as st
import time
import yfinance as yf
from datetime import datetime
import toml
import math
import datetime
from datetime import timedelta

secrets = toml.load('secrets.toml')
st.set_page_config(page_title="ETFDash", page_icon="📈", layout="wide")
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

@st.cache_data
def fetch_data_from_google_sheets_d(_secrets):
    try:
        client = gspread.service_account_from_dict({
            "type": _secrets["connections"]["gsheets_d"]["type"],
            "project_id": _secrets["connections"]["gsheets_d"]["project_id"],
            "private_key_id": _secrets["connections"]["gsheets_d"]["private_key_id"],
            "private_key": _secrets["connections"]["gsheets_d"]["private_key"],
            "client_email": _secrets["connections"]["gsheets_d"]["client_email"],
            "client_id": _secrets["connections"]["gsheets_d"]["client_id"],
            "auth_uri": _secrets["connections"]["gsheets_d"]["auth_uri"],
            "token_uri": _secrets["connections"]["gsheets_d"]["token_uri"],
            "auth_provider_x509_cert_url": _secrets["connections"]["gsheets_d"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": _secrets["connections"]["gsheets_d"]["client_x509_cert_url"]
        })
        spreadsheet_key = _secrets["connections"]["gsheets_d"]["spreadsheet"]
        
        all_data = {}
        for cmp_symbol in _secrets["connections"]["gsheets"]["worksheets"].values():
            sheet = client.open_by_key(spreadsheet_key).worksheet(cmp_symbol)
            data = sheet.get_all_values()
            df = pd.DataFrame(data)
            df = pd.DataFrame(data[1:], columns=data[0])
            all_data[cmp_symbol] = df
        
        return all_data
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()

@st.cache_data
def fetch_data_from_google_sheets(_secrets):
    try:
        client = gspread.service_account_from_dict({
            "type": _secrets["connections"]["gsheets"]["type"],
            "project_id": _secrets["connections"]["gsheets"]["project_id"],
            "private_key_id": _secrets["connections"]["gsheets"]["private_key_id"],
            "private_key": _secrets["connections"]["gsheets"]["private_key"],
            "client_email": _secrets["connections"]["gsheets"]["client_email"],
            "client_id": _secrets["connections"]["gsheets"]["client_id"],
            "auth_uri": _secrets["connections"]["gsheets"]["auth_uri"],
            "token_uri": _secrets["connections"]["gsheets"]["token_uri"],
            "auth_provider_x509_cert_url": _secrets["connections"]["gsheets"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": _secrets["connections"]["gsheets"]["client_x509_cert_url"]
        })
        spreadsheet_key = _secrets["connections"]["gsheets"]["spreadsheet"]
        
        all_data = {}
        for cmp_symbol in _secrets["connections"]["gsheets"]["worksheets"].values():
            sheet = client.open_by_key(spreadsheet_key).worksheet(cmp_symbol)
            data = sheet.get_all_values()
            df = pd.DataFrame(data)
            df = pd.DataFrame(data[1:], columns=data[0])
            all_data[cmp_symbol] = df
        
        return all_data
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()

def get_cmp_price(cmp_symbol):
    try:
        cmp_data = yf.Ticker(cmp_symbol+".NS")
        cmp_price = cmp_data.history(period="1d")["Close"].iloc[-1]
        return cmp_price
    except Exception as e:
        st.error(f"Failed to fetch cmp price: {e}")
        return None
def get_stock_data(stock, start, end):
    try:
        data = yf.download(stock, start=start, end=end, progress = False)
        if data.empty:
            return None
        return data
    except Exception as e:
        return None


user = st.selectbox("Select User",['None','Amit','Deepti'])
if user == 'Amit':
    all_data = fetch_data_from_google_sheets(secrets)
elif user == 'Deepti':
    all_data = fetch_data_from_google_sheets_d(secrets)
if user:
    st.sidebar.title('Navigation')
    selected_tab = st.sidebar.radio('Go to',['Summary']+list(all_data.keys()))
    clear = st.sidebar.button("Clear Cache")
    if clear:
        st.cache_data.clear()
        st.rerun()
    if "selected_tab" not in st.session_state:
        st.session_state["selected_tab"] = 0
    res = all_data[selected_tab] if selected_tab != 'Summary' else all_data
    if 'last_analysis_time' not in st.session_state:
        st.session_state.last_analysis_time = time.time()
    sum_title = st.empty()
    summary_place = st.empty()
    total_place = st.empty()
    title = st.empty()
    res_place = st.empty()
    if selected_tab == 'Summary':
        sum_title.title('Summary')
        res_place = st.empty()
        title = st.empty()
        while True:
            summary = pd.DataFrame(columns=['ETF','Down%', 'CMP', 'LB','Amount', 'Qty'])
            if time.time() - st.session_state.last_analysis_time >= 0 or selected_tab != st.session_state["selected_tab"]:
                st.session_state["selected_tab"] = selected_tab
                st.session_state.last_analysis_time = time.time()
                stocks = list(all_data.keys())
                today = datetime.datetime.today().date()
                for stock in stocks:
                    time.sleep(1)
                    data = get_stock_data(f"{stock}.NS", today, today + timedelta(days=1))
                    cmp = round(data['Close'][-1],2)
                    total_value =  ((all_data[stock]['Qty.'].str.replace(',','').astype(float)) * (all_data[stock]['Price']).astype(float)).sum() if not all_data[stock].empty else 0
                    total_qty = (all_data[stock]['Qty.'].str.replace(',','').astype(float)).sum() if not all_data[stock].empty else 1
                    buy_price = round(total_value / total_qty,2)
                    all_data[stock]['Price'] = pd.to_numeric(all_data[stock]['Price'], errors='coerce')
                    last_buy = all_data[stock].sort_values('Date')['Price'].values[-1] if not all_data[stock].empty else 0
                    pnl = (cmp-buy_price)/buy_price if buy_price != 0 else 0
                    multi_fac = -1*round(pnl*1000,2)
                    variable = round((5000 * multi_fac)/100,2)
                    amount = int(5000 + variable) if variable > 0 else 0
                    qty = math.ceil(amount / cmp)
                    if cmp < last_buy:
                        new_res = pd.DataFrame({'ETF': [stock], 'Down%':[round(pnl*100,2)], 'CMP':[cmp], 'Amount': [amount], 'Qty': [qty], 'LB': [last_buy]})
                        summary = pd.concat([summary,new_res],ignore_index=True)
                if summary.empty:
                    total = 0
                else:
                    print(1)
                    total = summary['Amount'].sum()
                    summary_place.dataframe(summary.sort_values('Down%'))
                    total_place.success('Total Amount: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(total))
    else:
        if 'Price' in res.columns and 'Qty.' in res.columns:
            res['Price'] = res['Price'].str.replace(',', '').astype(float)
            res['Qty.'] = res['Qty.'].str.replace(',', '').astype(float)
            res['Buy Value'] = res['Price'] * res['Qty.']
            res['Age'] = (datetime.datetime.now() - pd.to_datetime(res['Date'])).dt.days
        else:
            st.error("Columns 'Price' and/or 'Qty.' not found in the DataFrame.")
        while True:
            if time.time() - st.session_state.last_analysis_time >= 100 or selected_tab != st.session_state["selected_tab"]:
                st.session_state.last_analysis_time = time.time()
                st.session_state.selected_tab = selected_tab

                res['CMP'] = round(get_cmp_price(st.secrets["connections"]["gsheets"]["worksheets"][selected_tab]),2)
                res['Current Value'] = res['Qty.'] * res['CMP']
                res['Gain%'] = round(((res['Current Value'] - res['Buy Value']) / res['Buy Value']) * 100,2)
                res['Amount'] = res['Current Value'] - res['Buy Value']
                
                title.title('')
                title.title(f'Data for {selected_tab}')
                res_place.text('')
                res_rounded = res.round(2)
                format_dict = {'Price': '{:.2f}', 'CMP': '{:.2f}', 'Buy Value': '{:.2f}', 'Qty.': '{:.0f}',
                'Current Value': '{:.2f}', 'Gain%': '{:.2f}', 'Amount': '{:.2f}'}
                total_place = st.empty()
                summary_place = st.empty()
                styled_res = res_rounded.sort_values('Date').style.format(format_dict).apply(highlight_gain_condition, subset=['Gain%'], axis=0)
                res_place.dataframe(styled_res)
                # res_place.data_editor(styled_res,key = st.session_state.last_analysis_time, num_rows="dynamic")

