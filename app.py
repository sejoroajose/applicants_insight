import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px

# Fetch database connection details from Streamlit secrets
DB_HOST = st.secrets["database"]["DB_HOST"]
DB_NAME = st.secrets["database"]["DB_NAME"]
DB_USER = st.secrets["database"]["DB_USER"]
DB_PASSWORD = st.secrets["database"]["DB_PASSWORD"]

# Function to connect to PostgreSQL and fetch data
def fetch_data():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    # SQL query to get unique entries based on email, keeping only the latest entry
    query = """
    SELECT DISTINCT ON (email) * 
    FROM scholarship_applications
    ORDER BY email, updated_at DESC;
    """
    
    # Fetch the data into a DataFrame
    df = pd.read_sql(query, conn)
    
    # Close the connection
    conn.close()
    
    return df

# Load the data
df = fetch_data()

# Streamlit app
st.title("1000ttp Applicant Insights")


# Percentage of preferred programs
st.header("Percentage of Preferred Programs")
preferred_program_counts = df['preferred_program'].value_counts(normalize=True) * 100

# Data for pie chart
preferred_program_df = preferred_program_counts.reset_index()
preferred_program_df.columns = ['preferred_program', 'proportion']

# Bar chart and pie chart for preferred programs
st.bar_chart(preferred_program_counts)
preferred_program_fig = px.pie(
    preferred_program_df, 
    names='preferred_program', 
    values='proportion', 
    title='Preferred Program Distribution',
)
st.plotly_chart(preferred_program_fig)

# Percentage distribution of local governments
st.header("Percentage Distribution of Local Governments")
local_government_counts = df['local_government'].value_counts(normalize=True) * 100

# Data for pie chart
local_government_df = local_government_counts.reset_index()
local_government_df.columns = ['local_government', 'proportion']

# Bar chart and pie chart for local governments
st.bar_chart(local_government_counts)
local_government_fig = px.pie(
    local_government_df, 
    names='local_government', 
    values='proportion', 
    title='Local Government Distribution',
)
st.plotly_chart(local_government_fig)

# Score analysis by total count
st.header("Score Analysis (by Total Count)")
score_counts = df['score'].value_counts()

# Bar chart for score distribution
st.bar_chart(score_counts)

# Pie chart for score distribution
score_distribution_df = score_counts.reset_index()
score_distribution_df.columns = ['score', 'count']
score_distribution_fig = px.pie(
    score_distribution_df, 
    names='score', 
    values='count', 
    title='Score Distribution',
)
st.plotly_chart(score_distribution_fig)

# Score Distribution by Local Government
st.header("Score Distribution by Local Government")

# Group by local government and score
grouped_scores = df.groupby(['local_government', 'score']).size().reset_index(name='count')

# Loop through each local government and display score distribution
for lg in grouped_scores['local_government'].unique():
    st.subheader(f"Score Distribution in {lg}")
    lg_data = grouped_scores[grouped_scores['local_government'] == lg]
    score_lg_fig = px.bar(
        lg_data, 
        x='score', 
        y='count', 
        title=f"Score Distribution for {lg}", 
        color='score',
    )
    st.plotly_chart(score_lg_fig)

# Show the raw data if needed
if st.checkbox("Show raw data"):
    st.write(df)
