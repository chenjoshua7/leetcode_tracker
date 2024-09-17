from etl import DataQuerier
import streamlit as st
import pandas as pd

def querier_page():
    # Initialize the DataQuerier class (assuming it exists)
    querier = DataQuerier()

    # Page title
    st.markdown("<h2 style='text-align: center; padding-bottom: 10px;'>Querier</h2>", unsafe_allow_html=True)

    # Store the query in session state
    if "query" not in st.session_state:
        st.session_state.query = ""
    if "query_submitted" not in st.session_state:
        st.session_state.query_submitted = False

    # Function to run the query when either "Enter" is pressed or button clicked
    def run_query():
        try:
            df = querier.query(st.session_state.query)
            # Display the result in a dataframe format
            if df is not None and not df.empty:
                st.dataframe(df)
            else:
                st.write("No data returned from the query.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Input field for the query
    query_input = st.text_input('Enter Query', value=st.session_state.query, key="query")

    # Button to run the query manually
    if st.button('Query'):
        st.session_state.query_submitted = True
        run_query()

    # Check if "Enter" is pressed (i.e., query text changes)
    elif st.session_state.query_submitted or st.session_state.query != "":
        run_query()

    st.subheader("Example Queries:")
    st.code("SELECT * FROM daily_problems ORDER BY date DESC")
    st.code("SELECT id, name, notes FROM daily_problems ORDER BY time LIMIT 5")
    st.code("SELECT complexity, AVG(time) AS average_time FROM daily_problems GROUP BY complexity")
    querier.close()