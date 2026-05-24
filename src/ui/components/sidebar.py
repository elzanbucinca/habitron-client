"""
Sidebar navigation component.

Provides navigation, filters, and controls for the dashboard.
"""

import streamlit as st


def render_sidebar(analysis_data=None):
    """
    Render the sidebar navigation and filters.

    Displays the current user's name and email at the top with a
    Log out button. Also renders page selection and filter options.

    Args:
        analysis_data: Dictionary with pre-loaded analysis data.

    Returns:
        dict: Contains page, date_range, selected_habits, anomaly_threshold.
    """
    _render_user_section()

    st.sidebar.title('Navigation & Filters')

    st.sidebar.markdown('### :material/menu: Page Selection')

    page = st.sidebar.radio(
        'Select a page:',
        [
            'Log Habits',
            'AI Insights',
            'Data Overview',
            'Correlation Analysis',
            'Trends & Patterns',
            'Model & Predictions',
            'Anomalies',
        ]
    )

    st.sidebar.markdown('---')
    st.sidebar.markdown('### :material/tune: Filter Options')

    date_range = (None, None)
    selected_habits = []
    anomaly_threshold = 2.5

    if analysis_data is not None:
        dataframe = analysis_data['dataframe']

        start_date = st.sidebar.date_input(
            'Start Date',
            value=dataframe.index[0].date()
        )

        end_date = st.sidebar.date_input(
            'End Date',
            value=dataframe.index[-1].date()
        )

        date_range = (start_date, end_date)

        st.sidebar.markdown('---')

        habit_options = [
            'Sleep Hours',
            'Focus Hours',
            'Exercise Minutes',
            'Mood',
            'Screen Time Hours',
            'Diet Quality'
        ]

        selected_habits_display = st.sidebar.multiselect(
            'Select Habits to Display',
            habit_options,
            default=habit_options,
            help='Choose which habits to show in trends'
        )

        selected_habits = [
            h.lower().replace(' ', '_')
            for h in selected_habits_display
        ]

        anomaly_threshold = st.sidebar.slider(
            'Anomaly Detection Threshold',
            min_value=1.0,
            max_value=4.0,
            value=2.5,
            step=0.1
        )

    st.sidebar.markdown('---')
    st.sidebar.info(
        '**About Habitron**: '
        'This dashboard analyzes daily habit data to identify '
        'patterns, anomalies, and predictive relationships with '
        'productivity.'
    )

    return {
        'page': page,
        'date_range': date_range,
        'selected_habits': selected_habits,
        'anomaly_threshold': anomaly_threshold
    }


def _render_user_section():
    """
    Render the logged-in user's name, email, and a Log out button.

    Reads current_user from session state. If no user is set,
    nothing is rendered. The Log out button removes current_user
    from session state and triggers a rerun.
    """
    current_user = st.session_state.get('current_user')

    if current_user is None:
        return

    first_name = current_user['first_name']
    email = current_user['email']

    st.sidebar.markdown(f':material/person: **{first_name}**')
    st.sidebar.markdown(f'{email}')

    if st.sidebar.button('Log out'):
        del st.session_state['current_user']
        # Clear log_habits cache to avoid leaking data between users
        st.session_state.pop('log_habits_date', None)
        st.session_state.pop('log_habits_cached_date', None)
        st.session_state.pop('log_habits_cached_user', None)
        st.session_state.pop('log_habits_cached_entry', None)
        st.rerun()

    st.sidebar.markdown('---')
