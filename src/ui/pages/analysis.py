"""
Correlation Analysis page - Display habit-productivity relationships.

Shows:
- Correlation matrix
- Strength of relationships
"""

import streamlit as st
import matplotlib.pyplot as plt


def render(data):
    """
    Render the correlation analysis page.

    Args:
        data: Dictionary with pre-loaded analysis data.
    """
    st.header(':material/hub: Correlation Analysis')

    if data is None:
        st.warning('No data available.')
        return

    try:
        correlations = data['correlations']

        st.subheader('Habit-Productivity Correlations')

        if correlations:
            habit_friendly_names = {
                'sleep_hours': 'Sleep Hours',
                'focus_hours': 'Focus Hours',
                'exercise_minutes': 'Exercise Minutes',
                'mood': 'Mood',
                'screen_time_hours': 'Screen Time Hours',
                'diet_quality': 'Diet Quality'
            }

            correlation_list = []
            for habit, info in correlations.items():
                friendly_name = habit_friendly_names.get(
                    habit, habit.replace('_', ' ').title()
                )
                correlation_list.append({
                    'Habit': friendly_name,
                    'Correlation': f"{info['correlation']:.3f}",
                    'Strength': info['strength'].upper()
                })

            st.dataframe(correlation_list, use_container_width=True)

            # Display as chart
            st.subheader('Correlation Visualization')
            habits_display = []
            values = []
            for habit, info in correlations.items():
                friendly_name = habit_friendly_names.get(
                    habit, habit.replace('_', ' ').title()
                )
                habits_display.append(friendly_name)
                values.append(info['correlation'])

            fig, ax = plt.subplots(figsize=(10, 4))
            colors = []
            for v in values:
                if v < 0:
                    colors.append('red')
                else:
                    colors.append('green')
            ax.barh(habits_display, values, color=colors)
            ax.set_xlabel('Correlation with Productivity')
            ax.set_title('Habit-Productivity Correlations')
            ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
            st.pyplot(fig)
        else:
            st.info('No correlation data available.')
    except Exception as error:
        st.error(f'Error displaying correlations: {error}')
