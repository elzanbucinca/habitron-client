"""
Log Habits page – manual habit entry form.

Shows:
- Date navigation (previous/next day, today button)
- Habit input fields with guidance tooltips
- Pre-fills form when editing existing entries
- Save button that inserts or updates via API
"""

import datetime

import streamlit as st

from src.services.api_client import client


def _load_existing_entry(user_key, date_str):
    """
    Fetch an existing habit entry for the given date.

    Args:
        user_key (str): GUID of the logged-in user.
        date_str (str): Date in YYYY-MM-DD format.

    Returns:
        dict: Habit record if found, None otherwise.
    """
    try:
        response = client.get_habit_by_date(user_key, date_str)
        return response.get('habit')
    except Exception:
        return None


def render(user_key):
    """
    Render the log habits page.

    Args:
        user_key (str): GUID of the logged-in user.
    """
    st.header(':material/edit_note: Log Habits')

    # Initialize date in session state if not set
    if 'log_habits_date' not in st.session_state:
        st.session_state['log_habits_date'] = datetime.date.today()

    # Date navigation row
    col_prev, col_date, col_next, col_today = st.columns([1, 2, 1, 1])

    with col_prev:
        if st.button('◀', help='Previous day'):
            st.session_state['log_habits_date'] = (
                st.session_state['log_habits_date'] -
                datetime.timedelta(days=1)
            )
            st.rerun()

    with col_date:
        new_date = st.date_input(
            'Date',
            value=st.session_state['log_habits_date'],
            label_visibility='collapsed'
        )
        if new_date != st.session_state['log_habits_date']:
            st.session_state['log_habits_date'] = new_date
            st.rerun()

    with col_next:
        if st.button('▶', help='Next day'):
            st.session_state['log_habits_date'] = (
                st.session_state['log_habits_date'] +
                datetime.timedelta(days=1)
            )
            st.rerun()

    with col_today:
        if st.button('Today', help='Go to today'):
            st.session_state['log_habits_date'] = datetime.date.today()
            st.rerun()

    selected_date = st.session_state['log_habits_date']
    date_str = selected_date.strftime('%Y-%m-%d')

    # Load existing entry only when date or user changes (cache in session state)
    cached_date = st.session_state.get('log_habits_cached_date')
    cached_user = st.session_state.get('log_habits_cached_user')
    if cached_date != date_str or cached_user != user_key:
        existing_entry = _load_existing_entry(user_key, date_str)
        st.session_state['log_habits_cached_date'] = date_str
        st.session_state['log_habits_cached_user'] = user_key
        st.session_state['log_habits_cached_entry'] = existing_entry
    else:
        existing_entry = st.session_state.get('log_habits_cached_entry')

    if existing_entry is not None:
        st.info('Editing existing entry for this date.')
        default_sleep = existing_entry.get('sleep_hours', 0.0)
        default_exercise = existing_entry.get('exercise_minutes', 0)
        default_screen = existing_entry.get('screen_time_hours', 0.0)
        default_diet = existing_entry.get('diet_quality', 5)
        default_mood = existing_entry.get('mood', 5)
        default_focus = existing_entry.get('focus_hours', 0.0)
        default_productivity = existing_entry.get('productivity_score', 5)
    else:
        default_sleep = 0.0
        default_exercise = 0
        default_screen = 0.0
        default_diet = 5
        default_mood = 5
        default_focus = 0.0
        default_productivity = 5

    st.markdown('---')

    col_left, col_right = st.columns(2)

    with col_left:
        sleep_hours = st.number_input(
            'Sleep Hours',
            min_value=0.0,
            max_value=24.0,
            value=float(default_sleep),
            step=0.5,
            help='Total hours slept last night (e.g. 7.5)'
        )

        exercise_minutes = st.number_input(
            'Exercise Minutes',
            min_value=0,
            max_value=300,
            value=int(default_exercise),
            step=5,
            help=(
                'Total minutes of physical activity of any kind '
                '(walking, gym, sport)'
            )
        )

        screen_time_hours = st.number_input(
            'Screen Time Hours',
            min_value=0.0,
            max_value=24.0,
            value=float(default_screen),
            step=0.5,
            help=(
                'Recreational screen time in hours – '
                'excludes focused work or study'
            )
        )

    with col_right:
        diet_quality = st.slider(
            'Diet Quality',
            min_value=1,
            max_value=10,
            value=int(default_diet),
            help=(
                '1 = very poor (junk food / skipped meals), '
                '5 = balanced and adequate, '
                '10 = excellent (varied, nutritious whole foods)'
            )
        )

        mood = st.slider(
            'Mood',
            min_value=1,
            max_value=10,
            value=int(default_mood),
            help=(
                '1 = very low (depressed, anxious), '
                '5 = neutral, '
                '10 = excellent (energised, positive)'
            )
        )

        focus_hours = st.number_input(
            'Focus Hours',
            min_value=0.0,
            max_value=24.0,
            value=float(default_focus),
            step=0.5,
            help='Hours of concentrated, uninterrupted work or study'
        )

    st.markdown('---')

    productivity_score = st.slider(
        'Productivity Score',
        min_value=1,
        max_value=10,
        value=int(default_productivity),
        help=(
            '1 = very unproductive, '
            '5 = average, '
            '10 = highly productive – '
            'your own overall assessment of the day'
        )
    )

    if st.button('Save Entry'):
        _handle_log_habits(
            user_key,
            date_str,
            sleep_hours,
            diet_quality,
            exercise_minutes,
            mood,
            screen_time_hours,
            focus_hours,
            productivity_score
        )


def _handle_log_habits(
    user_key,
    date_str,
    sleep_hours,
    diet_quality,
    exercise_minutes,
    mood,
    screen_time_hours,
    focus_hours,
    productivity_score
):
    """
    Call the API to save a habit entry and handle the response.

    Shows a success message indicating whether the entry was
    inserted or updated, and clears the analysis cache.

    Args:
        user_key (str): GUID of the logged-in user.
        date_str (str): Date in YYYY-MM-DD format.
        sleep_hours (float): Hours slept.
        diet_quality (int): Diet quality rating (1-10).
        exercise_minutes (int): Minutes of exercise.
        mood (int): Mood rating (1-10).
        screen_time_hours (float): Recreational screen time in hours.
        focus_hours (float): Hours of focused work or study.
        productivity_score (int): Productivity rating (1-10).
    """
    try:
        response = client.log_habits(
            user_key,
            date_str,
            sleep_hours,
            diet_quality,
            exercise_minutes,
            mood,
            screen_time_hours,
            focus_hours,
            productivity_score
        )
        action = response.get('action', 'inserted')
        if action == 'updated':
            st.success('Entry updated.')
        else:
            st.success('Entry saved.')
        st.cache_data.clear()
        # Clear cached entry so form reloads with saved data
        st.session_state.pop('log_habits_cached_date', None)
        st.session_state.pop('log_habits_cached_user', None)
        st.session_state.pop('log_habits_cached_entry', None)
    except Exception as error:
        st.error(str(error))
