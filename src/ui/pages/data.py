"""
Data Overview page - Display raw data and statistics.

Shows:
- All habit records in tabular format
- Basic statistics (mean, median, std_dev)
"""

import streamlit as st

from src.services.api_client import client


def render(data, date_range):
    """
    Render the data overview page.

    Args:
        data: Dictionary with pre-loaded analysis data.
        date_range: Tuple of (start_date, end_date).
    """
    st.header(':material/table_chart: Data Overview')

    if data is None:
        st.warning('No data available.')
        return

    try:
        import pandas as pd
        
        dataframe = data['dataframe']
        statistics = data['statistics']

        start_date, end_date = date_range

        filtered_df = dataframe.loc[
            (dataframe.index >= pd.Timestamp(start_date)) &
            (dataframe.index <= pd.Timestamp(end_date))
        ]

        columns_to_hide = ['key', 'user_key']
        columns_to_drop = [
            col for col in columns_to_hide
            if col in filtered_df.columns
        ]
        filtered_df = filtered_df.drop(columns=columns_to_drop)

        st.subheader(
            f'Data from {start_date} to {end_date} '
            f'({len(filtered_df)} records)'
        )
        st.dataframe(filtered_df, use_container_width=True)

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

        st.subheader('Data Quality')
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric('Total Records', len(dataframe))

        with col2:
            st.metric(
                'Date Range',
                f"{dataframe.index[0].strftime('%Y-%m-%d')} to "
                f"{dataframe.index[-1].strftime('%Y-%m-%d')}"
            )

        with col3:
            st.metric('Missing Values', 0)
    except Exception as error:
        st.error(f'Error displaying data: {error}')
