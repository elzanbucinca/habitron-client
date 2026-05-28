"""
Chat message component.

Displays messages in a chat-like format for AI conversations.
Supports both user messages (right-aligned) and AI messages
(left-aligned).
"""

import streamlit as st


# CSS styles for chat messages
CHAT_STYLES = """
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin: 1rem 0;
}
.chat-message {
    padding: 0.75rem 1rem;
    border-radius: 1rem;
    max-width: 85%;
    line-height: 1.5;
}
.chat-message-user {
    background-color: #0084ff;
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 0.25rem;
    margin-left: auto;
}
.chat-message-ai {
    background-color: #f0f0f0;
    color: #333;
    align-self: flex-start;
    border-bottom-left-radius: 0.25rem;
}
.chat-label {
    font-size: 0.75rem;
    color: #888;
    margin-bottom: 0.25rem;
}
.chat-label-user {
    text-align: right;
}
.chat-label-ai {
    text-align: left;
}
</style>
"""


def render_chat_message(message, is_user=False, label=None):
    """
    Render a single chat message bubble.

    Args:
        message (str): The message content to display.
        is_user (bool): True for user messages (right-aligned),
                       False for AI messages (left-aligned).
        label (str): Optional label above the message (e.g., "You",
                    "Assistant").

    Returns:
        None. Renders the message directly to Streamlit.
    """
    # Inject styles once per session
    if 'chat_styles_injected' not in st.session_state:
        st.markdown(CHAT_STYLES, unsafe_allow_html=True)
        st.session_state['chat_styles_injected'] = True

    message_type = 'user' if is_user else 'ai'
    default_label = 'You' if is_user else 'Habitron'
    display_label = label if label else default_label

    # Escape HTML in message to prevent XSS
    safe_message = (
        message
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('\n', '<br>')
    )

    html = f"""
    <div class="chat-label chat-label-{message_type}">{display_label}</div>
    <div class="chat-message chat-message-{message_type}">
        {safe_message}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def render_chat_history(messages):
    """
    Render a list of chat messages.

    Args:
        messages (list): List of dictionaries with keys:
                        - content (str): Message text
                        - is_user (bool): True for user, False for AI
                        - label (str): Optional custom label

    Returns:
        None. Renders messages directly to Streamlit.
    """
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for msg in messages:
        render_chat_message(
            message=msg.get('content', ''),
            is_user=msg.get('is_user', False),
            label=msg.get('label')
        )

    st.markdown('</div>', unsafe_allow_html=True)
