import streamlit as st
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the goals page functions
from pages.components.goals import goals_page

# Set page config
st.set_page_config(
    page_title="Goal Tracking | Fitness Tracker",
    page_icon="🎯",
    layout="wide"
)

# Display the goals page
goals_page()