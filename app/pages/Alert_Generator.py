import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(page_title="Alert Generator", page_icon="⚙️", layout="wide")

st.title("⚙️ Generate Alert INSERT Script")
st.markdown("Use this tool to configure alert rows and generate the MySQL `START TRANSACTION` script.")

DATA_DIR = "/data"

# Load backend file tables for UI dropdowns
try:
    users_df = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))
    groups_df = pd.read_csv(os.path.join(DATA_DIR, "users_groups.csv"))
except FileNotFoundError:
    st.error("Data files not found. Please visit the main dashboard to initialize them.")
    st.stop()

# --- UI Inputs ---
with st.form("alert_generation_form"):
    st.subheader("1. Base Configurations")
    col1, col2 = st.columns(2)
    
    with col1:
        selected_user = st.selectbox("Select User", users_df['name'])
        user_id = users_df[users_df['name'] == selected_user]['id'].values[0]
        
    with col2:
        selected_group = st.selectbox("Select Group", groups_df['group_name'])
        role_int = groups_df[groups_df['group_name'] == selected_group]['role_int'].values[0]

    st.subheader("2. Alert Rules & Values")
    alert_name = st.text_input("Alert Name", value="CPU Spike Alert")
    threshold = st.number_input("Threshold Value", value=90.0)
    
    st.subheader("3. JSON Configuration Column")
    st.markdown("Input the SQL query and metadata that will be stored as JSON.")
    sql_query = st.text_area("SQL Trigger Query", value="SELECT * FROM metrics WHERE cpu_usage > 90;")
    alert_severity = st.selectbox("Severity", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])

    submitted = st.form_submit_button("Generate MySQL Script", type="primary")

# --- Script Generation ---
if submitted:
    # Build the JSON object structure
    json_config = {
        "query": sql_query,
        "severity": alert_severity,
        "metadata": {
            "created_by_app": "alert-stream-mini",
            "threshold_applied": threshold
        }
    }
    
    # Escape single quotes for safe SQL insertion
    safe_alert_name = alert_name.replace("'", "''")
    # Dump to JSON string and escape single quotes for SQL insertion
    json_str = json.dumps(json_config).replace("'", "''")

    # Generate the SQL Template
    sql_script = f"""-- =======================================================
-- Generated Alert Configuration Script
-- User ID: {user_id} | Group Role: {role_int}
-- =======================================================

START TRANSACTION;

-- Insert the configured alert row
INSERT INTO alerts_table (
    user_id, 
    group_role, 
    alert_name, 
    threshold_value, 
    json_config
) VALUES (
    {user_id},
    {role_int},
    '{safe_alert_name}',
    {threshold},
    '{json_str}'
);

COMMIT;
"""
    
    st.success("Script generated successfully!")
    st.code(sql_script, language="sql")
    
    st.download_button(
        label="Download .sql File",
        data=sql_script,
        file_name=f"insert_alert_{alert_name.replace(' ', '_').lower()}.sql",
        mime="text/plain"
    )