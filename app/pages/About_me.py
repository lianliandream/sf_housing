from pathlib import Path
import streamlit as st

CSS_PATH = Path(__file__).resolve().parent.parent / "styles" / "about_me.css"

with open(CSS_PATH, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
# Lian Wang

### Data Analytics • Data Engineering • Machine Learning
""")
st.caption("Email: lianwangsf2021@gmail.com • GitHub: https://github.com/lianliandream")

st.markdown("""
Ex-cruise ship crew and a recent graduate from **UC San Diego** with a B.S. in **Mathematics & Computer Science** 
Continuing studies in the **Master of Science in Analytics (OMSA)** program at **Georgia Tech**, with a focus on data science, machine learning, and business analytics.
""")

st.divider()

milestones = [
    ("2017–2019", "Cruise operations and customer service: gained teamwork, process flow, and hospitality experience.", "🌍", "Traveling the world while working"),
    ("2019–2020", "Publishing and rights management: analytical thinking and project leadership.", "📚", "Publishing"),
    ("2021–2025", "UC San Diego — Mathematics & Computer Science, building a strong foundation in data and engineering.", "🎓", "UC San Diego"),
    ("2025–Present", "Focusing on analytics, machine learning, and projects that bridge data and business.", "🔧", "Engineering"),
]

st.markdown(""" ### About me
##### International cruise ships → Publishing → UC San Diego → Georgia Tech → ?
""")
for year, text, icon, label in milestones:
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown(f"**{year}** — {text}")
    with col_right:
        st.markdown(f"{icon} {label}")

skill_list = [
    "Python",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Streamlit",
    "Tableau",
    "SQL",
    "Git",
    "C++",
    "C",
    "Java",
    "Matplotlib",
    "Seaborn",
    "Plotly",
    "Statsmodels",
    "Jupyter Notebook",
    "VS Code",
    "Linux",
    "Docker",
    "AWS S3",
]

st.divider()

skills_text = " • ".join(skill_list)
st.markdown(f"**Skills:** {skills_text}")

st.divider()

 
