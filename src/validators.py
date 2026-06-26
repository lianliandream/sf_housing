"""
validators.py

Validation functions for the SF Housing Intelligence Platform.
"""

import pandas as pd


# ==========================================================
# Missing Values
# ==========================================================

def validate_missing_values(df):
    """Return missing value summary."""

    summary = pd.DataFrame({
        "Missing": df.isna().sum(),
        "Percent": (df.isna().mean() * 100).round(2)
    })

    return summary.sort_values("Percent", ascending=False)


# ==========================================================
# Duplicate IDs
# ==========================================================

def validate_duplicates(df):
    """Check duplicate unique IDs."""

    duplicates = df["unique_id"].duplicated().sum()

    print("=" * 50)
    print("Duplicate Validation")
    print("=" * 50)
    print(f"Duplicate unique_id: {duplicates}")

    return duplicates


# ==========================================================
# Rent
# ==========================================================

def validate_rent(df):

    print("=" * 50)
    print("Monthly Rent")
    print("=" * 50)

    print(df["monthly_rent_mid"].describe())


# ==========================================================
# Square Footage
# ==========================================================

def validate_square_footage(df):

    print("=" * 50)
    print("Square Footage")
    print("=" * 50)

    print(df["square_footage_mid"].describe())


# ==========================================================
# Bedrooms
# ==========================================================

def validate_bedrooms(df):

    print("=" * 50)
    print("Bedrooms")
    print("=" * 50)

    print(
        df["bedroom_num"]
        .value_counts(dropna=False)
        .sort_index()
    )


# ==========================================================
# Bathrooms
# ==========================================================

def validate_bathrooms(df):

    print("=" * 50)
    print("Bathrooms")
    print("=" * 50)

    print(
        df["bathroom_num"]
        .value_counts(dropna=False)
        .sort_index()
    )


# ==========================================================
# Coordinates
# ==========================================================

def validate_coordinates(df):

    print("=" * 50)
    print("Coordinates")
    print("=" * 50)

    print("\nLongitude")
    print(df["longitude"].describe())

    print("\nLatitude")
    print(df["latitude"].describe())


# ==========================================================
# Unknown Bedrooms
# ==========================================================

def unknown_bedrooms(df):

    print("=" * 50)
    print("Unknown Bedroom Categories")
    print("=" * 50)

    unknown = df.loc[
        df["bedroom_num"].isna(),
        "bedroom_count"
    ]

    print(unknown.value_counts())


# ==========================================================
# Unknown Bathrooms
# ==========================================================

def unknown_bathrooms(df):

    print("=" * 50)
    print("Unknown Bathroom Categories")
    print("=" * 50)

    unknown = df.loc[
        df["bathroom_num"].isna(),
        "bathroom_count"
    ]

    print(unknown.value_counts())