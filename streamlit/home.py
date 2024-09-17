import streamlit as st

from sidebar import sidebar

import pandas as pd
import numpy as np

import plotly.express as px

import datetime
from etl import DataQuerier
from skills import skills_page

from helper_functions import wrap_text, get_master_query, create_temporary_table

# Main function to display the home page
def home_page(df_filtered):

    ## Time Analsysis
    df_filtered['datetime'] = pd.to_datetime(df_filtered['date'])  # Ensure 'date' column is in datetime format

    # Round the datetime to the nearest 15 minutes
    df_filtered['time_15min'] = df_filtered['datetime'].dt.floor('30min')  # Use 'T' for minutes rounding

    # Extract just the time part for visualization (ignoring the date)
    df_filtered['time_15min'] = df_filtered['time_15min'].dt.time
    df_filtered = df_filtered.sort_values("time_15min", ascending=True)

    c1, space, c2 = st.columns([0.7,0.02, 0.3])
    with c1:
        st.markdown("<h2 style='text-align: center; padding-bottom: 10px;'>Home</h2>", unsafe_allow_html = True)
        st.markdown("""
                    LeetCode offers an excellent way to challenge your problem-solving skills while honing your knowledge of data structures and algorithms. This automated dashboard is designed to visualize my progress, providing both motivation and insights into my strengths and areas for improvement.

                    In addition to tracking performance, the dashboard includes a tool that automatically scrapes daily LeetCode problem data, allowing for easy submission and progress tracking through a user-friendly interface.

                    ### Time Prediction Benchmark
                    One key feature of this dashboard is a time predictor built. This model estimates the expected time to solve a problem, and I use it as a benchmark. Beating the predicted time is considered a win, while missing the benchmark signals the need for more practice.

                    ### Dashboard Sections:
                    - **Completion Time Analysis**: While completion time alone doesn’t always provide a complete picture—since some problems don’t require the most efficient solution—it still serves as a solid metric for evaluating performance.
                    
                    - **Skills Analysis**: This section helps me identify which skills I excel in and where further improvement is needed.

                    By analyzing both time and skills, this dashboard is a comprehensive tool to guide my ongoing development in competitive programming. Use the filter on the side to view specific data and focus on areas that matter most to you.
                    """)

    with c2:
        
        for _ in range(4):
            st.write("")
            
        #st.markdown("<h4 style='text-align: center; padding-bottom: 10px;'>LeetCode Habits</h4>", unsafe_allow_html = True)
        for _ in range(2):
            st.write("")
        # Plot the distribution using a histogram
        fig = px.histogram(
            df_filtered, 
            x='time_15min', 
            nbins=96,  # 96 intervals in a 24-hour day (24 hours * 4 per hour)
            title='LeetCode Time of Day Distribution',
        )
        
        # Update layout settings for better formatting
        fig.update_layout(
            bargap=0.2,  # Space between bars
            margin=dict(l=10, r=10, t=30, b=0),  # Customize margins
            xaxis_title=None,  # Remove x-axis title
            yaxis_title=None,  # Remove y-axis title
            height=230,  # Set figure height
        ).update_yaxes(
            showgrid=False,  # Remove gridlines from y-axis
            showticklabels=False  # Hide y-axis labels
        )
        
        # Display the plot in Streamlit
        st.plotly_chart(fig)

        #### Complexity

        complexity_counts = df_filtered.groupby("complexity").size()

        # Plot a pie chart with Plotly inside a container
        with st.container():
            complexity_fig = px.pie(complexity_counts, 
                                    names=complexity_counts.index, 
                                    values=complexity_counts.values,
                                    height = 250)
            
            complexity_fig.update_layout(
                    bargap=0.2,  # Space between bars
                    margin=dict(l=10, r=10, t=30, b=0),  # Customize margins
                    xaxis_title=None,  # Remove x-axis title
                    yaxis_title=None,  # Remove y-axis title
                    height=230,  # Set figure height
                ).update_yaxes(
                    showgrid=False,  # Remove gridlines from y-axis
                    showticklabels=False  # Hide y-axis labels
                )

            # Update the hover template for the pie chart
            complexity_fig.update_traces(hovertemplate="Complexity: %{label} <br> Count: %{value}")

            # Display the pie chart in Streamlit
            st.plotly_chart(complexity_fig)
            st.write("")