# Snowflake Analytics Studio - Enhanced with fancy UI and persistent connections
# Test comment: Authentication setup verified! 🎉

import streamlit as st
import os
import snowflake.connector
import pandas as pd
from datetime import datetime
import time

from dotenv import load_dotenv
load_dotenv()

# Initialize session state for connection
if 'snowflake_connection' not in st.session_state:
    st.session_state.snowflake_connection = None
if 'connection_status' not in st.session_state:
    st.session_state.connection_status = "Disconnected"

# Custom CSS for fancy styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        animation: fadeInDown 1s ease-out;
    }
    
    .main-header h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .connection-container {
        background: linear-gradient(145deg, #e8f4fd, #ffffff);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border: 2px solid rgba(102, 126, 234, 0.2);
        margin-bottom: 2rem;
        animation: slideInDown 0.6s ease-out;
    }
    
    .query-container {
        background: linear-gradient(145deg, #f0f2f6, #ffffff);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 2rem;
        animation: slideInLeft 0.8s ease-out;
    }
    
    .results-container {
        background: linear-gradient(145deg, #ffffff, #f8fafc);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideInRight 0.8s ease-out;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        margin: 1rem 0;
        transform: translateY(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .snowflake-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        animation: spin 10s linear infinite;
    }
    
    .status-success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        animation: bounceIn 0.6s ease-out;
    }
    
    .status-error {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        animation: shake 0.5s ease-out;
    }
    
    .status-connected {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        animation: bounceIn 0.6s ease-out;
    }
    
    .status-disconnected {
        background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    @keyframes fadeInDown {
        0% { opacity: 0; transform: translateY(-50px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInDown {
        0% { opacity: 0; transform: translateY(-30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInLeft {
        0% { opacity: 0; transform: translateX(-50px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        0% { opacity: 0; transform: translateX(50px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
        20%, 40%, 60%, 80% { transform: translateX(10px); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        font-family: 'Consolas', monospace;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 1rem;
    }
    
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Main header with fancy styling
st.markdown("""
<div class="main-header">
    <div class="snowflake-icon">❄️</div>
    <h1>Snowflake Analytics Studio</h1>
    <p>Professional Data Query Interface with Advanced Visualization</p>
</div>
""", unsafe_allow_html=True)

# Connection Management Section
st.markdown('<div class="connection-container">', unsafe_allow_html=True)
st.markdown("### 🔌 Connection Management")

col_connect, col_status = st.columns([1, 2])

with col_connect:
    connect_button = st.button("🔑 Connect to Snowflake", type="primary")
    disconnect_button = st.button("🔌 Disconnect")

with col_status:
    if st.session_state.connection_status == "Connected":
        st.markdown("""
        <div class="status-connected">
            <h4>✅ Connected to Snowflake</h4>
            <p>Ready to execute queries without MFA!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-disconnected">
            <h4>⚠️ Not Connected</h4>
            <p>Click "Connect to Snowflake" to authenticate (MFA required once)</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle connection button
if connect_button:
    try:
        with st.spinner("🔐 Connecting to Snowflake (MFA may be required)..."):
            # Create connection with MFA
            conn = snowflake.connector.connect(
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA"),
            )
            
            # Test the connection
            with conn.cursor() as cur:
                cur.execute("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()")
                test_result = cur.fetchone()
            
            # Store in session state
            st.session_state.snowflake_connection = conn
            st.session_state.connection_status = "Connected"
            st.session_state.connection_time = datetime.now()
            st.session_state.user_info = test_result
            
            st.success("🎉 Successfully connected to Snowflake! No more MFA needed for queries.")
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Failed to connect: {str(e)}")
        st.session_state.snowflake_connection = None
        st.session_state.connection_status = "Disconnected"

# Handle disconnect button
if disconnect_button:
    if st.session_state.snowflake_connection:
        try:
            st.session_state.snowflake_connection.close()
        except:
            pass
    st.session_state.snowflake_connection = None
    st.session_state.connection_status = "Disconnected"
    st.success("✅ Disconnected from Snowflake")
    st.rerun()

# Sidebar with additional information
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h3>🚀 Features</h3>
        <ul>
            <li>One-time MFA authentication</li>
            <li>Persistent connection</li>
            <li>Advanced result visualization</li>
            <li>Error handling & validation</li>
            <li>Performance metrics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Current time display
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    <div class="feature-card">
        <h4>🕐 Current Time</h4>
        <p>{current_time}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Connection status and info
    if st.session_state.connection_status == "Connected" and hasattr(st.session_state, 'user_info'):
        user_info = st.session_state.user_info
        connection_time = st.session_state.connection_time.strftime("%H:%M:%S")
        st.markdown(f"""
        <div class="metric-card">
            <h4>👤 Connection Info</h4>
            <p><strong>User:</strong> {user_info[0]}</p>
            <p><strong>Role:</strong> {user_info[1]}</p>
            <p><strong>Warehouse:</strong> {user_info[2]}</p>
            <p><strong>Connected:</strong> {connection_time}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Connection Status</h4>
            <p>Not Connected</p>
        </div>
        """, unsafe_allow_html=True)

# Main content area - only show if connected
if st.session_state.connection_status == "Connected":
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="query-container">', unsafe_allow_html=True)
        st.markdown("### 📝 SQL Query Editor")
        
        # Sample queries in an expander
        with st.expander("💡 Sample Queries", expanded=False):
            sample_queries = {
                "Current Date": "SELECT CURRENT_DATE();",
                "System Info": "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE();",
                "Time Functions": "SELECT CURRENT_TIMESTAMP(), DATEADD('day', -7, CURRENT_DATE()) as WEEK_AGO;",
                "Random Data": "SELECT UNIFORM(1, 100, RANDOM()) as RANDOM_NUMBER, 'Sample Data' as TEXT_COLUMN;"
            }
            
            selected_query = st.selectbox("Choose a sample query:", list(sample_queries.keys()))
            if st.button("📋 Use Sample Query"):
                st.session_state.query = sample_queries[selected_query]
        
        # Query input with session state
        if 'query' not in st.session_state:
            st.session_state.query = "SELECT CURRENT_DATE();"
        
        query = st.text_area(
            "Enter your SQL query:", 
            value=st.session_state.query,
            height=150,
            placeholder="Write your SQL query here..."
        )
        
        # Fancy run button
        run_button = st.button("🚀 Execute Query", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>⚡ Quick Stats</h4>
            <p>Query Length: <strong>{} chars</strong></p>
            <p>Lines: <strong>{}</strong></p>
        </div>
        """.format(len(query), len(query.split('\n'))), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🎯 Pro Tips</h4>
            <ul style="text-align: left; font-size: 0.9rem;">
                <li>Use LIMIT for large datasets</li>
                <li>Check query syntax before running</li>
                <li>Optimize with indexes</li>
                <li>No MFA needed - connection persists!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Query execution with enhanced visual feedback
    if run_button:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        # Progress bar with custom styling
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Check if connection is still alive
            if not st.session_state.snowflake_connection or st.session_state.snowflake_connection.is_closed():
                st.error("❌ Connection lost. Please reconnect.")
                st.session_state.connection_status = "Disconnected"
                st.session_state.snowflake_connection = None
                st.rerun()
            
            # Simulate progress updates (faster since no connection needed)
            for i in range(101):
                progress_bar.progress(i)
                if i < 20:
                    status_text.text("📤 Sending query...")
                elif i < 80:
                    status_text.text("⚙️ Processing results...")
                else:
                    status_text.text("✅ Complete!")
                time.sleep(0.005)  # Faster since no connection overhead
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            start_time = time.time()
            
            # Use existing connection (no MFA needed!)
            with st.session_state.snowflake_connection.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                columns = [desc[0] for desc in cur.description] if cur.description else []
                
            execution_time = time.time() - start_time
            
            # Success message with animation
            st.markdown("""
            <div class="status-success">
                <h3>🎉 Query Executed Successfully!</h3>
                <p>Execution time: <strong>{:.3f} seconds</strong> (No MFA required!)</p>
                <p>Rows returned: <strong>{}</strong></p>
            </div>
            """.format(execution_time, len(result)), unsafe_allow_html=True)
            
            # Display results in a fancy way
            if result:
                st.markdown("### 📊 Query Results")
                
                # Convert to DataFrame for better display
                if columns:
                    df = pd.DataFrame(result, columns=columns)
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🔢 Total Rows", len(df))
                    with col2:
                        st.metric("📝 Columns", len(df.columns))
                    with col3:
                        st.metric("⚡ Exec Time", f"{execution_time:.3f}s")
                    
                    # Enhanced dataframe display
                    st.dataframe(
                        df, 
                        use_container_width=True,
                        height=min(400, len(df) * 35 + 100)
                    )
                    
                    # Download button for results
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"snowflake_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                else:
                    # For queries without results (like DDL)
                    st.success("✅ Query executed successfully (no results to display)")
            else:
                st.info("ℹ️ Query executed successfully but returned no results")

        except Exception as e:
            # Clear progress indicators on error
            progress_bar.empty()
            status_text.empty()
            
            # Check if it's a connection error
            if "not connected" in str(e).lower() or "connection" in str(e).lower():
                st.session_state.connection_status = "Disconnected"
                st.session_state.snowflake_connection = None
                st.error("❌ Connection lost. Please reconnect using the button above.")
            else:
                # Enhanced error display
                st.markdown(f"""
                <div class="status-error">
                    <h3>❌ Query Execution Failed</h3>
                    <p><strong>Error:</strong> {str(e)}</p>
                    <p>Please check your query syntax.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Error troubleshooting tips
                with st.expander("🔧 Troubleshooting Tips"):
                    st.markdown("""
                    - **Syntax Error**: Check SQL syntax and table/column names
                    - **Permission Error**: Ensure you have access to the requested resources
                    - **Timeout Error**: Try simplifying your query or adding LIMIT clause
                    """)
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Show message when not connected
    st.markdown("""
    <div class="query-container">
        <h3>🔐 Please Connect First</h3>
        <p>Click the "Connect to Snowflake" button above to authenticate with MFA once, then you can run unlimited queries without additional authentication!</p>
        
        <h4>✨ Benefits of Persistent Connection:</h4>
        <ul>
            <li>🚀 <strong>One-time MFA</strong> - Authenticate once per session</li>
            <li>⚡ <strong>Faster queries</strong> - No connection overhead</li>
            <li>🔒 <strong>Secure</strong> - Connection remains encrypted</li>
            <li>🎯 <strong>Seamless</strong> - Run multiple queries instantly</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer with additional fancy elements
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    <div class="metric-card">
        <h4>🏢 Environment</h4>
        <p>Production Ready</p>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.markdown("""
    <div class="metric-card">
        <h4>🔒 Security</h4>
        <p>Encrypted Connection</p>
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    st.markdown("""
    <div class="metric-card">
        <h4>⚡ Performance</h4>
        <p>Optimized Queries</p>
    </div>
    """, unsafe_allow_html=True)

# Floating particles animation (pure CSS)
st.markdown("""
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;">
    <div style="position: absolute; top: 20%; left: 10%; width: 4px; height: 4px; background: rgba(102, 126, 234, 0.3); border-radius: 50%; animation: float 6s ease-in-out infinite;"></div>
    <div style="position: absolute; top: 60%; right: 10%; width: 6px; height: 6px; background: rgba(118, 75, 162, 0.3); border-radius: 50%; animation: float 8s ease-in-out infinite reverse;"></div>
    <div style="position: absolute; bottom: 20%; left: 20%; width: 3px; height: 3px; background: rgba(132, 250, 176, 0.4); border-radius: 50%; animation: float 10s ease-in-out infinite;"></div>
</div>

<style>
@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(180deg); }
}
</style>
""", unsafe_allow_html=True)
