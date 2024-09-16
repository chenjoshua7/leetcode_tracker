import streamlit as st

from sidebar import sidebar

import pandas as pd
import numpy as np

import plotly.express as px

import datetime
from etl import DataQuerier

from helper_functions import wrap_text, get_master_query, create_temporary_table


@st.cache_data(ttl=1)
def get_filtered_table(start_date, end_date, complexity):
    querier = DataQuerier()
    create_temporary_table(querier.connection, start_date, end_date, complexity)
    # Get data with pfilters
    master_query = get_master_query()
    df_filtered = querier.query(master_query)
    querier.close()
    return df_filtered

# Main function to display the home page
def home_page():
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

    sidebar()

    #Filtering and sorting data    
    df_filtered = df_filtered[df_filtered['time'] >= 60]
    df_filtered = df_filtered.sort_values('date')
    df_filtered['notes'] = df_filtered['notes'].apply(wrap_text)

    skills = df_filtered['skills'].str.split(',').explode().str.strip().unique()
    # Create a dictionary to store the count of each skill
    skill_counts = {}
    skill_averages = {}

    # Loop through each unique skill
    for skill in skills:
        # Count the number of rows that contain the skill
        count = df_filtered['skills'].apply(lambda x: skill in x).sum()
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
            height=500,
        ).update_layout(xaxis_title=None, )
        c1.plotly_chart(skill_bar_count)

        # Create a DataFrame for skill averages
        skill_averages_df = pd.DataFrame(list(skill_averages.items()), columns=['Skill', 'Averages']).sort_values("Averages", ascending=True)

    # Function to convert seconds to "minutes and seconds" format
    def convert_seconds_to_min_sec(seconds):
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes} min {remaining_seconds} sec"

    def prepend_spaces(skill, max_length):
        return skill.rjust(max_length)

    max_length = max(skill_averages_df['Skill'].str.len())
    #skill_averages_df['Skill'] = skill_averages_df['Skill'].apply(lambda x: prepend_spaces(x, max_length))


    # Create a new column for the formatted labels
    skill_averages_df['Averages_Formatted'] = skill_averages_df['Averages'].apply(convert_seconds_to_min_sec)

    # Create containers within the second column for "rows"
    with c2:
        # Create a container for the top skills chart with reduced margins
        with st.container():
            top_skills_df = skill_averages_df.iloc[:5].iloc[::-1]  # Reverse the order
            skill_bar_top = px.bar(
                data_frame=top_skills_df, 
                x='Averages',
                y='Skill', 
                title="Top Skills", 
                orientation="h",
                color_discrete_sequence=["green"],
                height=230,
                custom_data=['Skill', 'Averages_Formatted'],
            )
            
            st.write("")
            
            skill_bar_top.update_layout(
                margin=dict(l=10, r=10, t=30, b=0), 
                title={'y': 1},
                xaxis_title=None,
                yaxis_title=None, 
            ).update_traces(
                hovertemplate="Skill: %{customdata[0]} <br> %{customdata[1]}"
            ).update_xaxes(
                showgrid=False,
                showticklabels=False 
            )   
            
            st.plotly_chart(skill_bar_top)

        st.write("")
        # Create a container for the needs practice chart with reduced margins
        with st.container():
            needs_practice_df = skill_averages_df.iloc[-5:]
            
            # Create the bar plot
            skill_bar_needs_practice = px.bar(
                data_frame=needs_practice_df, 
                x='Averages',  # x-axis data
                y='Skill',  # y-axis data
                title="Needs Practice", 
                orientation="h",
                color_discrete_sequence=["red"],
                height=230, 
                custom_data=['Skill', 'Averages_Formatted'], 
            )

            # Update the layout and traces
            skill_bar_needs_practice.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                title={'y': 1}, 
                xaxis_title=None,
                yaxis_title=None, 
            ).update_traces(
                hovertemplate="Skill: %{customdata[0]}<br>Time: %{customdata[1]}"  # Use customdata for hovertemplate
            ).update_xaxes(
                showgrid=False,
                showticklabels=False)
            
            # Display the figure in Streamlit
            st.plotly_chart(skill_bar_needs_practice, use_container_width=True)






    ## Time Analsysis


    st.markdown("<h2> Time Analysis </h2>", unsafe_allow_html=True)
    c1, space, c2 = st.columns([1,0.05,1])
    with c1.container():    
        try:
            fig = px.line(df_filtered, x='date', y='time',
                    title="Completion Time Over Time",
                    labels={'time': 'Time', 'date': 'Date', 'complexity': 'Complexity'},
                    hover_data={'id':True, 'name': True, 'complexity': True, 'notes': True}) 
            
            fig.update_traces(
                mode="markers+lines",
                hovertemplate=(
                    "%{customdata[0]}. %{customdata[1]}<br>"
                    "Date: %{x}<br>"
                    "Complete Time: %{y}<br>"
                    "Complexity: %{customdata[2]}<br><br>"
                    "Notes:<br>%{customdata[3]}<extra></extra>"
                )
            ).update_layout(
                xaxis_title = None
            )
        except:
            st.write("Please select a complexity")



        c1.plotly_chart(fig)

        time_hist = px.histogram(data_frame=df_filtered, x="time", nbins = 20, pattern_shape = "complexity")
        c2.plotly_chart(time_hist)


    #### Complexity

    complexity_counts = df_filtered.groupby("complexity").size()

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


    df_filtered['datetime'] = pd.to_datetime(df_filtered['date'])  # Ensure 'date' column is in datetime format

    # Round the datetime to the nearest 15 minutes
    df_filtered['time_15min'] = df_filtered['datetime'].dt.floor('30min')  # Use 'T' for minutes rounding

    # Extract just the time part for visualization (ignoring the date)
    df_filtered['time_15min'] = df_filtered['time_15min'].dt.time
    df_filtered = df_filtered.sort_values("time_15min", ascending=True)

    # Plot the distribution using a histogram
    fig = px.histogram(
        df_filtered, 
        x='time_15min', 
        nbins=96,  # There are 96 intervals in a 24-hour day (24 hours * 4 per hour)
        title='Distribution of Times in 15-Minute Increments',
        labels={'time_15min': 'Time (15-minute intervals)'},
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Time (15-minute intervals)",
        yaxis_title="Frequency",
        bargap=0.2
    )

    st.plotly_chart(fig)