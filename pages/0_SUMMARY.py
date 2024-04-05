import pandas as pd
import streamlit as st
import time
import yfinance as yf
from datetime import datetime
import datetime

secrets = st.session_state.secrets
page_config_set = False

def set_page_config():
    global page_config_set
    if not page_config_set:
        st.set_page_config(page_title="ETFDash", page_icon="📈", layout="wide")
        page_config_set = True

set_page_config()
col1, col2 = st.columns([1,1])
st.session_state.last_analysis_time = time.time() - 110

def highlight_gain_condition(s):
    if s.name == 'ROI' or s.name == 'Gain':
        return s.apply(lambda x: highlight_single_gain(x))
    elif s.name == 'Total Investment':
        return s.apply(lambda x: highlight(x))
    else:
        return s.apply(lambda x: highlight_2(x))

def highlight_gain_condition2(s):
    if s.name == 'ROI':
        return s.apply(lambda x: highlight_roi(x))
    
def highlight_roi(value):
    if value < 0:
        color = 'rgba(255, 0, 0, 0.8)'  # Red with 50% opacity
    elif value == 0:
        color = 'rgba(255, 192, 203, 0.7)'
    elif 0 < value <= 2:
        color = 'rgba(255, 255, 0, 0.7)'  # Yellow with 50% opacity
    elif 2 < value <= 3:
        color = 'rgba(255, 140, 0, 1)'  # Orange with 50% opacity
    elif 3 < value:
        color = 'rgba(63, 255, 0,1)'  # Green with 50% opacity
    else:
        color = ''  # No highlighting if not in specified ranges
    return 'background-color: %s' % color

def highlight_gain(x):
    if 3 < x <= 4:
        color = 'rgba(255, 140, 0, 1)'  # Orange with 50% opacity
    elif 4 < x:
        color = 'rgba(63, 255, 0,1)'  # Green with 50% opacity
    return 'background-color: %s' % color

def highlight(x):
    color = 'rgba(139,190,27,1)'
    return 'background-color: %s' % color
def highlight_2(x):
    color = 'rgba(255, 140, 0, 1)'
    return 'background-color: %s' % color
def highlight_single_gain(value):
    if value <= 0:
        color = 'rgba(255, 0, 0, 0.8)'
    else:
        color = 'rgba(63, 255, 0,1)'  
    return 'background-color: %s' % color

def get_cmp_price(cmp_symbol):
    try:
        cmp_data = yf.Ticker(cmp_symbol+".NS")
        cmp_price = cmp_data.history(period="1d")["Close"].iloc[-1]
        return cmp_price
    except Exception as e:
        st.error(f"Failed to fetch cmp price: {e}")
        return None


if 'total_invested' not in st.session_state:
    st.session_state.total_invested = 0

sum_title = st.empty()
total_invested_place = st.empty()
individual_invested_place_1 = st.empty()
individual_invested_place_2 = st.empty()
sum_title.title('Summary')

total_invested = 0
total_current_value = 0
while True:
    investment_total = pd.DataFrame(columns=['Total Investment','Current Value','ROI','Gain'])
    investment_individual = pd.DataFrame(columns=["ETF",'Total Investment','Current Value','ROI','Gain'])
    if time.time() - st.session_state.last_analysis_time >= 100:
        st.session_state.last_analysis_time = time.time()
        stocks = list(st.session_state.all_data.keys())
        today = datetime.datetime.today().date()
        for stock in stocks:
            time.sleep(1)
            st.session_state.all_data[stock]['Qty.'] = st.session_state.all_data[stock]['Qty.'].str.replace(',', '').astype(float) if st.session_state.all_data[stock]['Qty.'].dtype == 'object' else st.session_state.all_data[stock]['Qty.']
            cmp = get_cmp_price(st.session_state.secrets["connections"]["gsheets"]["worksheets"][stock])
            total_value =  ((st.session_state.all_data[stock]['Qty.']) * (st.session_state.all_data[stock]['Price']).astype(float)).sum() if not st.session_state.all_data[stock].empty else 0
            total_invested += total_value
            current_value =  ((st.session_state.all_data[stock]['Qty.']) * cmp).sum() if not st.session_state.all_data[stock].empty else 0
            total_current_value += current_value
            total_qty = (st.session_state.all_data[stock]['Qty.']).sum() if not st.session_state.all_data[stock].empty else 1
            buy_price = round(total_value / total_qty,2)
            st.session_state.all_data[stock]['Price'] = pd.to_numeric(st.session_state.all_data[stock]['Price'], errors='coerce')
            pnl = (cmp-buy_price)/buy_price if buy_price != 0 else 0
            investment_individual = pd.concat([investment_individual,pd.DataFrame({"ETF":[stock],'Total Investment':[total_value],'Current Value':[current_value],'ROI':[round((pnl) * 100,2)],'Gain':[round(current_value - total_value,2)]})],ignore_index=True)

        investment_total = pd.concat([investment_total,pd.DataFrame({'Total Investment':[total_invested],'Current Value':[total_current_value],'ROI':[round(((total_current_value - total_invested)/total_invested) * 100,2)],'Gain':[round(total_current_value - total_invested,2)]})],ignore_index=True)
        res_rounded = investment_total.round(2)
        res_individual_rounded = investment_individual.sort_values("ROI", ascending=False).round(2)
        res_individual_rounded_1 = res_individual_rounded.iloc[:len(res_individual_rounded)//2]
        res_individual_rounded_2 = res_individual_rounded.iloc[len(res_individual_rounded)//2:]
        format_dict = {'Total Investment': '{:.2f}', 'Current Value': '{:.2f}', 'ROI': '{:.2f}', 'Gain': '{:.0f}'}
        styled_res = res_rounded.style.format(format_dict).apply(highlight_gain_condition, axis=0)
        styled_res_individual_1 = res_individual_rounded_1.style.format(format_dict).apply(highlight_gain_condition2,subset=['ROI'], axis=0)
        styled_res_individual_2 = res_individual_rounded_2.style.format(format_dict).apply(highlight_gain_condition2,subset=['ROI'], axis=0)
        total_invested_place.dataframe(styled_res)
        numRows = len(res_individual_rounded)//2
        with col1:
            individual_invested_place_1.dataframe(styled_res_individual_1, use_container_width=True, height=(numRows + 1) * 35 + 3)
        with col2:
            individual_invested_place_2.dataframe(styled_res_individual_2, use_container_width=True, height=(numRows + 1) * 35 + 3)
        st.session_state.total_invested = total_invested
