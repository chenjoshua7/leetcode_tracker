import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from helper_functions import wrap_text

def skills_page(df_filtered):
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



