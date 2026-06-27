import joblib
import pandas as pd
import streamlit as st

from pathlib import Path

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Rent Predictor",
    page_icon="💰",
    layout="wide"
)

# ==========================================================
# Project Paths
# ==========================================================

ROOT = Path(__file__).resolve().parent.parent.parent

DATA_PATH = (
    ROOT
    / "data"
    / "processed"
    / "sf_housing_model_ready.csv"
)

MODEL_PATH = (
    ROOT
    / "models"
    / "rent_prediction_model.pkl"
)

# ==========================================================
# Load Data
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)

    df = df.rename(columns={
        "analysis_neighborhood": "neighborhood",
        "monthly_rent_mid": "rent",
        "square_footage_mid": "sqft",
        "bedroom_num": "bedrooms",
        "bathroom_num": "bathrooms"
    })

    return df


# ==========================================================
# Load Model
# ==========================================================

@st.cache_resource
def load_model():

    return joblib.load(MODEL_PATH)


# ==========================================================
# Initialize
# ==========================================================

df = load_data()

model = load_model()

# ==========================================================
# Lookup Tables
# ==========================================================

location_lookup = (

    df

    .groupby("neighborhood")[["latitude", "longitude"]]

    .mean()

)

city_avg_rent = df["rent"].mean()

CURRENT_YEAR = 2026

# ==========================================================
# Page Header
# ==========================================================

st.title("💰 Rent Predictor")

st.caption(
    "Estimate monthly rental prices using a trained Random Forest machine learning model."
)

st.divider()

# ==========================================================
# Sidebar - Property Information
# ==========================================================

st.sidebar.title("🏠 Property Information")

# Neighborhood

selected_neighborhood = st.sidebar.selectbox(
    "Neighborhood",
    sorted(df["neighborhood"].dropna().unique())
)

# Bedrooms

bedrooms = st.sidebar.selectbox(
    "Bedrooms",
    sorted(df["bedrooms"].dropna().unique())
)

# Bathrooms

bathrooms = st.sidebar.selectbox(
    "Bathrooms",
    sorted(df["bathrooms"].dropna().unique())
)

# Square Footage

sqft = st.sidebar.number_input(
    "Square Footage",
    min_value=200,
    max_value=6000,
    value=900,
    step=50
)

# Year Built

year_built = st.sidebar.number_input(
    "Year Built",
    min_value=1850,
    max_value=CURRENT_YEAR,
    value=1995,
    step=1
)

# ==========================================================
# Calculate Derived Features
# ==========================================================

property_age = CURRENT_YEAR - year_built

latitude = location_lookup.loc[selected_neighborhood, "latitude"]
longitude = location_lookup.loc[selected_neighborhood, "longitude"]



# ==========================================================
# Property Summary
# ==========================================================

st.subheader("Property Summary")

col1, col2 = st.columns(2)

with col1:
    st.metric("Neighborhood", selected_neighborhood)
    st.metric("Bedrooms", bedrooms)
    st.metric("Bathrooms", bathrooms)

with col2:
    st.metric("Square Footage", f"{sqft:,}")
    st.metric("Year Built", year_built)
    st.metric("Property Age", f"{property_age} years")


# ==========================================================
# Build Model Input
# ==========================================================

input_df = pd.DataFrame({
    "sqft": [sqft],
    "bedrooms": [bedrooms],
    "bathrooms": [bathrooms],
    "property_age": [property_age],
    "longitude": [longitude],
    "latitude": [latitude],
    "neighborhood": [selected_neighborhood]
})

prediction = model.predict(input_df)


# ==========================================================
# Prediction
# ==========================================================

if st.button("💰 Predict Monthly Rent", use_container_width=True):

    input_df = pd.DataFrame({
        "sqft": [sqft],
        "bedrooms": [bedrooms],
        "bathrooms": [bathrooms],
        "property_age": [property_age],
        "longitude": [longitude],
        "latitude": [latitude],
        "neighborhood": [selected_neighborhood]
    })

    prediction = model.predict(input_df)[0]

    st.success(f"## Estimated Monthly Rent\n\n${prediction:,.0f} / month")

    if prediction > city_avg_rent:
        st.info(
            f"This estimate is **${prediction - city_avg_rent:,.0f} above** the city average."
        )
    else:
        st.info(
            f"This estimate is **${city_avg_rent - prediction:,.0f} below** the city average."
        )