import streamlit as st
from etl import DataQuerier
from helper_functions import get_current_streak, get_daily_question
from queries import streak_query, streak_gpt_query
from datetime import datetime
import pytz

utc_time = datetime.utcnow()
eastern_tz = pytz.timezone('US/Eastern')
eastern_time = utc_time.replace(tzinfo=pytz.utc).astimezone(eastern_tz)

@st.cache_data(ttl=300) 
def get_data_from_db():
    querier = DataQuerier()

    # Fetch all required data
    df = querier.query("SELECT * FROM daily_problems ORDER BY date DESC")
    question_count = querier.query("SELECT COUNT(*) FROM daily_problems")
    streaks = querier.query(streak_query)
    gpt_streaks = querier.query(streak_gpt_query)
    querier.close()
    return df, question_count, streaks, gpt_streaks

def header():
    # Retrieve data using cached query
    df, question_count, streaks, gpt_streaks = get_data_from_db()
    gpt_streak  = get_current_streak(gpt_streaks)
    
    # Get streak data
    current_streak = get_current_streak(streaks)

    #gpt_streak = get_current_streak(gpt_streaks)
    if df.loc[0, "date"].date() == eastern_time.date() and df.loc[0,"chat_gpt"] == 1:
        gpt_streak = 0 
        
    max_streak = max(streaks["streak_length"])

    # Daily question info
    daily_question = get_daily_question(df)
    
    # Title and description
    st.markdown("""
        <div style="text-align: center;">
            <a href='https://leetcode.com'>
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/LeetCode_Logo_2.png" alt="LeetCode Logo">
            </a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; padding-top:-10px; padding-bottom: 20px;'>Daily Problem Progress</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; padding-bottom: 10px;'>Joshua Chen</h4>", unsafe_allow_html=True)
    st.markdown("""<p style='text-align: justify; font-size: 18px; padding-left: 30px; padding-right: 30px;'>     
                Welcome to my LeetCode Daily Progress tracker. This automated dashboard analyzes my performance, 
                scrapes and tracks daily problem data, and sets benchmark goals to help improve my skills.
                </p>""", unsafe_allow_html=True)

    space1, c1, space2, c2, space3 = st.columns([0.2,1,0.3, 1.5, 0.2]) 
    c1.markdown(f"""
        <div style='text-align:center; margin-bottom: 20px; width:100%; background-color: #2d2d2d; padding: 20px 30px 10px 30px; border-radius: 15px; 
                    box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);'>
            <p style='font-size: 16px; font-weight: 600; color: #f9f9f9; margin-bottom: 5px;'>Current Streak: {current_streak} days</p>
            <p style='font-size: 15px; color: #dddddd; margin-bottom: 5px;'>No-GPT Streak: {gpt_streak} days {"😠" if gpt_streak == 0 else ""}</p>
            <p style='font-size: 15px; color: #dddddd;'>Longest Streak: {max_streak} days</p>
        </div>
        """, unsafe_allow_html=True)

    c2.markdown(daily_question, unsafe_allow_html=True)
    

""" Welcome to my LeetCode Daily Progress tracker. Each day, I start with the LeetCode Daily Problem 
                to sharpen as a brain teaser and to improve my coding skills. LeetCode offers a variety of challenges 
                focused on algorithms and data structures, which has helped me grow as a programmer. Take a look at 
                how I’ve been progressing!"""