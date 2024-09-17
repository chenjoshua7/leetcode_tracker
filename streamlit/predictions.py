import streamlit as st
import pickle
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from model.preprocessor import PreprocessData
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import json
from sklearn.linear_model import LinearRegression


# Function to convert time in seconds to minutes and seconds format
def convert_seconds(time) -> str:
    min, sec = divmod(int(time), 60)
    return f"{min} Minutes, {sec} Seconds"

    
# Function to render the prediction page
def prediction_page(df_filtered):
    # Page title and description
    st.markdown("<h2 style='text-align: center; padding-bottom: 10px;'>Today's Performance Review</h2>", unsafe_allow_html=True)
    st.info("This page is a work in progress", icon="🚧")
    
    st.markdown("""
        To better track my daily performance, I'm building a model that predicts my progress. The goal is to eventually surpass 
        the model’s predictions and achieve better results over time.
        
        At this stage, I only have 16 samples, which is too limited for high accuracy. For now, I’ll use a simple 
        **Linear Regression model** as a baseline. As I gather more data, I plan to experiment with more advanced algorithms 
        and techniques, such as clustering to identify patterns in similar types of problems.
    """)
    
    # Reconstruct the linear regression model
    pipeline = Pipeline(steps=[
        ('preprocessor', PreprocessData()),
        ('regressor', LinearRegression())
    ])

    # Date logic: filter today's and yesterday's data
    today = datetime.now().date()
    
    df_filtered = df_filtered.sort_values("date", ascending=False).reset_index(drop=True)

    # Check if there's data available for today
    if df_filtered['date'][0].date() == today:
        # Make prediction based on the most recent 4 records
        pipeline.fit(df_filtered, df_filtered["time"])
        y_pred = pipeline.predict(df_filtered)
        actual_time = df_filtered["time"]
        df_filtered["predicted"] = y_pred

        # Determine color (goal achieved or not)
        if y_pred[0] > actual_time[0]:
            color = "green"
        else:
            color = "red"

        # Calculate standard deviation for the time data
        std_dev = df_filtered["time"].std()/2
        
        # Display goal and actual performance with color coding
        st.markdown(f"<h4 style='text-align: center; color: {color};'>Today's Goal: {convert_seconds(y_pred[0])}</h4>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: {color};'>Actual Time: {convert_seconds(actual_time[0])}</h4>", unsafe_allow_html=True)

        # Determine how far actual time is from predicted time in terms of standard deviations
        time_difference = abs(y_pred[0] - actual_time[0])
        feedback_message = ""
        
        if time_difference <= 0.5 * std_dev:
            feedback_message = "Nicely Done! 👍"
        elif time_difference <= 1 * std_dev:
            feedback_message = "Not bad, I was close! 😊"
        elif time_difference <= 1.5 * std_dev:
            if y_pred[0] > actual_time[0]:
                feedback_message = "Super fast! 🚀"
            else:
                feedback_message = "Tough one today, I gotta keep pushing! 💪"
        else:
            if y_pred[0] > actual_time[0]:
                feedback_message = "WOW! That was lightning fast! ⚡️"
            else:
                feedback_message = "Oof, rough day... 😅"
        st.markdown(f"<h4 style='text-align: center; color: {color};'>{feedback_message}</h4>", unsafe_allow_html=True)
        
        # Add a slider to select how many rows to display
        row_count = st.slider('Select number of rows to display', min_value=3, max_value=len(df_filtered), value=5, step=1)

        # Filter the DataFrame based on slider value
        df_filtered_slider = df_filtered.head(row_count)

        # Create the line plot
        predict_fig = px.line(
            data_frame=df_filtered_slider, 
            x="date", 
            y=["predicted", "time"],  # Both predicted and actual time
            labels={'time': 'Completion Time', 'predicted': 'Predicted Time', 'date': 'Date', 'complexity': 'Complexity'},
            hover_data={'id': True, 'name': True, 'complexity': True, 'notes': True}
        )

        # Customize the figure layout for a nicer appearance and unified hovermode
        predict_fig.update_layout(
            title="Predicted vs Actual Time over Date",
            xaxis_title="Date",
            yaxis_title="Time (Seconds)",
            hovermode="x unified",  # Show one hover box per x value
            template="plotly_white"  # Use a clean template
        )

        # Apply a hovertemplate to present data in a compact single-line text format
        predict_fig.update_traces(
            mode="markers+lines",
            hovertemplate=(
                "On %{x}, you predicted %{y[0]} seconds, but completed in %{y[1]} seconds.<br>"
                "Complexity: %{customdata[2]}<br>"
                "Notes: %{customdata[3]}<extra></extra>"
            )
        )
        st.plotly_chart(predict_fig)
    else:
        st.warning("No data available for today. Daily Problem not yet completed.")
        
    
if __name__ == '__main__':
    import pandas as pd
    data = {
        "date": [datetime.now() - timedelta(days=i) for i in range(5)],
        "time": [300, 350, 400, 450, 500]  # Sample times in seconds
    }
    df_filtered = pd.DataFrame(data)
    
    # Run the prediction page
    prediction_page(df_filtered)
