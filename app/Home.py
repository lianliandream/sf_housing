import streamlit as st
from components.kpis import render_kpis
from common.data_loader import load_market_data, load_css


st.set_page_config(
    page_title="SF Housing Analytics",
    layout="wide",
)

load_css()
data = load_market_data()

st.subheader("About This Project")

st.write(
    """
    This platform analyzes more than **546,000** San Francisco rental records.
    It's interactive dashboard explores rental housing trends across
    San Francisco using real-world listing data.

   
- Data Engineering
- ETL Pipeline
- Data Validation
- Exploratory Data Analysis
- Feature Engineering
- Machine Learning
- Geospatial Analytics
- Interactive Dashboard
    to help users better understand neighborhood-level rental markets.
    """
)

st.divider()

st.subheader("Market Snapshot")
render_kpis(data)


st.header("Features")

st.markdown("""
- **Market Overview** — Explore rental trends and neighborhood comparisons.
- **Interactive Map** — Visualize rental hotspots across San Francisco.
- **ML Insights** — Predict rental prices using machine learning.
- **Neighborhood Explorer** — Compare neighborhoods and housing characteristics.
""")

st.divider()

st.header("Dataset")

st.write("""
**Source:** San Francisco Rent Board Housing Inventory Data](https://data.sfgov.org/)

**Coverage:** San Francisco, California

The dataset includes:
- Monthly rent
- Square footage
- Bedrooms
- Neighborhood
- Latitude & Longitude
""")

st.divider()

st.header("Technology Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
**Languages**
- Python
- SQL
""")

with col2:
    st.markdown("""
**Libraries**
- Pandas
- Plotly
- Scikit-learn
""")

with col3:
    st.markdown("""
**Tools**
- Streamlit
- GitHub
- VS Code
""")

st.divider()

st.info(
    "👈 Use the navigation menu on the left to explore the Market Overview, Interactive Map, and Machine Learning Insights."
)