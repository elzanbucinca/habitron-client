"""
Metric display component.

Displays metrics in plain English instead of raw numbers.
Converts technical values to human-readable interpretations.
"""

import streamlit as st


def render_probability_metric(probability, context='productivity'):
    """
    Display a probability value in plain English.

    Args:
        probability (float): Value between 0 and 1.
        context (str): What the probability refers to
                      (e.g., 'productivity', 'good day').

    Returns:
        None. Renders the metric directly to Streamlit.
    """
    percentage = int(probability * 100)

    # Determine interpretation
    if percentage >= 80:
        interpretation = 'Very likely'
        color = '#00c853'
    elif percentage >= 60:
        interpretation = 'Looking good'
        color = '#64dd17'
    elif percentage >= 40:
        interpretation = 'Could go either way'
        color = '#ffc107'
    elif percentage >= 20:
        interpretation = 'Less likely'
        color = '#ff9800'
    else:
        interpretation = 'Unlikely'
        color = '#f44336'

    st.markdown(
        f'<span style="color: {color}; font-size: 1.5rem; '
        f'font-weight: 600;">{percentage}%</span>',
        unsafe_allow_html=True
    )
    st.markdown(f'**{interpretation}** to have a {context}')


def render_confidence_indicator(confidence):
    """
    Display a confidence level with explanation.

    Args:
        confidence (str): One of 'high', 'medium', 'low'.

    Returns:
        None. Renders the indicator directly to Streamlit.
    """
    confidence_info = {
        'high': {
            'label': 'High confidence',
            'description': 'Based on 14+ days of your data',
            'color': '#00c853'
        },
        'medium': {
            'label': 'Medium confidence',
            'description': 'Based on 7-13 days of your data',
            'color': '#ffc107'
        },
        'low': {
            'label': 'Low confidence',
            'description': 'Less than 7 days of data available',
            'color': '#f44336'
        }
    }

    info = confidence_info.get(confidence, confidence_info['low'])

    st.caption(
        f'<span style="color: {info["color"]};">{info["label"]}</span> '
        f'- {info["description"]}',
        unsafe_allow_html=True
    )


def render_prediction_summary(prediction, probability):
    """
    Display a prediction with visual indicator.

    Args:
        prediction (str): Either 'good' or 'bad'.
        probability (float): Probability value between 0 and 1.

    Returns:
        None. Renders the summary directly to Streamlit.
    """
    percentage = int(probability * 100)

    if prediction == 'good':
        icon = 'check_circle'
        color = '#00c853'
        label = 'Productive day ahead'
    else:
        icon = 'warning'
        color = '#ff9800'
        label = 'May be challenging'

    st.markdown(
        f'<div style="display: flex; align-items: center; gap: 0.5rem;">'
        f'<span class="material-icons" style="color: {color}; '
        f'font-size: 2rem;">:{icon}:</span>'
        f'<div>'
        f'<div style="font-size: 1.25rem; font-weight: 600;">{label}</div>'
        f'<div style="color: #666;">{percentage}% chance of a good day</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def format_habit_value(habit_name, value):
    """
    Format a habit value for display.

    Args:
        habit_name (str): Name of the habit (e.g., 'sleep_hours').
        value: The value to format.

    Returns:
        str: Human-readable formatted value.
    """
    formatters = {
        'sleep_hours': lambda v: f'{v:.1f} hours of sleep',
        'focus_hours': lambda v: f'{v:.1f} hours of focus time',
        'exercise_minutes': lambda v: f'{int(v)} minutes of exercise',
        'mood': lambda v: f'Mood rating: {int(v)}/10',
        'screen_time_hours': lambda v: f'{v:.1f} hours of screen time',
        'diet_quality': lambda v: f'Diet quality: {int(v)}/10'
    }

    formatter = formatters.get(habit_name)
    if formatter:
        return formatter(value)

    return f'{habit_name}: {value}'
