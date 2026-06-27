import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Neighborhood Recommendations",
    layout="wide"
)

ROOT = Path(__file__).resolve().parent.parent.parent

DATA_PATH = (
    ROOT
    / "data"
    / "processed"
    / "sf_housing_model_ready.csv"
)

df = pd.read_csv(DATA_PATH)



df = df.rename(columns={
    "analysis_neighborhood": "neighborhood",
    "monthly_rent_mid": "rent",
    "square_footage_mid": "sqft",
    "bedroom_num": "bedrooms",
    "bathroom_num": "bathrooms"
})


ranking = (
    df
    .groupby("neighborhood")
    .agg(
        Average_Rent=("rent", "mean"),
        Listings=("rent", "count"),
        Average_Sqft=("sqft", "mean")
    )
    .sort_values("Average_Rent")
)


st.title(" Neighborhood Recommendation Engine")

st.caption(
    "Find the best San Francisco neighborhoods based on your priorities."
)

st.divider()

# -------------------------------------------------------
# Recommendation Engine
# -------------------------------------------------------
 

 
recommendation_type = st.selectbox(

    "What are you looking for?",

    [

        "Budget Friendly",

        "Luxury Living",

        "Large Apartments",

        "Most Inventory",

        "Best Value"

    ]

)

# Create Value Score
ranking["Value_Score"] = (
    ranking["Average_Sqft"]
    / ranking["Average_Rent"]
) * 1000

# Choose recommendation
if recommendation_type == "Budget Friendly":

    recommendation = (
        ranking
        .sort_values("Average_Rent", ascending=True)
        .head(10)
    )

    message = "These neighborhoods have the lowest average monthly rent."

elif recommendation_type == "Luxury Living":

    recommendation = (
        ranking
        .sort_values("Average_Rent", ascending=False)
        .head(10)
    )

    message = "These neighborhoods have the highest average monthly rent."

elif recommendation_type == "Large Apartments":

    recommendation = (
        ranking
        .sort_values("Average_Sqft", ascending=False)
        .head(10)
    )

    message = "These neighborhoods offer the largest average living space."

elif recommendation_type == "Most Inventory":

    recommendation = (
        ranking
        .sort_values("Listings", ascending=False)
        .head(10)
    )

    message = "These neighborhoods currently have the greatest number of listings."

else:

    recommendation = (
        ranking
        .sort_values("Value_Score", ascending=False)
        .head(10)
    )

    message = "These neighborhoods provide the best square footage per rental dollar."

st.success(message)

st.dataframe(
    recommendation.round(2),
    use_container_width=True
)