"""
Login page – email-based user selection.

Shows:
- Email input and Continue button
- Registration form if user is not found
"""

import streamlit as st

from src.services.api_client import client


def render():
    """
    Render the login page.

    Prompts for an email address. If a matching user is found,
    stores the user dict in session state and reruns. If not
    found, shows a registration form to create a new account.
    """
    st.title('Welcome to Habitron')
    st.markdown(
        'Enter your email address to continue.'
    )

    email = st.text_input('Email address')

    if st.button('Continue'):
        if not email:
            st.warning('Please enter your email address.')
            return

        _handle_email_submit(email)


def _handle_email_submit(email):
    """
    Look up a user by email and update session state.

    If the user exists, stores the user dict in session state
    and reruns. If not found, stores the email in session state
    so the registration form can be shown.

    Args:
        email (str): Email address entered by the user.
    """
    try:
        response = client.get_user_by_email(email)
        user = response['user']
        st.session_state['current_user'] = user
        st.rerun()
    except Exception:
        st.session_state['pending_email'] = email
        st.rerun()


def render_registration(email):
    """
    Render the registration form for a new user.

    Collects first name, last name, age, and gender, then
    calls the API to create the user. On success, stores the
    user dict in session state and reruns.

    Args:
        email (str): Email address already entered by the user.
    """
    st.info(
        f'No account found for **{email}**. '
        'Please fill in your details to create an account.'
    )

    first_name = st.text_input('First name')
    last_name = st.text_input('Last name')
    age = st.number_input(
        'Age',
        min_value=1,
        max_value=120,
        step=1
    )
    gender = st.selectbox(
        'Gender',
        ['Male', 'Female', 'Other', 'Prefer not to say']
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Create account'):
            _handle_registration(
                first_name,
                last_name,
                int(age),
                gender,
                email
            )

    with col2:
        if st.button('Back'):
            del st.session_state['pending_email']
            st.rerun()


def _handle_registration(
    first_name,
    last_name,
    age,
    gender,
    email
):
    """
    Submit registration data to the API and update session state.

    On success, stores the new user dict in session state and
    reruns. On failure, displays an error message.

    Args:
        first_name (str): User's first name.
        last_name (str): User's last name.
        age (int): User's age.
        gender (str): User's gender.
        email (str): User's email address.
    """
    if not first_name or not last_name:
        st.warning('Please fill in all fields.')
        return

    try:
        create_response = client.create_user(
            first_name,
            last_name,
            age,
            gender,
            email
        )
        user_key = create_response['user_key']

        user = {
            'key': user_key,
            'first_name': first_name,
            'last_name': last_name,
            'age': age,
            'gender': gender,
            'email': email
        }
        st.session_state['current_user'] = user

        if 'pending_email' in st.session_state:
            del st.session_state['pending_email']

        st.rerun()
    except Exception as error:
        st.error(f'Could not create account: {error}')
