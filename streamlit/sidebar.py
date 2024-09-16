import streamlit as st
from helper_functions import create_temporary_table
import webbrowser

def sidebar(filter = True):
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
        