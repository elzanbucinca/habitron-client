"""
Predictions page - Tomorrow's outlook and what-if scenarios.

Shows:
- Prediction for tomorrow's productivity
- What-if scenario form to experiment with habit changes
"""

import streamlit as st

from src.services.api_client import client
from src.ui.components.metric_display import (
    render_probability_metric,
    render_confidence_indicator,
    format_habit_value
)


def render(user_key):
    """
    Render the Predictions page.

    Displays tomorrow's productivity prediction and allows
    users to experiment with what-if scenarios.

    Args:
        user_key (str): GUID of the logged-in user.
    """
    st.header('Predictions')

    st.markdown(
        'See what tomorrow might look like and experiment with '
        'different habit combinations.'
    )

    # Tomorrow's Outlook section
    _render_tomorrow_outlook(user_key)

    st.markdown('---')

    # What-If Scenarios section
    _render_what_if_section(user_key)


def _render_tomorrow_outlook(user_key):
    """
    Render the tomorrow's outlook section.

    Args:
        user_key (str): GUID of the logged-in user.
    """
    st.subheader("Tomorrow's Outlook")

    try:
        with st.spinner('Analyzing your habits...'):
            response = client.predict_tomorrow(user_key)

        # Handle insufficient data
        if response.get('prediction') is None:
            message = response.get(
                'message',
                'Not enough data for predictions yet.'
            )
            st.info(
                f'{message} Log at least 5 days of habits to unlock '
                'this feature.'
            )
            return

        prediction = response.get('prediction', 'unknown')
        probability = response.get('probability', 0.5)
        confidence = response.get('confidence', 'low')
        explanation = response.get('explanation', '')
        today_habits = response.get('today_habits', {})

        # Display prediction
        col1, col2 = st.columns([1, 2])

        with col1:
            render_probability_metric(probability, 'productive day')

        with col2:
            render_confidence_indicator(confidence)

            if explanation:
                st.markdown(f'**Why:** {explanation}')

        # Show habits used for prediction
        if today_habits:
            with st.expander('Based on your recent habits'):
                _display_habits(today_habits)

        # Refresh button
        if st.button('Refresh prediction', key='refresh_prediction'):
            st.rerun()

    except Exception as error:
        st.error(f'Unable to load prediction: {error}')


def _render_what_if_section(user_key):
    """
    Render the what-if scenario form.

    Args:
        user_key (str): GUID of the logged-in user.
    """
    st.subheader('What-If Scenarios')

    st.markdown(
        'Experiment with different habit values to see how they '
        'might affect your productivity.'
    )

    # Get default values from session state or use defaults
    defaults = st.session_state.get('what_if_defaults', {
        'sleep_hours': 7.0,
        'focus_hours': 4.0,
        'exercise_minutes': 30,
        'mood': 7,
        'screen_time_hours': 3.0,
        'diet_quality': 7
    })

    with st.form(key='what_if_form'):
        col1, col2 = st.columns(2)

        with col1:
            sleep_hours = st.slider(
                'Sleep (hours)',
                min_value=0.0,
                max_value=12.0,
                value=float(defaults.get('sleep_hours', 7.0)),
                step=0.5
            )

            focus_hours = st.slider(
                'Focus time (hours)',
                min_value=0.0,
                max_value=12.0,
                value=float(defaults.get('focus_hours', 4.0)),
                step=0.5
            )

            exercise_minutes = st.slider(
                'Exercise (minutes)',
                min_value=0,
                max_value=180,
                value=int(defaults.get('exercise_minutes', 30)),
                step=5
            )

        with col2:
            mood = st.slider(
                'Mood (1-10)',
                min_value=1,
                max_value=10,
                value=int(defaults.get('mood', 7))
            )

            screen_time_hours = st.slider(
                'Screen time (hours)',
                min_value=0.0,
                max_value=12.0,
                value=float(defaults.get('screen_time_hours', 3.0)),
                step=0.5
            )

            diet_quality = st.slider(
                'Diet quality (1-10)',
                min_value=1,
                max_value=10,
                value=int(defaults.get('diet_quality', 7))
            )

        submitted = st.form_submit_button(
            'Predict outcome',
            use_container_width=True
        )

    if submitted:
        habits = {
            'sleep_hours': sleep_hours,
            'focus_hours': focus_hours,
            'exercise_minutes': exercise_minutes,
            'mood': mood,
            'screen_time_hours': screen_time_hours,
            'diet_quality': diet_quality
        }
        _handle_what_if_prediction(user_key, habits)


def _handle_what_if_prediction(user_key, habits):
    """
    Process a what-if prediction request.

    Args:
        user_key (str): GUID of the logged-in user.
        habits (dict): Hypothetical habit values.
    """
    try:
        with st.spinner('Calculating...'):
            response = client.what_if_prediction(user_key, habits)

        # Handle insufficient data
        if response.get('prediction') is None:
            message = response.get(
                'message',
                'Not enough data for predictions.'
            )
            st.warning(message)
            return

        prediction = response.get('prediction', 'unknown')
        probability = response.get('probability', 0.5)
        confidence = response.get('confidence', 'low')
        explanation = response.get('explanation', '')

        # Display result
        st.markdown('---')
        st.markdown('**Predicted Outcome**')

        render_probability_metric(probability, 'productive day')
        render_confidence_indicator(confidence)

        if explanation:
            st.markdown(f'{explanation}')

    except Exception as error:
        st.error(f'Unable to calculate prediction: {error}')


def _display_habits(habits):
    """
    Display habit values in a readable format.

    Args:
        habits (dict): Dictionary of habit values.
    """
    for habit_name, value in habits.items():
        formatted = format_habit_value(habit_name, value)
        st.markdown(f'- {formatted}')
