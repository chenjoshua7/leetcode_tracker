import streamlit as st
from home import home_page
from scraper import scraper_page
from header import header

# Ensure set_page_config is called only once at the start
st.set_page_config(layout="wide")

# Sidebar for page navigation
with st.sidebar:
    st.markdown("<h1 style='text-align: center; padding: 20px 0;'>Mavigation</h1>", unsafe_allow_html=True) 
    page_selection = st.selectbox("Select a page", ["Home", "Scraper"], index=0)

header()

# Load the appropriate page based on the selection
if page_selection == "Home":
    home_page()
elif page_selection == "Scraper":
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
