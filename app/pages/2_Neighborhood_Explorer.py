import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import geopandas as gpd
import streamlit as st

# ===========================================================
# Page Configuration
# ===========================================================

st.set_page_config(
    page_title="Neighborhood Explorer",
    layout="wide"
)

# ===========================================================
# Paths
# ===========================================================

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

# ===========================================================
# Load Data
# ===========================================================

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_data
def load_geojson():
    with open(GEOJSON_PATH, encoding="utf-8") as f:
        return json.load(f)
gdf = gpd.read_file(GEOJSON_PATH)

df = load_data()
geojson = load_geojson()


# ===========================================================
# Rename Columns
# ===========================================================

df = df.rename(
    columns={
        "analysis_neighborhood": "neighborhood",
        "monthly_rent_mid": "rent",
        "square_footage_mid": "sqft",
        "bedroom_num": "bedrooms",
        "bathroom_num": "bathrooms",
    }
)

# ===========================================================
# City Statistics
# ===========================================================

city_stats = {
    "avg_rent": df["rent"].mean(),
    "median_rent": df["rent"].median(),
    "avg_sqft": df["sqft"].mean(),
    "listings": len(df),
}

# ===========================================================
# Sidebar Filters
# ===========================================================

st.sidebar.title("Neighborhood Explorer")
# Neighborhood

selected_neighborhood = st.sidebar.selectbox(
    "Neighborhood",
    sorted(df["neighborhood"].dropna().unique())
)

# Bedrooms

bedroom_options = sorted(df["bedrooms"].dropna().unique())

selected_bedrooms = st.sidebar.multiselect(
    "Bedrooms",
    options=bedroom_options,
    default=bedroom_options,
)

# Bathrooms

bathroom_options = sorted(df["bathrooms"].dropna().unique())

selected_bathrooms = st.sidebar.multiselect(
    "Bathrooms",
    options=bathroom_options,
    default=bathroom_options,
)

# Monthly Rent

rent_range = st.sidebar.slider(
    "Monthly Rent ($)",
    min_value=int(df["rent"].min()),
    max_value=int(df["rent"].max()),
    value=(
        int(df["rent"].min()),
        int(df["rent"].max()),
    ),
)

# Square Footage

sqft_range = st.sidebar.slider(
    "Square Footage",
    min_value=int(df["sqft"].min()),
    max_value=int(df["sqft"].max()),
    value=(
        int(df["sqft"].min()),
        int(df["sqft"].max()),
    ),
)

# ===========================================================
# Apply Filters
# ===========================================================

filtered = df[
    (df["neighborhood"] == selected_neighborhood)
    & (df["bedrooms"].isin(selected_bedrooms))
    & (df["bathrooms"].isin(selected_bathrooms))
    & (df["rent"].between(*rent_range))
    & (df["sqft"].between(*sqft_range))
]

# ===========================================================
# Neighborhood Statistics
# ===========================================================

avg_rent = filtered["rent"].mean()
median_rent = filtered["rent"].median()
avg_sqft = filtered["sqft"].mean()
listing_count = len(filtered)

# ===========================================================
# Header
# ===========================================================

st.title(f" {selected_neighborhood}")
st.caption("Interactive Neighborhood Analytics")
st.divider()

# ===========================================================
# KPI Cards
# ===========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Average Rent",
    f"${avg_rent:,.0f}" if listing_count else "N/A"
)

c2.metric(
    "Median Rent",
    f"${median_rent:,.0f}" if listing_count else "N/A"
)

c3.metric(
    "Listings",
    f"{listing_count:,}"
)

c4.metric(
    "Average Sq Ft",
    f"{avg_sqft:,.0f}" if listing_count else "N/A"
)

# ===========================================================
# Neighborhood Map Data
# ===========================================================

map_df = (
    df.groupby("neighborhood", as_index=False)
      .agg(
          avg_rent=("rent", "mean"),
          median_rent=("rent", "median"),
          listings=("rent", "count"),
          avg_sqft=("sqft", "mean"),
      )
)

# -------------------------------------------------
# Find selected neighborhood center
# -------------------------------------------------
selected_poly = gdf[
    gdf["nhood"] == selected_neighborhood
]

center = selected_poly.geometry.centroid.iloc[0]

# -------------------------------------------------
# Base choropleth
# -------------------------------------------------

fig = px.choropleth_mapbox(
    map_df,
    geojson=geojson,
    locations="neighborhood",
    featureidkey="properties.nhood",   # or properties.analysis_neighborhood
    color="avg_rent",
    color_continuous_scale="Blues",
    hover_name="neighborhood",
    hover_data={
        "avg_rent": ":,.0f",
        "median_rent": ":,.0f",
        "avg_sqft": ":,.0f",
        "listings": True,
    },
    center={
        "lat": center.y,
        "lon": center.x,
    },
    zoom=10.8,
    opacity=0.75,
    mapbox_style="carto-positron",
)

# ===========================================================
# Neighborhood Map Data
# ===========================================================
st.divider()
st.subheader(" Interactive Neighborhood Map")

map_df = (
    df.groupby("neighborhood", as_index=False)
      .agg(
          avg_rent=("rent", "mean"),
          median_rent=("rent", "median"),
          listings=("rent", "count"),
          avg_sqft=("sqft", "mean"),
      )
)

# Selected neighborhood boundary
selected_geojson = {
    "type": "FeatureCollection",
    "features": [
        f for f in geojson["features"]
        if f["properties"]["nhood"] == selected_neighborhood
    ]
}

# Center map on selected neighborhood
selected_poly = gdf[gdf["nhood"] == selected_neighborhood]
center = selected_poly.geometry.centroid.iloc[0]

fig_map = px.choropleth_mapbox(
    map_df,
    geojson=geojson,
    locations="neighborhood",
    featureidkey="properties.nhood",
    color="avg_rent",
    color_continuous_scale="Blues",
    hover_name="neighborhood",
    hover_data={
        "avg_rent": ":,.0f",
        "median_rent": ":,.0f",
        "avg_sqft": ":,.0f",
        "listings": True,
    },
    center={
        "lat": center.y,
        "lon": center.x,
    },
    zoom=10.8,
    opacity=0.75,
    mapbox_style="carto-positron",
)

# Highlight selected neighborhood
fig_map.update_layout(
    mapbox_layers=[
        {
            "source": selected_geojson,
            "type": "line",
            "color": "#E63946",
            "line": {"width": 5},
        }
    ],
    margin=dict(l=0, r=0, t=0, b=0),
    height=650,
    coloraxis_colorbar=dict(title="Average Rent"),
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)


st.divider()
st.subheader(" Neighborhood vs City")

# ===========================================================
# Neighborhood vs City
# ===========================================================

st.divider()

# -----------------------------------------------------------
# Comparison table
# -----------------------------------------------------------

comparison = pd.DataFrame(
    {
        "Metric": [
            "Average Rent",
            "Median Rent",
            "Average Sq Ft",
            "Listings",
        ],
        selected_neighborhood: [
            avg_rent,
            median_rent,
            avg_sqft,
            listing_count,
        ],
        "San Francisco": [
            city_stats["avg_rent"],
            city_stats["median_rent"],
            city_stats["avg_sqft"],
            city_stats["listings"],
        ],
    }
)

comparison[selected_neighborhood] = comparison[selected_neighborhood].round(1)
comparison["San Francisco"] = comparison["San Francisco"].round(1)

# -----------------------------------------------------------
# Calculate differences
# -----------------------------------------------------------

rent_diff = (
    (avg_rent - city_stats["avg_rent"])
    / city_stats["avg_rent"]
) * 100

sqft_diff = (
    (avg_sqft - city_stats["avg_sqft"])
    / city_stats["avg_sqft"]
) * 100

compare_chart = pd.DataFrame(
    {
        "Metric": [
            "Average Rent",
            "Average Sq Ft",
        ],
        "Difference (%)": [
            rent_diff,
            sqft_diff,
        ],
    }
)

# -----------------------------------------------------------
# Difference chart
# -----------------------------------------------------------

fig_compare = px.bar(
    compare_chart,
    x="Metric",
    y="Difference (%)",
    color="Difference (%)",
    color_continuous_scale="RdBu",
    text="Difference (%)",
)

fig_compare.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside",
)

fig_compare.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=20, b=20),
    coloraxis_showscale=False,
    yaxis_title="Percent Difference",
)

# -----------------------------------------------------------
# Display
# -----------------------------------------------------------

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader(" Neighborhood vs City")
    st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True,
)

with right:
    st.subheader(" Difference from City Average")

    st.plotly_chart(
        fig_compare,
        use_container_width=True,
    )

# -----------------------------------------------------------
# Insight text
# -----------------------------------------------------------

if rent_diff >= 10:
    rent_text = "significantly more expensive"
elif rent_diff >= 0:
    rent_text = "slightly more expensive"
elif rent_diff >= -10:
    rent_text = "slightly more affordable"
else:
    rent_text = "significantly more affordable"

size_text = "larger" if sqft_diff > 0 else "smaller"

st.divider()
st.info(f"""
### Neighborhood Insights

**{selected_neighborhood}** is **{rent_text}** than the San Francisco average.

Homes are generally **{size_text}** than the city average.

The current filters returned **{listing_count:,}** listings.

This neighborhood has an average monthly rent of **${avg_rent:,.0f}**.
""")

