import streamlit as st
from home import home_page
from scraper import scraper_page

# Ensure set_page_config is called only once at the start
st.set_page_config(layout="wide")

# Sidebar for page navigation
with st.sidebar:
    st.markdown("<h1 style='text-align: center; padding: 20px 0;'>Mavigation</h1>", unsafe_allow_html=True) 
    page_selection = st.selectbox("Select a page", ["Home", "Scraper"], index=0)

# Load the appropriate page based on the selection
if page_selection == "Home":
    home_page()
elif page_selection == "Scraper":
    scraper_page()
