"""
What's Working page - Display top habits and recommendations.

Shows:
- AI-generated recommendations for habit improvement
- Top habits that correlate with good days
- Quick wins and actionable tips
"""

import streamlit as st

from src.services.api_client import client


def render(user_key, correlations=None):
    """
    Render the What's Working page.

    Displays AI recommendations and top habits contributing to
    productivity in a friendly card-based format.

    Args:
        user_key (str): GUID of the logged-in user.
        correlations (dict): Optional pre-loaded correlation data.
    """
    st.header("✨ What's Working")

    st.markdown(
        'Discover which habits help you the most and get '
        'personalized tips to improve.'
    )

    # Display top habits section
    _render_top_habits(user_key, correlations)

    st.markdown('---')

    # Display AI recommendations
    _render_recommendations(user_key)


def _render_top_habits(user_key, correlations):
    """
    Render the top habits section based on correlation data.

    Args:
        user_key (str): GUID of the logged-in user.
        correlations (dict): Correlation data from API.
    """
    st.subheader('🏆 Your Top Habits')

    try:
        # Load correlations if not provided
        if correlations is None:
            response = client.get_correlations(user_key)
            correlations = response.get('correlations', {})

        if not correlations:
            st.info('Log more data to see which habits help you most.')
            return

        # Sort by positive correlation (habits that help productivity)
        habit_list = []
        for habit, info in correlations.items():
            habit_list.append({
                'habit': habit,
                'correlation': info['correlation'],
                'strength': info['strength']
            })

        # Sort by correlation descending
        sorted_habits = sorted(
            habit_list,
            key=lambda x: x['correlation'],
            reverse=True
        )

        # Display top 3 positive correlations
        positive_habits = [
            h for h in sorted_habits if h['correlation'] > 0
        ]

        if not positive_habits:
            st.info('Not enough data to identify top habits yet.')
            return

        habit_emojis = {
            'sleep_hours': '🛏️',
            'focus_hours': '🎯',
            'exercise_minutes': '🏃',
            'mood': '😊',
            'screen_time_hours': '📱',
            'diet_quality': '🥗'
        }

        habit_names = {
            'sleep_hours': 'Sleep',
            'focus_hours': 'Focus Time',
            'exercise_minutes': 'Exercise',
            'mood': 'Mood',
            'screen_time_hours': 'Screen Time',
            'diet_quality': 'Diet Quality'
        }

        for habit_data in positive_habits[:3]:
            habit = habit_data['habit']
            emoji = habit_emojis.get(habit, '📊')
            name = habit_names.get(habit, habit.replace('_', ' ').title())
            strength = habit_data['strength'].upper()

            # Create a card-like display
            st.markdown(
                f'**{emoji} {name}** — {strength} positive impact on '
                f'your productivity'
            )

    except Exception as error:
        st.warning(f'Could not load habit analysis: {error}')


def _render_recommendations(user_key):
    """
    Render AI-generated recommendations.

    Args:
        user_key (str): GUID of the logged-in user.
    """
    st.subheader('💡 Quick Wins')

    st.markdown(
        'Personalized suggestions to boost your productivity:'
    )

    try:
        with st.spinner('Getting personalized recommendations...'):
            response = client.get_recommendations(user_key)

        recommendations = response.get('recommendations', '')
        confidence = response.get('confidence', 'low')

        if not recommendations:
            st.info(
                'Log more habits to receive personalized '
                'recommendations!'
            )
            return

        # Display recommendations
        st.markdown(recommendations)

        # Show confidence level
        if confidence == 'low':
            st.caption(
                '💡 These recommendations will improve as you '
                'log more data.'
            )

    except Exception as error:
        st.warning(f'Could not load recommendations: {error}')
        st.info(
            'Make sure the API is running and AI features are '
            'configured.'
        )
