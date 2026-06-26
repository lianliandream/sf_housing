import streamlit as st
import plotly.express as px

from utils import load_data

st.title("📊 Market Overview")

df = load_data()

st.sidebar.header("Filters")

selected_neighborhoods = st.sidebar.multiselect(
    "Neighborhood",
    sorted(df["neighborhood"].dropna().unique()),
    default=sorted(df["neighborhood"].dropna().unique())
)

filtered = df[
    df["neighborhood"].isin(selected_neighborhoods)
]


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Listings",
    f"{len(filtered):,}"
)

col2.metric(
    "Average Rent",
    f"${filtered['rent'].mean():,.0f}"
)

col3.metric(
    "Median Rent",
    f"${filtered['rent'].median():,.0f}"
)

col4.metric(
    "Neighborhoods",
    filtered["neighborhood"].nunique()
)


fig = px.histogram(
    filtered,
    x="rent",
    nbins=40,
    title="Monthly Rent Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


avg = (
    filtered
    .groupby("neighborhood")["rent"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    avg,
    x="neighborhood",
    y="rent",
    title="Average Rent by Neighborhood"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

fig = px.scatter(
    filtered,
    x="sqft",
    y="rent",
    color="bedrooms",
    hover_name="neighborhood",
    title="Rent vs Square Footage"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Listing Locations")

st.map(
    filtered[
        ["latitude", "longitude"]
    ]
)