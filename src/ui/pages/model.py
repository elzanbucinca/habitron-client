"""
Model & Predictions page - Display ML model performance.

Shows:
- Model metrics (MAE, RMSE, R²)
- Feature coefficients
- Model importance ranking
"""

import streamlit as st
import matplotlib.pyplot as plt


def render(data):
    """
    Render the model page.

    Args:
        data: Dictionary with pre-loaded analysis data.
    """
    st.header(':material/model_training: Model & Predictions')

    if data is None:
        st.warning('No data available.')
        return

    try:
        metrics = data['model_metrics']
        coefficients = data['coefficients']

        st.subheader('Model Performance Metrics')
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric('MAE', f"{metrics['mae']:.3f}")

        with col2:
            st.metric('RMSE', f"{metrics['rmse']:.3f}")

        with col3:
            st.metric('R² Score', f"{metrics['r2']:.3f}")

        st.subheader('Feature Importance (Coefficients)')

        if coefficients:
            habit_friendly_names = {
                'sleep_hours': 'Sleep Hours',
                'focus_hours': 'Focus Hours',
                'exercise_minutes': 'Exercise Minutes',
                'mood': 'Mood',
                'screen_time_hours': 'Screen Time Hours',
                'diet_quality': 'Diet Quality'
            }

            coeff_names_raw = list(coefficients.keys())
            coeff_values = list(coefficients.values())

            coeff_names_display = []
            for name in coeff_names_raw:
                friendly_name = habit_friendly_names.get(
                    name, name.replace('_', ' ').title()
                )
                coeff_names_display.append(friendly_name)

            fig, ax = plt.subplots(figsize=(10, 6))
            colors = []
            for v in coeff_values:
                if v > 0:
                    colors.append('green')
                else:
                    colors.append('red')
            ax.barh(coeff_names_display, coeff_values, color=colors)
            ax.set_xlabel('Coefficient Value')
            ax.set_title('Feature Importance in Regression Model')
            ax.axvline(x=0, color='black', linestyle='-', linewidth=0.8)
            st.pyplot(fig)
        else:
            st.info('No coefficient data available.')
    except Exception as error:
        st.error(f'Error displaying model data: {error}')
