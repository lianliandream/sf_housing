import streamlit as st

st.set_page_config(
    page_title="SF Housing Rent Intelligence Platform",
    layout="wide"
)

st.title("SF Housing Rent Intelligence Platform")

st.caption("Interactive Rental Market Analytics for San Francisco")
st.divider()

st.markdown("""
## Welcome

This platform analyzes more than **546,000** San Francisco rental records collected by the San Francisco Rent Board.

**Data Source:**  
[San Francisco Rent Board – Rent Board Housing Inventory Data](https://data.sfgov.org/)

The project demonstrates an end-to-end analytics workflow, including:

- Data Engineering
- ETL Pipeline
- Data Validation
- Exploratory Data Analysis
- Feature Engineering
- Machine Learning
- Geospatial Analytics
- Interactive Dashboard
""")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rental Records", "546K+")

with col2:
    st.metric("Neighborhoods", "41")

with col3:
    st.metric("ML Models", "3")

with col4:
    st.metric("Interactive Maps", "GeoJSON")

st.divider()

st.subheader("Technology Stack")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
### Programming

- Python
- SQL
- Git
""")

with c2:
    st.markdown("""
### Analytics

- Pandas
- NumPy
- Scikit-Learn
""")

with c3:
    st.markdown("""
### Visualization

- Streamlit
- Plotly
- GeoJSON
""")

st.divider()

st.subheader("Explore")

st.info("""
Use the navigation menu on the left to explore:

• Market Overview

• Neighborhood Explorer

• Neighborhood Comparison

• Rent Predictor
        
• About Me
""")

st.divider()


 