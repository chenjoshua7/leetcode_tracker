import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st

# Utility function to convert time in seconds to a readable format
def convert_seconds(time) -> str:
    min, sec = divmod(time, 60)
    return f"{min} Minutes, {sec} Seconds"

# Main Time Analysis Page
def time_page(df_filtered):
    # Header and Description
    st.markdown("<h2 style='text-align: center; padding-bottom: 20px;'>Completion Time Breakdown</h2>", unsafe_allow_html=True)
    st.markdown("""
    Tracking my performance over time is a valuable way to identify trends in how quickly I can solve problems. 
    It's also a great opportunity to revisit past questions and reflect on the notes I made.
    """, unsafe_allow_html=True)
    
    # Add some extra spacing before performance breakdown
    st.markdown("<br>", unsafe_allow_html=True)

    # Overall Performance and Performance by Complexity at the Top
    c1, c2 = st.columns(2)

    with c1:
        # Calculate the overall average and standard deviation for the "time" column
        average_time = int(np.mean(df_filtered["time"]))
        stddev_time = np.std(df_filtered["time"])

        # Display the overall average time with standard deviation
        st.markdown(f"<h3 style='text-align: center; padding-bottom: 15px;'>Overall Performance</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: #ff6347;'>Average Time: {convert_seconds(average_time)}</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #808080;'>Standard Deviation: {convert_seconds(int(stddev_time))}</p>", unsafe_allow_html=True)

    with c2:
        # Performance by Complexity - Mean and Standard Deviation
        st.markdown("<h3 style='text-align: center; padding-bottom: 15px;'>Performance by Complexity</h3>", unsafe_allow_html=True)

        # Group by complexity, calculate mean and standard deviation for each group
        by_complexity = df_filtered.groupby("complexity")["time"].agg(['mean', 'std']).dropna()
        
        # Organize complexity breakdown into columns
        cols = st.columns(len(by_complexity))
        
        for i, (complexity, stats) in enumerate(by_complexity.iterrows()):
            average = int(stats['mean'])
            stddev = int(stats['std'])

            with cols[i]:
                st.markdown(f"<h4 style='color: #4CAF50; text-align: center; padding-bottom: 5px;'>{complexity}</h4>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>Average Time: {convert_seconds(average)}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>Standard Deviation: {convert_seconds(stddev)}</p>", unsafe_allow_html=True)

    # Add a separator line
    st.markdown("<hr style='margin-top: 30px; margin-bottom: 20px;'>", unsafe_allow_html=True)

    # Line Chart - Completion Time Over Time
    st.markdown("<h3 style='text-align: center;'>Performance Over Time</h3>", unsafe_allow_html=True)
    fig = px.line(df_filtered, x='date', y='time',
                  labels={'time': 'Time', 'date': 'Date', 'complexity': 'Complexity'},
                  hover_data={'id': True, 'name': True, 'complexity': True, 'notes': True})
    
    fig.update_traces(
        mode="markers+lines",
        hovertemplate=(
            "%{customdata[0]}. %{customdata[1]}<br>"
            "Date: %{x}<br>"
            "Completion Time: %{y}<br>"
            "Complexity: %{customdata[2]}<br><br>"
            "Notes:<br>%{customdata[3]}<extra></extra>"
        )
        ).update_layout(
            xaxis_title=None,
            margin=dict(l=10, r=10, t=30, b=30),  # Reduced margins for more compact layout
            height=400  # Adjust height for a more compact chart
        )
    st.plotly_chart(fig, use_container_width=True)

    # Add some spacing before Time Distribution
    st.markdown("<br>", unsafe_allow_html=True)

    # Time Distribution with Reduced Height
    st.markdown("<h3 style='text-align: center;'>Time Distribution</h3>", unsafe_allow_html=True)
    time_hist = px.histogram(data_frame=df_filtered, x="time", nbins=20, color="complexity")
    time_hist.update_layout(
        height=250,  # Make the bottom graph smaller
        margin=dict(l=10, r=10, t=30, b=10)  # Adjust margins for the histogram
    )
    st.plotly_chart(time_hist, use_container_width=True)
