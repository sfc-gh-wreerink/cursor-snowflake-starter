import streamlit as st
import os
import snowflake.connector

from dotenv import load_dotenv
load_dotenv()

# Streamlit UI
st.title("Snowflake Demo App")

query = st.text_area("Enter your SQL query:", "SELECT CURRENT_DATE;")
run_button = st.button("Run Query")

# Only run if button is clicked
if run_button:
    try:
        # Establish connection from env vars (set manually or via secrets manager)
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
        )

        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
            st.write("✅ Query Result:")
            st.write(result)

        conn.close()

    except Exception as e:
        st.error(f"❌ Error running query: {e}")
