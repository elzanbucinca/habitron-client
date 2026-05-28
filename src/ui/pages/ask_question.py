"""
Ask Question page - AI chat interface.

Allows users to ask natural language questions about their
habit data and receive AI-generated responses.
"""

import streamlit as st

from src.services.api_client import client
from src.ui.components.chat_message import render_chat_message
from src.ui.components.metric_display import render_confidence_indicator


# Suggested questions for users to try
SUGGESTED_QUESTIONS = [
    'Why was last week rough?',
    'What should I focus on improving?',
    'How can I boost my productivity?',
    'What patterns do you see in my habits?'
]


def render(user_key):
    """
    Render the Ask Question page.

    Provides a chat interface for users to ask AI questions
    about their habit data.

    Args:
        user_key (str): GUID of the logged-in user.
    """
    st.header('Ask a Question')

    st.markdown(
        'Ask anything about your habits and get personalized insights.'
    )

    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Render chat history
    _render_chat_history()

    st.markdown('---')

    # Question input
    _render_question_input(user_key)

    # Suggested questions (only show if no chat history)
    if not st.session_state['chat_history']:
        st.markdown('---')
        _render_suggested_questions(user_key)


def _render_chat_history():
    """
    Render the conversation history.
    """
    for entry in st.session_state['chat_history']:
        render_chat_message(
            message=entry['content'],
            is_user=entry['is_user']
        )
        if not entry['is_user'] and 'confidence' in entry:
            render_confidence_indicator(entry['confidence'])


def _render_question_input(user_key):
    """
    Render the question input form.

    Args:
        user_key (str): GUID of the logged-in user.
    """
    with st.form(key='question_form', clear_on_submit=True):
        question = st.text_input(
            'Your question',
            placeholder='e.g., Why was I less productive last week?',
            label_visibility='collapsed'
        )

        col1, col2 = st.columns([4, 1])
        with col2:
            submitted = st.form_submit_button(
                'Ask',
                use_container_width=True
            )

    if submitted and question.strip():
        _handle_question(user_key, question.strip())


def _handle_question(user_key, question):
    """
    Process a user question and get AI response.

    Args:
        user_key (str): GUID of the logged-in user.
        question (str): The user's question.
    """
    # Add user message to history
    st.session_state['chat_history'].append({
        'content': question,
        'is_user': True
    })

    try:
        with st.spinner('Thinking...'):
            response = client.ask_question(user_key, question)

        answer = response.get('answer', 'Sorry, I could not process that.')
        confidence = response.get('confidence', 'low')

        # Add AI response to history
        st.session_state['chat_history'].append({
            'content': answer,
            'is_user': False,
            'confidence': confidence
        })

    except Exception as error:
        error_message = (
            'I encountered an error while processing your question. '
            'Please try again.'
        )
        st.session_state['chat_history'].append({
            'content': error_message,
            'is_user': False,
            'confidence': 'low'
        })
        st.error(f'Error: {error}')

    st.rerun()


def _render_suggested_questions(user_key):
    """
    Render suggested question buttons.

    Args:
        user_key (str): GUID of the logged-in user.
    """
    st.subheader('Try asking')

    cols = st.columns(2)

    for idx, question in enumerate(SUGGESTED_QUESTIONS):
        col = cols[idx % 2]
        with col:
            if st.button(
                question,
                key=f'suggested_{idx}',
                use_container_width=True
            ):
                _handle_question(user_key, question)


def clear_chat_history():
    """
    Clear the chat history.

    Call this function to reset the conversation.
    """
    if 'chat_history' in st.session_state:
        st.session_state['chat_history'] = []
