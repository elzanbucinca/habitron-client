"""
Insight card component.

Reusable card for displaying a single insight with icon, title,
description, and optional color coding.
"""

import streamlit as st


# CSS styles for insight cards
CARD_STYLES = """
<style>
.insight-card {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
}
.insight-card-positive {
    background-color: rgba(0, 200, 83, 0.1);
    border-left: 4px solid #00c853;
}
.insight-card-warning {
    background-color: rgba(255, 152, 0, 0.1);
    border-left: 4px solid #ff9800;
}
.insight-card-info {
    background-color: rgba(33, 150, 243, 0.1);
    border-left: 4px solid #2196f3;
}
.insight-card-neutral {
    background-color: rgba(158, 158, 158, 0.1);
    border-left: 4px solid #9e9e9e;
}
.insight-card-title {
    font-weight: 600;
    margin-bottom: 0.25rem;
}
.insight-card-description {
    color: #666;
    font-size: 0.95rem;
}
</style>
"""


def render_insight_card(title, description, card_type='info', icon=None):
    """
    Render a styled insight card.

    Args:
        title (str): Card title text.
        description (str): Card description or explanation.
        card_type (str): One of 'positive', 'warning', 'info', 'neutral'.
                        Determines the color scheme.
        icon (str): Optional icon character to display before title.

    Returns:
        None. Renders the card directly to Streamlit.
    """
    # Inject styles once per session
    if 'insight_card_styles_injected' not in st.session_state:
        st.markdown(CARD_STYLES, unsafe_allow_html=True)
        st.session_state['insight_card_styles_injected'] = True

    # Build title with optional icon
    title_text = title
    if icon:
        title_text = f'{icon} {title}'

    # Validate card type
    valid_types = ['positive', 'warning', 'info', 'neutral']
    if card_type not in valid_types:
        card_type = 'info'

    card_html = f"""
    <div class="insight-card insight-card-{card_type}">
        <div class="insight-card-title">{title_text}</div>
        <div class="insight-card-description">{description}</div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)


def render_insight_cards(insights):
    """
    Render multiple insight cards from a list.

    Args:
        insights (list): List of dictionaries with keys:
                        - title (str): Card title
                        - description (str): Card description
                        - card_type (str): Optional, defaults to 'info'
                        - icon (str): Optional icon

    Returns:
        None. Renders cards directly to Streamlit.
    """
    for insight in insights:
        render_insight_card(
            title=insight.get('title', ''),
            description=insight.get('description', ''),
            card_type=insight.get('card_type', 'info'),
            icon=insight.get('icon')
        )
