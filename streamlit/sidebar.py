import streamlit as st
from helper_functions import create_temporary_table, get_master_query, wrap_text
import webbrowser
import datetime
from etl import DataQuerier


@st.cache_data(ttl=300)
def get_filtered_table(start_date, end_date, complexity):
    querier = DataQuerier()
    create_temporary_table(querier.connection, start_date, end_date, complexity)
    # Get data with pfilters
    master_query = get_master_query()
    df_filtered = querier.query(master_query)
    querier.close()
    return df_filtered

def sidebar():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; padding: 20px 0;'>Filters</h1>", unsafe_allow_html=True)
        with st.expander("Filters", expanded=False):
            c1, c2= st.columns(2)
            with st.container():
                # Date pickers for start and end dates
                start_date = c1.date_input("Start Date", value=datetime.date(2024, 8, 28))
                end_date = c2.date_input("End Date", value=datetime.date.today())
                start_date= start_date + datetime.timedelta(days= 1)
                
            # Filter by complexity
            complexity = st.multiselect("Complexity", ['Easy', 'Medium', 'Hard'])
    
    df_filtered = get_filtered_table(start_date, end_date, complexity)
    #Filtering and sorting data    
    df_filtered = df_filtered[df_filtered['time'] >= 60]
    df_filtered = df_filtered.sort_values('date')
    df_filtered['notes'] = df_filtered['notes'].apply(wrap_text)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; padding: 20px 0;'>Links</h1>", unsafe_allow_html=True)
        
        # Create columns for better alignment of buttons
        col1 = st.columns(1)
        with col1[0]:
            if st.button("🏠  Portfolio", use_container_width=True):
                webbrowser.open_new_tab("https://chenjoshua7.github.io")
            
            if st.button("🐙  GitHub", use_container_width=True):
                webbrowser.open_new_tab("https://www.github.com/chenjoshua7")
            
            if st.button("🔗  LinkedIn", use_container_width=True):
                webbrowser.open_new_tab("https://www.linkedin.com/in/chenjoshua7")

        st.markdown("<p style='margin-top: 10px;'>Email: <a href='mailto:chen.joshua98@gmail.com'>chen.joshua98@gmail.com</a></p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top: 0px;'>Repo: <a href='https://github.com/chenjoshua7/leetcode_tracker'>/chenjoshua7/leetcode_tracker</a></p>", unsafe_allow_html=True)
    return df_filtered