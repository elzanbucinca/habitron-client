"""
Unusual Days page - Display days with unusual habit patterns.

Shows:
- Days where habits deviated significantly from normal
- Plain English explanations of what was unusual
"""

import streamlit as st

from src.services.api_client import client
from src.ui.components.insight_card import render_insight_card


# Default threshold for anomaly detection (hidden from user)
DEFAULT_THRESHOLD = 2.5


def render():
    """
    Render the unusual days page.
    """
    st.header('Unusual Days')

    st.markdown(
        'Days where your habits were significantly different from '
        'your usual patterns.'
    )

    try:
        current_user = st.session_state.get('current_user')
        user_key = current_user['key']
        response = client.detect_anomalies(user_key, DEFAULT_THRESHOLD)
        anomalies = response.get('anomalies', [])
        count = response.get('count', 0)

        if not anomalies:
            st.info(
                'No unusual days detected. Your habits have been '
                'consistent lately.'
            )
            return

        st.markdown(f'Found **{count}** unusual day(s) in your data.')
        st.markdown('---')

        # Display each anomaly as a card
        for anomaly in anomalies[:10]:
            _render_anomaly_card(anomaly)

    except Exception as error:
        st.error(f'Unable to load unusual days: {error}')


def _render_anomaly_card(anomaly):
    """
    Render a single anomaly as an insight card.

    Args:
        anomaly (dict): Anomaly data with date, unusual_habits, record.
    """
    date = anomaly.get('date', 'Unknown date')
    unusual_habits = anomaly.get('unusual_habits', [])

    # Build description from unusual habits
    descriptions = []
    for habit_info in unusual_habits:
        description = _format_unusual_habit(habit_info)
        if description:
            descriptions.append(description)

    if descriptions:
        description_text = '. '.join(descriptions) + '.'
    else:
        description_text = 'Some habits were outside your normal range.'

    render_insight_card(
        title=f'Date: {date}',
        description=description_text,
        card_type='warning'
    )


def _format_unusual_habit(habit_info):
    """
    Format an unusual habit into plain English.

    Args:
        habit_info (dict): Dictionary with 'habit', 'value', and
                          'z_score' keys.

    Returns:
        str: Human-readable description of the anomaly.
    """
    habit_labels = {
        'sleep_hours': 'Sleep',
        'focus_hours': 'Focus time',
        'exercise_minutes': 'Exercise',
        'mood': 'Mood',
        'screen_time_hours': 'Screen time',
        'diet_quality': 'Diet quality',
        'productivity_score': 'Productivity'
    }

    habit_name = habit_info.get('habit', '')
    label = habit_labels.get(habit_name, habit_name.replace('_', ' ').title())
    value = habit_info.get('value', 0)
    z_score = habit_info.get('z_score', 0)

    # Determine direction and magnitude
    if z_score > 0:
        direction = 'higher'
    else:
        direction = 'lower'

    magnitude = abs(z_score)
    if magnitude > 3:
        intensity = 'much'
    elif magnitude > 2:
        intensity = 'significantly'
    else:
        intensity = 'somewhat'

    # Format value based on habit type
    if habit_name in ['sleep_hours', 'focus_hours', 'screen_time_hours']:
        value_str = f'{value:.1f} hours'
    elif habit_name == 'exercise_minutes':
        value_str = f'{int(value)} minutes'
    else:
        value_str = str(int(value))

    return f'{label} was {intensity} {direction} than usual ({value_str})'
