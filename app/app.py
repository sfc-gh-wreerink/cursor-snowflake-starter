import streamlit as st
import yaml
import os
from connector.snowflake_connection import get_connection

# Load config
if os.path.exists("config.yaml"):
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
else:
    config = {}

st.title("Snowflake Demo App")

query = st.text_input("Enter your SQL query:", config.get("default_query", "SELECT CURRENT_DATE;"))

if st.button("Run Query"):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()
        st.write(result)
