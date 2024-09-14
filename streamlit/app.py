import streamlit as st

import pandas as pd
import numpy as np

import plotly.express as px
import webbrowser
from datetime import timedelta

from etl import DataQuerier
from helper_functions import wrap_text, get_current_streak, get_daily_question, get_master_query, create_temporary_table
from queries import streak_query

# Wide Layout
st.set_page_config(layout="wide")

# Set Up
querier = DataQuerier()
df = querier.query("SELECT * FROM daily_problems ORDER BY date DESC")
question_count = querier.query("SELECT COUNT(*) FROM daily_problems")
streaks = querier.query(streak_query)

# Get streak data
current_streak = get_current_streak(streaks)
max_streak = max(streaks["streak_length"])

# Daily question info
daily_question = get_daily_question(df)

# Sidebar navigation
with st.sidebar:
    with st.expander("Filters", expanded=False):
        c1, c2= st.columns(2)
        with st.container():
            # Date pickers for start and end dates
            start_date = c1.date_input("Start Date", value=df['date'].min())
            end_date = c2.date_input("End Date", value=df['date'].max() + timedelta(days=1))

        # Filter by complexity
        complexity = st.multiselect("Complexity", ['Easy', 'Medium', 'Hard'])
        
    st.markdown("<h1 style='text-align: center; padding: 20px 0;'>Navigation</h1>", unsafe_allow_html=True)
    
    ## Create the temporary table based off of filters
    create_temporary_table(querier.connection, start_date, end_date, complexity)
    
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
    
# Title and description
st.markdown("<h1 style='text-align: center; padding-top:-10px; padding-bottom: 20px;'>LeetCode Daily Problem Progress</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; padding-bottom: 10px;'>Joshua Chen</h4>", unsafe_allow_html=True)
st.markdown("""<p style='text-align: justify; font-size: 18px; padding-left: 30px; padding-right: 30px;'>     
            Welcome to my LeetCode Daily Progress tracker. Each day, I start with the LeetCode Daily Problem 
            to sharpen as a brain teaser and to improve my coding skills. LeetCode offers a variety of challenges 
            focused on algorithms and data structures, which has helped me grow as a programmer. Take a look at 
            how I’ve been progressing!
            </p>""", unsafe_allow_html=True)

space1, c1, space2, c2, space3 = st.columns([0.2,1,0.3, 1.5, 0.2]) 
c1.markdown(f"""
    <div style='text-align:center; margin-bottom: 20px; width:100%; background-color: #2d2d2d; padding: 20px 30px 10px 30px; border-radius: 15px; 
                box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);'>
        <p style='font-size: 16px; font-weight: 600; color: #f9f9f9; margin-bottom: 5px;'>Total Completed: {question_count.iloc[0,0]}</p>
        <p style='font-size: 15px; color: #dddddd; margin-bottom: 5px;'>Current Streak: {current_streak} days</p>
        <p style='font-size: 15px; color: #dddddd;'>Longest Streak: {max_streak} days</p>
    </div>
    """, unsafe_allow_html=True)

c2.markdown(daily_question, unsafe_allow_html=True)

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


# Querying data from filters:
master_query = get_master_query()
df = querier.query(master_query)

df_filtered = df[df['time'] >= 60]
df_filtered = df_filtered.sort_values('date')
df_filtered['notes'] = df_filtered['notes'].apply(wrap_text)

skills = df['skills'].str.split(',').explode().str.strip().unique()
# Create a dictionary to store the count of each skill
skill_counts = {}
skill_averages = {}

# Loop through each unique skill
for skill in skills:
    # Count the number of rows that contain the skill
    count = df['skills'].apply(lambda x: skill in x).sum()
    filtered_df = df_filtered[df_filtered['skills'].apply(lambda x: skill in x)]

    average = filtered_df['time'].mean()
    if average is not np.nan:
        skill_averages[skill] = average
    skill_counts[skill] = count

st.markdown("## Skills Section")

#with st.expander("Skills Section", expanded = False):
with st.container():
    # Create two columns for the main layout, allocating more space for column 1
    c1, space, c2 = st.columns([2, 0.25, 1.75])

    # Create a DataFrame for skill counts and plot the bar chart
    skill_count_df = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Count']).sort_values("Count", ascending=False)
    skill_bar_count = px.bar(
        data_frame=skill_count_df, 
        x='Skill', 
        y='Count', 
        title="Skill Frequency",
        height=500  # Adjusting the height of the first plot
    )
    c1.plotly_chart(skill_bar_count)

    # Create a DataFrame for skill averages
    skill_averages_df = pd.DataFrame(list(skill_averages.items()), columns=['Skill', 'Averages']).sort_values("Averages", ascending=True)

    # Create containers within the second column for "rows"
    with c2:
        # Create a container for the top skills chart with reduced margins
        with st.container():
            top_skills_df = skill_averages_df.iloc[:5]
            skill_bar_top = px.bar(
                data_frame=top_skills_df, 
                x='Averages', 
                y='Skill', 
                title="Top Skills", 
                orientation="h",
                color_discrete_sequence=["green"],
                height=250 
            ).update_layout(
                margin=dict(l=10, r=10, t=30, b=0), 
                title={'y': 0.9} 
            )
            st.plotly_chart(skill_bar_top)

        # Create a container for the needs practice chart with reduced margins
        with st.container():
            needs_practice_df = skill_averages_df.iloc[-5:]
            skill_bar_needs_practice = px.bar(
                data_frame=needs_practice_df, 
                x='Averages', 
                y='Skill', 
                title="Needs Practice", 
                orientation="h",
                color_discrete_sequence=["red"],
                height=250
            ).update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                title={'y': 1}
            )
            st.plotly_chart(skill_bar_needs_practice)

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
