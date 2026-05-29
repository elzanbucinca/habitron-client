"""
Weekly Summary page - Display AI-generated weekly reflection.

Shows:
- AI-generated summary of the past week
- Highlights wins and areas to improve
- Confidence indicator based on data quality
"""

import streamlit as st

from src.services.api_client import client


def render(user_key):
    """
    Render the weekly summary page.

    Calls the AI weekly-summary endpoint and displays the result
    in a friendly, easy-to-read format with emojis.

    Args:
        user_key (str): GUID of the logged-in user.
    """
    st.header(':material/calendar_today: Weekly Summary')

    st.markdown(
        'Here\'s your personalized reflection on the past week, '
        'powered by AI.'
    )

    try:
        with st.spinner('Generating your weekly summary...'):
            response = client.get_weekly_summary(user_key)

        summary = response.get('summary', '')
        confidence = response.get('confidence', 'low')

        if not summary:
            st.info(
                '📝 No summary available yet. '
                'Log more habits to get personalized insights!'
            )
            return

        # Display confidence indicator
        confidence_display = _get_confidence_display(confidence)
        st.caption(f'Confidence: {confidence_display}')

        # Display summary in a styled container
        st.markdown('---')
        st.markdown(summary)
        st.markdown('---')

        # Add encouragement based on confidence
        if confidence == 'low':
            st.info(
                '💡 **Tip:** Log habits for at least 7 days '
                'to get more accurate insights!'
            )

    except Exception as error:
        st.error(f'Unable to load weekly summary: {error}')
        st.info(
            'Make sure the API is running and you have logged '
            'some habit data.'
        )


def _get_confidence_display(confidence):
    """
    Convert confidence level to a friendly display string.

    Args:
        confidence (str): Confidence level ('high', 'medium', 'low').

    Returns:
        str: Emoji and text representation of confidence.
    """
    confidence_map = {
        'high': '🟢 High (14+ days of data)',
        'medium': '🟡 Medium (7-13 days of data)',
        'low': '🔴 Low (less than 7 days of data)'
    }
    return confidence_map.get(confidence, '⚪ Unknown')
