import streamlit as st
from home import home_page
from scraper import scraper_page
from header import header
from sidebar import sidebar
from skills import skills_page
from time_page import time_page

# Ensure set_page_config is called only once at the start
st.set_page_config(layout="wide")

df_filtered = sidebar()

# Sidebar for page navigation
header()

with st.container():
    page_selection = st.selectbox("", ["Home", "Completion Time Breakdown", "Skills Breakdown", "Daily Problem Tracker"], index=0)

# Load the appropriate page based on the selection
if page_selection == "Home":
    home_page()
elif page_selection == "Completion Time Breakdown":
    time_page(df_filtered)
elif page_selection == "Skills Breakdown":
    skills_page(df_filtered)
elif page_selection == "Daily Problem Tracker":
    scraper_page()

with st.expander("About this Project", expanded=False):
        st.markdown("""
        **Backend:**  
        The project uses **AWS RDS** to host a **MySQL** database, ensuring scalability and secure data storage.
        
        **ETL Process:**  
        The Python script automates the scraping of the Daily Question using Selenium and BeautifulSoup, gathers performance statistics, and loads the data into the database.
        
        **Frontend:**  
        The user interface is built using **Streamlit**, providing an interactive and intuitive platform for visualizing the data.
        </br>
        </br>
        All code can be found in the repository link in the sidebar.
        """, unsafe_allow_html = True)
