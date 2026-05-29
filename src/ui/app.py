"""
Habitron – Interactive Streamlit Dashboard

Provides an interactive web interface to visualize habit data,
AI-generated insights, and habit recommendations.

The dashboard is organized into 3 sections:

DATA:
- Log Habits – Manual habit entry form
- View History – Raw data and statistics

INSIGHTS:
- Weekly Summary – AI-generated weekly reflection
- What's Working – Top habits and recommendations

AI ASSISTANT:
- Unusual Days – Anomaly detection (more features in Phase 4)
"""

import streamlit as st
import pandas as pd

from src.services.api_client import client
from src.ui.pages import (
    anomalies,
    ask_question,
    history,
    log_habits,
    login,
    predictions,
    weekly_summary,
    whats_working,
)
from src.ui.components.sidebar import render_sidebar


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title='Habitron Dashboard',
        page_icon='https://icons.getbootstrap.com/assets/icons/feather.svg',
        layout='wide',
        initial_sidebar_state='expanded'
    )


@st.cache_resource
def check_api_connection():
    """
    Check if API is running.

    Returns:
        bool: True if API is reachable, False otherwise.
    """
    try:
        client.health_check()
        return True
    except Exception:
        return False


@st.cache_data
def load_analysis_data(user_key):
    """
    Load all analysis data from API for a specific user.

    The user_key parameter is included in the cache key so that
    each user receives their own cached data.

    Args:
        user_key (str): GUID of the logged-in user.

    Returns:
        dict: Dictionary with all loaded data, or None if error.
    """
    try:
        # Load basic data
        data_response = client.load_data(user_key)

        if not data_response.get('data'):
            return None

        dataframe = pd.DataFrame(data_response['data'])
        dataframe['date'] = pd.to_datetime(dataframe['date'])
        dataframe = dataframe.set_index('date')

        # Load statistics
        stats_response = client.get_statistics(user_key)
        statistics = stats_response['statistics']

        # Load correlations
        corr_response = client.get_correlations(user_key)
        correlations = corr_response['correlations']

        # Load trends
        trends_response = client.get_trends(user_key)
        trends_data = trends_response['trends']

        return {
            'dataframe': dataframe,
            'statistics': statistics,
            'correlations': correlations,
            'trends': trends_data,
        }
    except Exception as error:
        st.error(f'Error loading data from API: {error}')
        return None


def main():
    """Main dashboard entry point."""
    setup_page_config()

    # Check API connection
    if not check_api_connection():
        st.error(
            'Cannot connect to API server. '
            'Make sure the API is running on '
            'http://localhost:5000'
        )
        st.info(
            'To start the API, run: python run_api.py'
        )
        return

    # Show registration form if email was entered but user not found
    pending_email = st.session_state.get('pending_email')
    if pending_email is not None:
        login.render_registration(pending_email)
        return

    # Block dashboard until user is logged in
    current_user = st.session_state.get('current_user')
    if current_user is None:
        login.render()
        return

    user_key = current_user['key']

    # Load all data from API
    analysis_data = load_analysis_data(user_key)

    # Render sidebar and get user selections
    sidebar_selections = render_sidebar(analysis_data)

    page = sidebar_selections['page']

    # Render selected page
    if page == 'Log Habits':
        log_habits.render(user_key)
    elif page == 'Weekly Summary':
        weekly_summary.render(user_key)
    elif page == "What's Working":
        correlations = None
        if analysis_data:
            correlations = analysis_data.get('correlations')
        whats_working.render(user_key, correlations)
    elif page == 'Ask a Question':
        ask_question.render(user_key)
    elif page == 'Predictions':
        predictions.render(user_key)
    elif page == 'Unusual Days':
        anomalies.render()
    elif analysis_data is None:
        st.info(
            'No habit data found for your account. '
            'Add records via the API to get started.'
        )
    elif page == 'View History':
        history.render(analysis_data)


if __name__ == '__main__':
    main()
