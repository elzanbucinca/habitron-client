"""
Frontend configuration and settings.

Defines API endpoint, UI settings, and application configuration.
"""

import os


def _resolve_api_url():
    """
    Resolve the backend API base URL.

    Checks Streamlit secrets first (used on Streamlit Cloud), then
    falls back to the API_URL environment variable, then to the
    local development default.

    Returns:
        str: Base URL of the backend API.
    """
    try:
        import streamlit as st
        url = st.secrets.get('API_URL')
        if url:
            return url
    except Exception:
        pass
    # return os.getenv('API_URL', 'http://localhost:5000')
    return os.getenv('API_URL', 'https://elzanbucincabarani.pythonanywhere.com')


class Config:
    """
    Configuration for Streamlit frontend.

    Defines API endpoint, UI settings, and application configuration.
    """

    # API Server settings
    API_URL = _resolve_api_url()
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 10))

    # UI settings
    PAGE_TITLE = 'Habitron Dashboard'
    PAGE_ICON = ':material/monitoring:'
    LAYOUT = 'wide'
