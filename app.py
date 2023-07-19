import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import xgboost
from xgboost import XGBRegressor
# Load the model pipeline
from PIL import Image

pipe = pickle.load(open('pipe.pkl', 'rb'))

# Define the options for teams and cities
teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa',
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]

cities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town',
    'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban',
    'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion',
    'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton',
    'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi', 'Nagpur',
    'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff',
    'Christchurch', 'Trinidad'
]

# Set page title and background color
st.set_page_config(page_title='Cricket Score Predictor', page_icon=':cricket:', layout='wide', initial_sidebar_state='collapsed')
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F2F6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set app title and header
st.title('Cricket Score Predictor')
st.markdown('<h2 style="color: #1E88E5;">Predict the T20 Score</h2>', unsafe_allow_html=True)


image = Image.open('image20.jpg')
st.image(image, use_column_width=False)

# Set up layout using columns
col1, col2 = st.columns(2)

# Team selection
with col1:
    batting_team = st.selectbox('Select batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select bowling team', sorted(teams))

# City selection
city = st.selectbox('Select city', sorted(cities))

# Inputs for score prediction
col3, col4, col5 = st.columns(3)

with col3:
    current_score = st.number_input('Current Score')
with col4:
    overs = st.number_input('Overs done (works for over > 5)')
with col5:
    wickets = st.number_input('Wickets out')

last_five = st.number_input('Runs scored in last 5 overs')

# Prediction button
if st.button('Predict Score'):
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = current_score / overs

    # Create input DataFrame for prediction
    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [city],
        'current_score': [current_score],
        'balls_left': [balls_left],
        'wickets_left': [wickets],
        'crr': [crr],
        'last_five': [last_five]
    })

    # Perform prediction
    result = pipe.predict(input_df)

    # Display predicted score
    st.markdown('<h3 style="color: #2ECC71;">Predicted Score: {}</h3>'.format(int(result[0])), unsafe_allow_html=True)


# #---------------------------------------------------------------------------------------
# # Import Excel file
# st.title("Data Analysis")
# df = pd.read_excel(io='T20.xlsx', sheet_name='Sheet1', engine='openpyxl', nrows=38478)
# st.sidebar.title("Dashbord")
# st.sidebar.image('image20_2.jpg', use_column_width=True)
# st.sidebar.write("Get sum of Total Score in T20 matches done by individual team")
#
# if st.sidebar.button("Get Total Run"):
#     grouped_df = df.groupby('batting_team')['runs_x'].sum().sort_values(ascending=False)
#     # Create a colorful pie chart using Plotly Express
#     fig = px.pie(grouped_df, values='runs_x', names=grouped_df.index, title='Total Score by Team')
#     fig.update_traces(textposition='inside', textinfo='percent+label')
#     fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
#     fig.update_layout(coloraxis_showscale=False)
#     st.plotly_chart(fig)
# #---------------------------------------------------------------------------------------
# st.sidebar.write("Get Max Score in T20 matches done by individual team")
# if st.sidebar.button("Get Max Run"):
#     grouped_df1 = df.groupby('batting_team')['runs_x'].max().sort_values(ascending=False)
#
#     # Create a colorful bar chart using Plotly Express
#     fig1 = px.bar(grouped_df1, title='Max Score by Team')
#     fig1.update_layout(xaxis_title='Team', yaxis_title='Max Runs')
#     fig1.update_traces(marker_color=['#FFA07A', '#FF4500', '#FF6347', '#FF7F50'])
#     fig1.update_layout(plot_bgcolor='white')
#     st.plotly_chart(fig1)
#
# #---------------------------------------------------------------------------------------
# st.sidebar.write("Get Max Run Rate in T20 matches of individual team")
# if st.sidebar.button("Get Max Run Rate"):
#     grouped_df2 = df.groupby('batting_team')['crr'].max().sort_values(ascending=False)
#
#     # Create a colorful bar chart using Plotly Express
#     fig2 = px.bar(grouped_df2, title='Max Run Rate by Team')
#     fig2.update_layout(xaxis_title='Team', yaxis_title='Max CRR')
#     fig2.update_traces(marker_color=['#9370DB', '#8A2BE2', '#800080', '#9932CC'])
#     fig2.update_layout(plot_bgcolor='white')
#     st.plotly_chart(fig2)
#
# #---------------------------------------------------------------------------------------
#
#
# # Group the data by batting_teams and wickets_left, calculate the maximum values, and sort the results
# grouped_df = df.groupby(['batting_team', 'wickets_left']).agg({'runs_x': 'max', 'crr': 'max'}).reset_index()
# grouped_df_sorted = grouped_df.sort_values(['runs_x', 'crr'], ascending=False)
#
# # Main Streamlit app
# def main():
#
#     st.write("Select a batting team and press 'Run Analysis' to perform analysis.")
#
#     # Selectbox for batting team
#     batting_teams = grouped_df_sorted['batting_team'].unique()
#     selected_batting_team = st.selectbox("Select Batting Team", batting_teams)
#
#     # Run Analysis button
#     if st.sidebar.button("Run Analysis"):
#         if selected_batting_team:
#             # Filter the grouped and sorted DataFrame based on selected batting team
#             filtered_df = grouped_df_sorted[grouped_df_sorted['batting_team'] == selected_batting_team]
#
#             # Display the filtered DataFrame
#             st.dataframe(filtered_df)
#
#             # Plotting the bar chart with eye-catching and colorful styles
#             fig3 = go.Figure()
#             fig3.add_trace(go.Bar(x=filtered_df['wickets_left'], y=filtered_df['runs_x'], name='Runs_x',
#                                   marker_color='#FFA07A'))
#             fig3.add_trace(go.Bar(x=filtered_df['wickets_left'], y=filtered_df['crr'], name='CRR',
#                                   marker_color='#9370DB'))
#             fig3.update_layout(barmode='group', plot_bgcolor='#F0F2F6', paper_bgcolor='#F0F2F6')
#             fig3.update_xaxes(showline=True, linewidth=1, linecolor='#333333')
#             fig3.update_yaxes(showline=True, linewidth=1, linecolor='#333333')
#             fig3.update_layout(title='Max Runs and CRR by Wickets Left', xaxis_title='Wickets Left',
#                                yaxis_title='Values', font=dict(family='Arial', size=12, color='#333333'))
#             fig3.update_traces(hovertemplate='<b>%{x}</b><br>%{y}', textposition='auto', textfont=dict(color='white'))
#
#             st.plotly_chart(fig3)
#         else:
#             st.warning("Please select a batting team before running the analysis.")
#
# # Run the app
# if __name__ == "__main__":
#     main()
#
# #---------------------------------------------------------------------------------------
