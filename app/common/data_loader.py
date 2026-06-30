
from pathlib import Path
import pandas as pd
import streamlit as st


APP_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = APP_DIR.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sf_housing_model_ready.csv"
)

CSS_PATH = (
    APP_DIR
    / "styles"
    / "styles.css"
)


@st.cache_data(show_spinner=False)
def load_market_data() -> pd.DataFrame:

    columns = [
        "rent",
        "sqft",
        "bedrooms",
        "neighborhood",
        "longitude",
        "latitude",
    ]

    return (
        pd.read_csv(
            DATA_PATH,
            usecols=columns,
        )
        .dropna(subset=["rent", "neighborhood"])
    )


def load_css():

    with open(CSS_PATH, encoding="utf-8") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )