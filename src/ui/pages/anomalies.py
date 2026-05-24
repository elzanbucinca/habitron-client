"""
Anomalies page - Display unusual day detection results.

Shows:
- Anomalous habit records
- Unusual habit values
"""

import streamlit as st

from src.services.api_client import client


def render(data, threshold):
    """
    Render the anomalies page.

    Args:
        data: Dictionary with pre-loaded analysis data (unused for anomalies).
        threshold: Anomaly detection threshold.
    """
    st.header(':material/warning: Anomalies')

    try:
        current_user = st.session_state.get('current_user')
        user_key = current_user['key']
        anom_response = client.detect_anomalies(user_key, threshold)
        anomalies = anom_response.get('anomalies', [])
        count = anom_response.get('count', 0)

        st.write(f'Found {count} anomalies (threshold: {threshold})')

        if anomalies:
            for anomaly in anomalies[:10]:
                with st.expander(f"Date: {anomaly['date']}"):
                    st.write('Unusual habits:')
                    st.write(anomaly['unusual_habits'])
                    st.json(anomaly['record'])
        else:
            st.info('No anomalies detected.')
    except Exception as error:
        st.error(f'Error loading anomalies: {error}')
