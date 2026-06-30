import streamlit as st
import pandas as pd


def render_kpis(df: pd.DataFrame) -> None:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Records",
            value=f"{len(df):,}",
        )

    with col2:
        st.metric(
            label="Average Rent",
            value=f"${df['rent'].mean():,.0f}",
        )

    with col3:
        st.metric(
            label="Median Rent",
            value=f"${df['rent'].median():,.0f}",
        )

    with col4:
        st.metric(
            label="Average Size",
            value=f"{df['sqft'].mean():,.0f} ft²",
        )
    st.divider()