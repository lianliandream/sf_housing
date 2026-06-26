import streamlit as st

st.set_page_config(
    page_title="SF Housing Intelligence Platform",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 SF Housing Intelligence Platform")

st.markdown("""
### End-to-End Data Analytics Project

This platform analyzes over **546,000** San Francisco housing records and provides:

- 📊 Market analytics
- 🗺️ Neighborhood comparison
- 🤖 Machine learning rent prediction
- 💬 AI-powered housing insights
""")

st.info("Use the navigation menu on the left to explore the platform.")

st.markdown("---")

st.subheader("Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Dataset", "546K+")

with col2:
    st.metric("Neighborhoods", "41")

with col3:
    st.metric("ML Models", "3")

st.markdown("---")

st.write(
    """
    This project demonstrates the complete analytics lifecycle:

    **Data Profiling → ETL → Validation → EDA → Feature Engineering → Machine Learning → Interactive Dashboard**
    """
)