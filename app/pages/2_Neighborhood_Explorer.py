import pandas as pd
import streamlit as st
from pathlib import Path

import json
import plotly.express as px


# ===========================================================
# Page Config
# ===========================================================

st.set_page_config(
    page_title="Neighborhood Explorer",
    page_icon="🏘️",
    layout="wide"
)

# ===========================================================
# Load Data
# ===========================================================

ROOT = Path(__file__).resolve().parent.parent.parent

DATA_PATH = (
    ROOT
    / "data"
    / "processed"
    / "sf_housing_model_ready.csv"
)

df = pd.read_csv(DATA_PATH)

# ===========================================================
# Rename Columns
# ===========================================================

df = df.rename(columns={

    "analysis_neighborhood":"neighborhood",

    "monthly_rent_mid":"rent",

    "square_footage_mid":"sqft",

    "bedroom_num":"bedrooms",

    "bathroom_num":"bathrooms"

})


# ===========================================================
# City Statistics
# ===========================================================

city_avg_rent = df["rent"].mean()
city_median_rent = df["rent"].median()
city_avg_sqft = df["sqft"].mean()
city_listings = len(df)

# ===========================================================
# Sidebar
# ===========================================================

st.sidebar.title("Neighborhood Explorer")

st.sidebar.markdown("---")

st.sidebar.subheader("Explore")

# Neighborhood

selected_neighborhood = st.sidebar.selectbox(

    "Neighborhood",

    sorted(df["neighborhood"].dropna().unique())

)

# Bedrooms

bedroom_options = sorted(df["bedrooms"].dropna().unique())

selected_bedrooms = st.sidebar.multiselect(

    "Bedrooms",

    bedroom_options,

    default=bedroom_options

)

# Bathrooms

bathroom_options = sorted(df["bathrooms"].dropna().unique())

selected_bathrooms = st.sidebar.multiselect(

    "Bathrooms",

    bathroom_options,

    default=bathroom_options

)

# Rent

rent_range = st.sidebar.slider(

    "Monthly Rent",

    int(df["rent"].min()),

    int(df["rent"].max()),

    (

        int(df["rent"].min()),

        int(df["rent"].max())

    )

)

# Square Footage

sqft_range = st.sidebar.slider(

    "Square Footage",

    int(df["sqft"].min()),

    int(df["sqft"].max()),

    (

        int(df["sqft"].min()),

        int(df["sqft"].max())

    )

)

# ===========================================================
# Apply Filters
# ===========================================================

filtered = df[

    (df["neighborhood"] == selected_neighborhood)

    & (df["bedrooms"].isin(selected_bedrooms))

    & (df["bathrooms"].isin(selected_bathrooms))

    & (df["rent"].between(rent_range[0], rent_range[1]))

    & (df["sqft"].between(sqft_range[0], sqft_range[1]))

]

# ===========================================================
# Header
# ===========================================================

st.title(selected_neighborhood)

st.caption(
    "Interactive Neighborhood Analytics"
)

st.divider()

# ===========================================================
# KPI Cards
# ===========================================================

avg_rent = filtered["rent"].mean()

median_rent = filtered["rent"].median()

avg_sqft = filtered["sqft"].mean()

listing_count = len(filtered)

c1, c2, c3, c4 = st.columns(4)

c1.metric(

    "Average Rent",

    f"${avg_rent:,.0f}"

)

c2.metric(

    "Median Rent",

    f"${median_rent:,.0f}"

)

c3.metric(

    "Listings",

    f"{listing_count:,}"

)

c4.metric(

    "Average Sq Ft",

    f"{avg_sqft:,.0f}"

)

# ===========================================================
# Summary
# ===========================================================

st.divider()

st.subheader("Neighborhood Summary")

st.write(

f"""
### {selected_neighborhood}

The current filters returned **{listing_count:,}** rental listings.

The average monthly rent is **${avg_rent:,.0f}**.

Median monthly rent is **${median_rent:,.0f}**.

Average unit size is **{avg_sqft:,.0f} sq ft**.
"""

)



# ===========================================================
# Load GeoJSON
# ===========================================================

GEOJSON_PATH = (
    ROOT
    / "data"
    / "geojson"
    / "sf_analysis_neighborhoods.geojson"
)

with open(GEOJSON_PATH, encoding="utf-8") as f:
    geojson = json.load(f)

# ===========================================================
# Neighborhood Summary Data
# ===========================================================

map_df = (

    df

    .groupby("neighborhood")

    .agg(

        avg_rent=("rent","mean"),

        median_rent=("rent","median"),

        listings=("rent","count"),

        avg_sqft=("sqft","mean")

    )

    .reset_index()

)


st.divider()

st.subheader("San Francisco Neighborhood Map")



fig = px.choropleth_mapbox(

    map_df,

    geojson=geojson,

    locations="neighborhood",

    featureidkey="properties.nhood",

    color="avg_rent",

    color_continuous_scale="Blues",

    hover_name="neighborhood",

    hover_data={

        "avg_rent":":,.0f",

        "median_rent":":,.0f",

        "avg_sqft":":,.0f",

        "listings":True

    },

    center={

        "lat":37.7749,

        "lon":-122.4194

    },

    zoom=11,

    opacity=0.75,

    mapbox_style="carto-positron"

)


fig.update_layout(

    margin=dict(

        l=0,

        r=0,

        t=0,

        b=0

    ),

    height=650,

    coloraxis_colorbar=dict(

        title="Average Rent"

    )

)


st.plotly_chart(

    fig,

    use_container_width=True

)


city_listings = len(df)


st.divider()

st.subheader("Neighborhood vs City")



comparison = pd.DataFrame({

    "Metric":[

        "Average Rent",

        "Median Rent",

        "Average Sq Ft",

        "Listings"

    ],

    selected_neighborhood:[

        avg_rent,

        median_rent,

        avg_sqft,

        listing_count

    ],

    "San Francisco":[

        city_avg_rent,

        city_median_rent,

        city_avg_sqft,

        city_listings

    ]

})

st.dataframe(
    comparison,
    use_container_width=True
)


rent_diff = (
    (avg_rent-city_avg_rent)
    / city_avg_rent
)*100

sqft_diff = (
    (avg_sqft-city_avg_sqft)
    / city_avg_sqft
)*100

compare_chart = pd.DataFrame({

    "Metric":[

        "Average Rent",

        "Average Sq Ft"

    ],

    "Difference":[

        rent_diff,

        sqft_diff

    ]

})

fig = px.bar(

    compare_chart,

    x="Metric",

    y="Difference",

    color="Difference",

    title="Difference from City Average (%)",

    text="Difference"

)

fig.update_traces(

    texttemplate="%{text:.1f}%",

    textposition="outside"

)

st.plotly_chart(
    fig,
    use_container_width=True
)


if rent_diff > 10:
    rent_text = "significantly more expensive"
elif rent_diff > 0:
    rent_text = "slightly more expensive"
elif rent_diff > -10:
    rent_text = "slightly more affordable"
else:
    rent_text = "significantly more affordable"

if sqft_diff > 0:
    size_text = "larger"
else:
    size_text = "smaller"

st.info(f"""
### Neighborhood Insights

**{selected_neighborhood}** is **{rent_text}** than the San Francisco average.

Homes are generally **{size_text}** than the city average.

The current filters returned **{listing_count:,}** listings.

This neighborhood has an average monthly rent of **${avg_rent:,.0f}**.
""")

