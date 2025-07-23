# Cursor Snowflake Starter Demo App

## Project Overview

This project demonstrates a simple interactive web interface built with Streamlit that connects to Snowflake database for executing SQL queries.

## Requirements

Create an app called `app_cursor.py` in the appropriate app locaiton with the following functionality MAKE SURE IT IS A NEW APP:
Do not install the helpers imports

### Core Features

1. **SQL Query Input Interface**
   - Text area for inputting SQL queries
   - Default query: `SELECT CURRENT_DATE;`

2. **Query Execution**
   - Single button click to execute queries against Snowflake database
   - Real-time query processing

3. **Results Display**
   - View query results directly in the browser interface
   - Clean, formatted output

## Expected Behavior

### Application Access
- App runs at: `http://localhost:8501`
- Standard Streamlit web interface

### Successful Query Execution
- Execute valid SQL queries
- Display results in a user-friendly format
- Apply functionality to `app.py`

### Error Handling
The application should gracefully handle:
- Missing/invalid Snowflake credentials
- SQL syntax errors
- Connection timeouts
- Permission issues

## Implementation Notes

- Ensure proper error messaging for all failure scenarios
- Maintain clean, intuitive user interface