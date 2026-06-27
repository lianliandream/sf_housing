from pathlib import Path
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
# ----------------------------------------------------
# Directories
# ----------------------------------------------------
CSS_CANDIDATES = [
    APP_DIR / "styles" / "main.css",
    APP_DIR / "stlyes" / "main.css",
]
CSS_PATH = next((path for path in CSS_CANDIDATES if path.exists()), CSS_CANDIDATES[0])

def load_css():
    with open(CSS_PATH, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

PROJECT_ROOT = APP_DIR.parent

# ----------------------------------------------------
# Paths
# ----------------------------------------------------

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sf_housing_model_ready.csv"
)

GEOJSON_PATH = (
    PROJECT_ROOT
    / "data"
    / "geojson"
    / "sf_analysis_neighborhoods.geojson"
)

CSS_PATH = next(
    (path for path in CSS_CANDIDATES if path.exists()),
    CSS_CANDIDATES[0],
)

# ----------------------------------------------------
# CSS
# ----------------------------------------------------

def load_css():

    with open(CSS_PATH, encoding="utf-8") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

# ----------------------------------------------------
# Data
# ----------------------------------------------------

@st.cache_data
def load_data():

    return pd.read_csv(DATA_PATH)

# ----------------------------------------------------
# GeoJSON
# ----------------------------------------------------

@st.cache_data
def load_geojson():

    with open(GEOJSON_PATH, encoding="utf-8") as f:

        return json.load(f)