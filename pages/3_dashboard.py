import streamlit as st
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.components.dashboard import dashboard_page

st.set_page_config(
    page_title="Dashboard | Fitness Tracker",
    page_icon="📊",
    layout="wide"
)

dashboard_page()