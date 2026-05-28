"""
Sidebar navigation component.

Provides navigation, filters, and controls for the dashboard.
"""

import streamlit as st


# Custom CSS for menu styling
MENU_CSS = """
<style>
/* Reduce spacing in sidebar button containers */
section[data-testid="stSidebar"] .stButton {
    margin-bottom: -0.5rem !important;
}

/* Target all sidebar buttons and style as menu items */
section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 0.4rem 0.75rem !important;
    margin: 0 !important;
    border: none !important;
    border-radius: 0.4rem !important;
    background: transparent !important;
    box-shadow: none !important;
    font-size: 0.95rem !important;
    font-weight: 400 !important;
    min-height: 0 !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: rgba(151, 166, 195, 0.15) !important;
    border: none !important;
}

section[data-testid="stSidebar"] .stButton > button:focus {
    box-shadow: none !important;
    border: none !important;
}

section[data-testid="stSidebar"] .stButton > button:active {
    background-color: rgba(151, 166, 195, 0.2) !important;
}

/* Style for active/selected menu item (primary button) */
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {
    background-color: rgba(151, 166, 195, 0.2) !important;
    font-weight: 600 !important;
}

/* Section header styling */
.menu-section-header {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #808495;
    margin-top: 1rem;
    margin-bottom: 0.1rem;
    padding-left: 0.75rem;
}

/* Hide button borders completely */
section[data-testid="stSidebar"] .stButton > button::before,
section[data-testid="stSidebar"] .stButton > button::after {
    display: none !important;
}
</style>
"""


def render_sidebar(analysis_data=None):
    """
    Render the sidebar navigation and filters.

    Displays the current user's name and email at the top with a
    Log out button. Also renders page selection organized into
    sections and filter options.

    Args:
        analysis_data: Dictionary with pre-loaded analysis data.

    Returns:
        dict: Contains page, date_range, selected_habits, anomaly_threshold.
    """
    # Inject custom CSS
    st.sidebar.markdown(MENU_CSS, unsafe_allow_html=True)

    _render_user_section()

    st.sidebar.title('Navigation')

    # Initialize selected page in session state
    if 'selected_page' not in st.session_state:
        st.session_state['selected_page'] = 'Log Habits'

    # DATA section
    st.sidebar.markdown(
        '<p class="menu-section-header">Data</p>',
        unsafe_allow_html=True
    )
    _render_menu_item('Log Habits')
    _render_menu_item('View History')

    # INSIGHTS section
    st.sidebar.markdown(
        '<p class="menu-section-header">Insights</p>',
        unsafe_allow_html=True
    )
    _render_menu_item('Weekly Summary')
    _render_menu_item("What's Working")

    # AI ASSISTANT section
    st.sidebar.markdown(
        '<p class="menu-section-header">AI Assistant</p>',
        unsafe_allow_html=True
    )
    _render_menu_item('Ask a Question')
    _render_menu_item('Predictions')
    _render_menu_item('Unusual Days')

    page = st.session_state['selected_page']

    st.sidebar.markdown('---')
    st.sidebar.markdown(
        '<p class="menu-section-header">⚙️ Filter Options</p>',
        unsafe_allow_html=True
    )

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

    return {
        'page': page,
        'date_range': date_range,
        'selected_habits': selected_habits,
        'anomaly_threshold': anomaly_threshold
    }


def _render_menu_item(label):
    """
    Render a single menu item as a styled button.

    Uses primary button type for the selected item and secondary
    for others to achieve different visual styles.

    Args:
        label (str): The menu item label.
        icon (str): Emoji icon to display before the label.
    """
    is_selected = st.session_state.get('selected_page') == label
    button_type = 'primary' if is_selected else 'secondary'

    if st.sidebar.button(
        label,
        key=f'menu_{label}',
        type=button_type,
        use_container_width=True
    ):
        st.session_state['selected_page'] = label
        st.rerun()


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
        st.session_state.pop('selected_page', None)
        st.rerun()

    st.sidebar.markdown('---')
