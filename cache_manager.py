import streamlit as st

# Function to clear cache based on user
def clear_cache_for_user(user, fetch_function):
    fetch_function.clear()