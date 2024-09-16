import plotly.express as px
import streamlit as st

def time_page(df_filtered):
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



