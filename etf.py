import yfinance as yf
import dateutil.relativedelta
import datetime
from datetime import timedelta
import streamlit as st
import pandas as pd
import time
import math

st.title('ETF')
uploaded_file = st.file_uploader('Upload file', type='xlsx')

def get_stock_data(stock, start, end):
    try:
        data = yf.download(stock, start=start, end=end, progress = False)
        if data.empty:
            return None
        return data
    except Exception as e:
        return None

if 'button_pressed' not in st.session_state:
    st.session_state.button_pressed = False

if 'last_analysis_time' not in st.session_state:
    st.session_state.last_analysis_time = 0

if uploaded_file and st.button('Analyse'):
    st.session_state.button_pressed = True
res_place = st.empty()
while st.session_state.button_pressed:
    res = pd.DataFrame(columns=['ETF','Down%', 'CMP', 'Amount', 'Qty'])
    current_time = time.time()
    if current_time - st.session_state.last_analysis_time >= 300:
        st.session_state.last_analysis_time = current_time
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
            stocks = df.loc[df['Buy Price'].notna(), 'ETF'].tolist()
            today = datetime.datetime.today().date()
            for stock in stocks:
                data = get_stock_data(f"{stock}.NS", today, today + timedelta(days=1))
                cmp = round(data['Close'][-1],2)
                buy_price = df.loc[df['ETF'] == stock, 'Buy Price'].values[0]
                pnl = (cmp-buy_price)/buy_price
                multi_fac = -1*round(pnl*1000,2)
                variable = round((2500 * multi_fac)/100,2)
                amount = int(2500 + variable)
                qty = math.ceil(amount / cmp)
                print(stock, cmp, pnl, amount, qty)
                if pnl <= -0.02:
                    new_res = pd.DataFrame({'ETF': [stock], 'Down%':[round(pnl,2)], 'CMP':[cmp], 'Amount': [amount], 'Qty': [qty]})
                    res = pd.concat([res,new_res],ignore_index=True)
            res_place.text('')
            res_place.table(res)
        else:
            st.warning('Please upload an Excel file')