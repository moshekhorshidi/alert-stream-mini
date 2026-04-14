import streamlit as st
import pandas as pd
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Alert Stream Mini",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Alert Stream Mini - Dashboard")
st.markdown("Welcome to the Alert Stream Mini management console.")

# --- Data Directory Setup ---
# This points to the /data volume mounted by Docker
DATA_DIR = "/data"

# Create dummy file tables if they don't exist yet
def init_dummy_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    users_file = os.path.join(DATA_DIR, "users.csv")
    if not os.path.exists(users_file):
        pd.DataFrame({
            "id": [1, 2],
            "name": ["Alice Admin", "Bob Developer"],
            "email": ["alice@example.com", "bob@example.com"]
        }).to_csv(users_file, index=False)
        
    groups_file = os.path.join(DATA_DIR, "users_groups.csv")
    if not os.path.exists(groups_file):
        pd.DataFrame({
            "role_int": [100, 200],
            "group_name": ["SuperAdmins", "DevOps"]
        }).to_csv(groups_file, index=False)

    alerts_file = os.path.join(DATA_DIR, "alerts_config.csv")
    if not os.path.exists(alerts_file):
        pd.DataFrame({
            "alert_id": [1],
            "alert_name": ["Sample Alert"],
            "table_name": ["metrics"],
            "severity": ["HIGH"],
            "threshold_value": [90.0],
            "json_config": ['{"query":"SELECT * FROM metrics WHERE cpu_usage > 90","severity":"HIGH"}']
        }).to_csv(alerts_file, index=False)

init_dummy_data()

# --- Display File Tables ---
st.subheader("Backend File Tables")
col1, col2 = st.columns(2)

with col1:
    st.write("**Users Table**")
    st.dataframe(pd.read_csv(os.path.join(DATA_DIR, "users.csv")), use_container_width=True)

with col2:
    st.write("**Users Groups Table**")
    st.dataframe(pd.read_csv(os.path.join(DATA_DIR, "users_groups.csv")), use_container_width=True)

st.write("**Alerts Config Table**")
st.dataframe(pd.read_csv(os.path.join(DATA_DIR, "alerts_config.csv")), use_container_width=True)

st.info("Use the sidebar to navigate to the Alert Generator.")