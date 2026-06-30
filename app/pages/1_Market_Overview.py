import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json

st.title("San Francisco Housing Rental Market Overview")

# -------------------------------------------------------
# Load data
# -------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent.parent

DATA_PATH = (
    ROOT
    / "data"
    / "processed"
    / "sf_housing_model_ready.csv"
)

GEOJSON_PATH = (
    ROOT
    / "data"
    / "geojson"
    / "sf_analysis_neighborhoods.geojson"
)

df = pd.read_csv(DATA_PATH)

with open(GEOJSON_PATH, encoding="utf-8") as f:
    geojson = json.load(f)

# -------------------------------------------------------
# Rename columns
# -------------------------------------------------------

df = df.rename(columns={
    "analysis_neighborhood":"neighborhood",
    "monthly_rent_mid":"rent",
    "square_footage_mid":"sqft",
    "bedroom_num":"bedrooms",
    "bathroom_num":"bathrooms"
})

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.header("Filters")

selected = st.sidebar.multiselect(
    "Neighborhood",
    sorted(df["neighborhood"].dropna().unique()),
    default=sorted(df["neighborhood"].dropna().unique())
)

filtered = df[
    df["neighborhood"].isin(selected)
]

# -------------------------------------------------------
# KPIs
# -------------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Listings",
    f"{len(filtered):,}"
)

c2.metric(
    "Average Rent",
    f"${filtered['rent'].mean():,.0f}"
)

c3.metric(
    "Median Rent",
    f"${filtered['rent'].median():,.0f}"
)

c4.metric(
    "Neighborhoods",
    filtered["neighborhood"].nunique()
)

st.divider()

# -------------------------------------------------------
# Neighborhood summary
# -------------------------------------------------------

summary = (
    filtered
    .groupby("neighborhood")
    .agg(
        avg_rent=("rent","mean"),
        median_rent=("rent","median"),
        listings=("rent","count")
    )
    .reset_index()
)

# -------------------------------------------------------
# GeoJSON Map
# -------------------------------------------------------

fig = px.choropleth_mapbox(
    summary,
    geojson=geojson,
    locations="neighborhood",
    featureidkey="properties.nhood",
    color="avg_rent",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    zoom=11,
    center={
        "lat":37.7749,
        "lon":-122.4194
    },
    opacity=0.7,
    hover_data={
        "avg_rent":":,.0f",
        "median_rent":":,.0f",
        "listings":True
    }
)

fig.update_layout(
    margin=dict(
        l=0,
        r=0,
        t=0,
        b=0
    ),
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Charts
# -------------------------------------------------------

left,right = st.columns(2)

with left:

    fig = px.histogram(
        filtered,
        x="rent",
        nbins=40,
        title="Rent Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.scatter(
        filtered,
        x="sqft",
        y="rent",
        color="bedrooms",
        hover_name="neighborhood",
        title="Monthly Rent vs Square Footage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader("Neighborhood Statistics")

st.dataframe(
    summary.sort_values(
        "avg_rent",
        ascending=False
    ),
    use_container_width=True
)
st.divider()