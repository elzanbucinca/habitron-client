"""
AI Insights page - Display AI-generated insights.

Shows ranked insights from the backend including:
- Correlation insights
- Trend insights
- Anomaly insights
- Model insights
"""

import streamlit as st

from src.services.api_client import client


def render(data):
    """
    Render the insights page.

    Args:
        data: Dictionary with pre-loaded analysis data.
    """
    st.header(':material/lightbulb: AI Insights')

    if data is None:
        st.warning('No data available.')
        return

    try:
        insights = data.get('insights', [])
        total = data.get('total_insights', 0)

        st.write(f'Found {total} total insights')

        if insights:
            st.subheader('Top Insights (Ranked by Importance)')
            for item in insights[:10]:
                st.write(f"{item['rank']}. {item['insight']}")
        else:
            st.info('No insights generated yet.')
    except Exception as error:
        st.error(f'Error displaying insights: {error}')
