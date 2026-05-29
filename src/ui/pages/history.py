"""
View History page - Display raw data and statistics.

Shows:
- All habit records in tabular format
- Basic statistics (mean, median, std_dev)
"""

import streamlit as st

from src.services.api_client import client


def render(data):
    """
    Render the view history page.

    Args:
        data: Dictionary with pre-loaded analysis data.
    """
    st.header(':material/table_chart: History')

    if data is None:
        st.warning('No data available.')
        return

    try:
        dataframe = data['dataframe']
        statistics = data['statistics']

        columns_to_hide = ['key', 'user_key']
        columns_to_drop = [
            col for col in columns_to_hide
            if col in dataframe.columns
        ]
        display_df = dataframe.drop(columns=columns_to_drop)

        st.subheader(f'All Records ({len(display_df)} total)')
        st.dataframe(display_df, use_container_width=True)

        st.subheader('Basic Statistics')
        stats_data = []
        for column, stats in statistics.items():
            stats_data.append({
                'Column': column,
                'Mean': f"{stats['mean']:.2f}",
                'Median': f"{stats['median']:.2f}",
                'Std Dev': f"{stats['std_dev']:.2f}"
            })

        st.dataframe(stats_data, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.metric('Total Records', len(dataframe))

        with col2:
            st.metric(
                'Date Range',
                f"{dataframe.index[0].strftime('%Y-%m-%d')} to "
                f"{dataframe.index[-1].strftime('%Y-%m-%d')}"
            )


    except Exception as error:
        st.error(f'Error displaying data: {error}')
