"""
Habitron – Interactive Streamlit Dashboard

Provides an interactive web interface to visualize habit data, analysis results,
anomalies, and AI-generated insights.

The dashboard is organized into 7 pages:
1. AI Insights – Generated insights and recommendations
2. Data Overview – Raw data and statistics
3. Correlation Analysis – Habit-productivity relationships
4. Trends & Patterns – Time-series visualization
5. Model & Predictions – ML model performance
6. Anomalies – Unusual day detection
7. Log Habits – Manual habit entry form
"""

import streamlit as st
import pandas as pd

from src.services.api_client import client
from src.ui.pages import (
    analysis,
    anomalies,
    data,
    log_habits,
    insights,
    login,
    model,
    trends,
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

        # Train model and get metrics
        model_response = client.train_model(user_key)
        metrics = model_response['metrics']
        coefficients = model_response['coefficients']

        # Load insights
        insights_response = client.get_all_insights(user_key)
        insights_list = insights_response.get('insights', [])
        total_insights = insights_response.get('total_insights', 0)

        return {
            'dataframe': dataframe,
            'statistics': statistics,
            'correlations': correlations,
            'trends': trends_data,
            'model_metrics': metrics,
            'coefficients': coefficients,
            'insights': insights_list,
            'total_insights': total_insights
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
    date_range = sidebar_selections['date_range']
    selected_habits = sidebar_selections['selected_habits']
    anomaly_threshold = sidebar_selections['anomaly_threshold']

    # Render selected page
    if page == 'Log Habits':
        log_habits.render(user_key)
    elif analysis_data is None:
        st.info(
            'No habit data found for your account. '
            'Add records via the API to get started.'
        )
    elif page == 'AI Insights':
        insights.render(analysis_data)
    elif page == 'Data Overview':
        data.render(analysis_data, date_range)
    elif page == 'Correlation Analysis':
        analysis.render(analysis_data)
    elif page == 'Trends & Patterns':
        trends.render(analysis_data, selected_habits)
    elif page == 'Model & Predictions':
        model.render(analysis_data)
    elif page == 'Anomalies':
        anomalies.render(analysis_data, anomaly_threshold)


if __name__ == '__main__':
    main()
