import streamlit as st

# Function to clear cache based on user
def clear_cache():
    if st.session_state.user == 'Amit':
        fetch_data_from_google_sheets.clear()
    elif st.session_state.user == 'Deepti':
        fetch_data_from_google_sheets_d.clear()
    elif st.session_state.user == 'Mridul':
        fetch_data_from_google_sheets_m.clear()
    elif st.session_state.user == 'Hemank':
        fetch_data_from_google_sheets_h.clear()