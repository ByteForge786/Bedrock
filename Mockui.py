import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import streamlit as st
import os
from datetime import datetime
import hashlib
import logging
import plotly.express as px

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set page config
st.set_page_config(page_title="NeuroFlake", layout="wide", initial_sidebar_state="collapsed")

# Constants
CSV_FILE = 'user_interactions.csv'
MAX_RETRIES = 3

# Initialize CSV file
def init_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['timestamp', 'question', 'result', 'upvote', 'downvote', 'session_id'])
        df.to_csv(CSV_FILE, index=False)

# Load CSV file
@st.cache_data
def load_data():
    for _ in range(MAX_RETRIES):
        try:
            data = pd.read_csv(CSV_FILE, parse_dates=['timestamp'])
            return data
        except pd.errors.EmptyDataError:
            logging.warning(f"CSV file {CSV_FILE} is empty. Initializing with header.")
            init_csv()
        except Exception as e:
            logging.error(f"Error loading CSV: {str(e)}")
    return pd.DataFrame()  # Return empty DataFrame if all retries fail

# Append data to CSV
def append_to_csv(new_data):
    for _ in range(MAX_RETRIES):
        try:
            with open(CSV_FILE, 'a', newline='') as f:
                new_data.to_csv(f, header=f.tell() == 0, index=False)
            return True
        except Exception as e:
            logging.error(f"Error appending to CSV: {str(e)}")
    return False

# Generate a session ID
def generate_session_id():
    return hashlib.md5(str(datetime.now()).encode()).hexdigest()

# Initialize app
def init_app():
    init_csv()
    if 'chat' not in st.session_state:
        st.session_state['chat'] = []
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = generate_session_id()

# Mock function for SQL generation (replace with actual implementation)
def generate_sql(question):
    return f"SELECT * FROM sample_table WHERE condition = '{question}';"

# Mock function for query execution (replace with actual implementation)
def execute_query(sql):
    return "Query executed successfully. 5 rows returned."

# Handle user interaction
def handle_interaction(question, result):
    new_data = pd.DataFrame({
        'timestamp': [datetime.now()],
        'question': [question.strip().replace('\n', ' ')],
        'result': [result.strip().replace('\n', ' ')],
        'upvote': [0],
        'downvote': [0],
        'session_id': [st.session_state['session_id']]
    })
    append_to_csv(new_data)

# Main Streamlit app logic
init_app()
data = load_data()

st.title("NeuroFlake Chatbot")

# User input section
user_input = st.text_input("Ask a question:")
if st.button("Submit") and user_input:
    sql_query = generate_sql(user_input)
    response = execute_query(sql_query)
    
    # Display response and save interaction
    st.write(f"Generated SQL: {sql_query}")
    st.write(response)
    
    # Append the interaction to chat history
    st.session_state['chat'].append({'question': user_input, 'result': response})
    handle_interaction(user_input, response)

# Display chat history with upvote/downvote
for i, entry in enumerate(st.session_state['chat']):
    st.write(f"**Q{i+1}:** {entry['question']}")
    st.write(f"**A{i+1}:** {entry['result']}")
    
    # Upvote and downvote buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"Upvote {i+1}"):
            data.loc[data['question'] == entry['question'], 'upvote'] += 1
            data.to_csv(CSV_FILE, index=False)
    with col2:
        if st.button(f"Downvote {i+1}"):
            data.loc[data['question'] == entry['question'], 'downvote'] += 1
            data.to_csv(CSV_FILE, index=False)

# Display interaction graph
if not data.empty:
    fig = px.bar(data, x='timestamp', y=['upvote', 'downvote'], title="User Interaction Over Time")
    st.plotly_chart(fig)
