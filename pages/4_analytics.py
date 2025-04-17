import streamlit as st
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.components.analytics import analytics_page

st.set_page_config(
    page_title="Analytics | Fitness Tracker",
    page_icon="📈",
    layout="wide"
)

analytics_page()