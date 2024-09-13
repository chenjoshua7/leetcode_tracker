import streamlit as st

import pandas as pd
import plotly.express as px
import webbrowser
from datetime import timedelta

from etl import ETL, DataQuerier

querier = DataQuerier()
df = querier.query("SELECT * FROM daily_problems ORDER BY date DESC", col_names = querier.col_names)
question_count = querier.query("SELECT COUNT(*) FROM daily_problems")

# Sidebar navigation
with st.sidebar:
    st.markdown("<h1 style='text-align: center; padding: 20px 0;'>Navigation</h1>", unsafe_allow_html=True)
    
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

    st.markdown("<h2>About the Project</h2>", unsafe_allow_html=True)
    st.markdown("")
# Title and description
st.markdown("<h1 style='text-align: center; padding-top:-10px; padding-bottom: 20px;'>LeetCode Daily Challenge Progress</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; padding-bottom: 10px;'>Joshua Chen</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: justify; font-size: 18px; padding-left: 30px; padding-right: 30px;'>Check out my progress with LeetCode Daily Challenges, where I solve algorithmic problems to hone my problem-solving skills.</p>", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1.2]) 
c1.markdown(f"""
    <div style='margin: auto; margin-bottom: 20px; width:80%; background-color: #2d2d2d; padding: 20px 30px; border-radius: 15px; 
                box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);'>
        <p style='font-size: 16px; font-weight: 600; color: #f9f9f9; margin-bottom: 5px;'>Total Completed: {question_count.iloc[0,0]}</p>
        <p style='font-size: 14px; color: #dddddd; margin-bottom: 5px;'>Current Streak: {"10 days"}</p>
        <p style='font-size: 14px; color: #dddddd;'>Longest Streak: {"30 days"}</p>
    </div>
    """, unsafe_allow_html=True)

c2.markdown(f"""
    <div style='margin-bottom: 20px; width:100%; background-color: #2d2d2d; padding: 20px 30px; border-radius: 15px; 
                box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);'>
        <p style='font-size: 16px; font-weight: 600; color: #f9f9f9; margin-bottom: 5px;'>Today's Daily Challenge Problem</p>
        <p style='font-size: 14px; color: #dddddd; margin-bottom: 5px;'>Current Streak: {"10 days"}</p>
        <p style='font-size: 14px; color: #dddddd;'>Longest Streak: {"30 days"}</p>
    </div>
    """, unsafe_allow_html=True)


# Expander for filters on top of the chart
with st.expander("Filters", expanded=False):
    c1, c2= st.columns(2)
    with st.container():
        # Date pickers for start and end dates
        start_date = c1.date_input("Start Date", value=df['date'].min())
        end_date = c2.date_input("End Date", value=df['date'].max() + timedelta(days=1))
    
    #filter by complexity:
    complexity = st.multiselect("Complexity", ['Easy', 'Medium', 'Hard'])

if not complexity:
    complexity = ['Easy', 'Medium', 'Hard']
    
# Ensure dates are in the correct format
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')
complexity_str = ', '.join([f"'{c}'" for c in complexity])

# Querying data from filters:
master_query = f"""
    SELECT * FROM daily_problems
    WHERE date BETWEEN '{start_date_str}' AND '{end_date_str}'
    AND complexity IN ({complexity_str});
"""
df = querier.query(master_query, col_names = querier.col_names)

df_filtered = df[df['time'] >= 60]
df_filtered = df_filtered.sort_values('date')

with st.container():    
    try:
        fig = px.line(df_filtered, x='date', y='time',
                title="Completion Time Over Time",
                labels={'time': 'Time', 'date': 'Date', 'complexity': 'Complexity'},
                hover_data={'id':True, 'name': True, 'complexity': True, 'notes': True}) 
    except:
        st.write("Please select a complexity")

# Update traces to show complexity in the hover template
    fig.update_traces(
        mode="markers+lines",
        hovertemplate=(
            "%{customdata[0]}. %{customdata[1]}<br>"
            "Date: %{x}<br>"
            "Complete Time: %{y}<br>"
            "Complexity: %{customdata[2]}<br><br>"
            "Notes:<br>%{customdata[3]}<extra></extra>"
        )
    )

    st.plotly_chart(fig)




complexity_counts = df.groupby("complexity").size()

# Plot a bar chart with Plotly inside a container
with st.container():
    complexity_fig = px.bar(complexity_counts, 
                            x=complexity_counts.index, 
                            y=complexity_counts.values, 
                            title="Count of Each Complexity Level",
                            labels={'x': 'Complexity', 'y': 'Count'})
    
    # Update the hover template for the bar chart
    complexity_fig.update_traces(hovertemplate="Complexity: %{x}<br>Count: %{y}")

    # Display the chart in Streamlit
    st.plotly_chart(complexity_fig)

querier.close()
