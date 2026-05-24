"""
Trends & Patterns page - Display time-series trends.

Shows:
- Trend direction and slope for each habit
- Improving vs declining habits
"""

import streamlit as st


def render(data, selected_habits):
    """
    Render the trends page.

    Args:
        data: Dictionary with pre-loaded analysis data.
        selected_habits: List of habit filters.
    """
    st.header(':material/trending_up: Trends & Patterns')

    if data is None:
        st.warning('No data available.')
        return

    try:
        trends = data['trends']

        st.subheader('Habit Trends Over Time')

        if trends:
            habit_friendly_names = {
                'sleep_hours': 'Sleep Hours',
                'focus_hours': 'Focus Hours',
                'exercise_minutes': 'Exercise Minutes',
                'mood': 'Mood',
                'screen_time_hours': 'Screen Time Hours',
                'diet_quality': 'Diet Quality'
            }

            for habit, trend_data in trends.items():
                if selected_habits and habit not in selected_habits:
                    continue

                friendly_name = habit_friendly_names.get(
                    habit, habit.replace('_', ' ').title()
                )

                with st.expander(friendly_name):
                    st.write(
                        f'**Direction:** {trend_data["direction"].upper()}'
                    )
                    st.write(f'**Slope:** {trend_data["slope"]:.4f}')
                    st.write(
                        f'**Interpretation:** '
                        f'{trend_data["interpretation"]}'
                    )
        else:
            st.info('No trend data available.')
    except Exception as error:
        st.error(f'Error displaying trends: {error}')
