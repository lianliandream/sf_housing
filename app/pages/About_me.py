from pathlib import Path
import streamlit as st

CSS_PATH = (
    Path(__file__).resolve().parent.parent
    / "styles"
    / "main.css"
)

with open(CSS_PATH, encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )

st.markdown("""
# Lian Wang

### Data Analytics • Data Engineering • Machine Learning

---

I am a former cruise industry professional and a recent graduate from **UC San Diego** with a B.S. in **Mathematics & Computer Science**. I will continue my studies in the **Online Master of Science in Analytics (OMSA)** program at **Georgia Tech**, with a focus on data science, machine learning, and business analytics.

This project demonstrates a complete analytics workflow using more than **546,000** San Francisco rental records, including:

- Data Engineering & ETL
- Data Validation
- Exploratory Data Analysis (EDA)
- Feature Engineering
- Machine Learning
- Geospatial Analytics
- Interactive Dashboard Development
""")

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.subheader("Technical Skills")

    st.markdown("""
**Programming**

- Python
- SQL
- C++
- Java
- C

**Data Analytics**

- Pandas
- NumPy
- Scikit-learn

**Visualization**

- Power BI
- Tableau
- Streamlit

**Tools**

- Git
- GitHub
- Jupyter Notebook
""")

with col2:

    st.subheader("Contact")

    st.markdown("""
**Email**

your_email@example.com

**LinkedIn**

https://www.linkedin.com/in/lianwangcs/

**GitHub**

https://github.com/lianliandream
""")

st.divider()

 
