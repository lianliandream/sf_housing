"""
cleaning.py

ETL cleaning functions for the SF Housing Intelligence Platform.
"""

import re
import numpy as np
import pandas as pd

# ==========================================================
# CONSTANTS
# ==========================================================

BEDROOM_MAP = {
    "studio": 0,
    "zero-(studio)": 0,
    "zero -(studio)": 0,
    "0": 0,

    "one-bedroom": 1,
    "one bedroom": 1,
    "1 bedroom": 1,
    "1 bedroom ": 1,
    "1bedroom": 1,
    "1 bedroom": 1,
    "1br": 1,
    "1 bed": 1,
    "1": 1,

    "two-bedroom": 2,
    "two bedroom": 2,
    "2 bedroom": 2,
    "2br": 2,
    "2brd": 2,
    "2": 2,

    "three-bedroom": 3,
    "three bedroom": 3,
    "3 bedroom": 3,
    "3bedroom": 3,
    "3": 3,

    "four-bedroom": 4,
    "four bedroom": 4,

    "five-bedroom": 5,
    "5+": 5,
}

BATHROOM_MAP = {
    "one bathroom": 1,
    "one-bathroom": 1,
    "one bathroom ": 1,
    "one bathroom": 1,
    "one bathroom": 1,
    "1 bathroom": 1,
    "1bathroom": 1,
    "1": 1,
    "1.00": 1,

    "one and a half bathrooms": 1.5,

    "two bathrooms": 2,
    "two bathroom": 2,
    "two-bathroom": 2,
    "2 bathroom": 2,
    "2": 2,
    "2.00": 2,

    "two and a half bathrooms": 2.5,
    "2.5": 2.5,

    "three bathrooms or more": 3,
    "3.5": 3.5,

    "shared bathroom facilities with other units": 0.5,
}

# ==========================================================
# HELPERS
# ==========================================================

def normalize_text(value):
    """
    Normalize strings before mapping.
    """

    if pd.isna(value):
        return np.nan

    value = str(value).lower().strip()

    value = re.sub(r"\s+", " ", value)

    return value


# ==========================================================
# MONTHLY RENT
# ==========================================================

def clean_monthly_rent(series: pd.Series) -> pd.Series:
    """
    Convert rent ranges into numeric midpoints.

    Example
    -------
    $1001-$1250 -> 1125.5
    """

    def convert(value):

        if pd.isna(value):
            return np.nan

        value = str(value)

        value = value.replace("$", "")
        value = value.replace(",", "")
        value = value.strip()

        numbers = re.findall(r"\d+", value)

        if len(numbers) == 2:
            low, high = map(int, numbers)
            return (low + high) / 2

        return np.nan

    return series.apply(convert)


# ==========================================================
# SQUARE FOOTAGE
# ==========================================================

def clean_square_footage(series: pd.Series) -> pd.Series:
    """
    Convert square footage ranges into numeric midpoints.

    Example
    -------
    501-750 Sq.Ft -> 625.5
    4000+ Sq.Ft -> 4000
    """

    def convert(value):

        if pd.isna(value):
            return np.nan

        value = str(value)

        if value.lower() == "unknown":
            return np.nan

        value = value.replace("Sq.ft", "Sq.Ft")
        value = value.replace("Sq.Ft", "")
        value = value.strip()

        if "+" in value:
            return float(value.replace("+", ""))

        numbers = re.findall(r"\d+", value)

        if len(numbers) == 2:
            low, high = map(int, numbers)
            return (low + high) / 2

        return np.nan

    return series.apply(convert)


# ==========================================================
# BEDROOMS
# ==========================================================

def clean_bedroom_count(series: pd.Series) -> pd.Series:
    """
    Convert bedroom categories into numeric values.
    """

    def convert(value):

        value = normalize_text(value)

        if pd.isna(value):
            return np.nan

        return BEDROOM_MAP.get(value, np.nan)

    return series.apply(convert)


# ==========================================================
# BATHROOMS
# ==========================================================

def clean_bathroom_count(series: pd.Series) -> pd.Series:
    """
    Convert bathroom categories into numeric values.
    """

    def convert(value):

        value = normalize_text(value)

        if pd.isna(value):
            return np.nan

        return BATHROOM_MAP.get(value, np.nan)

    return series.apply(convert)


# ==========================================================
# COORDINATES
# ==========================================================

def extract_coordinates(series: pd.Series) -> pd.DataFrame:
    """
    Extract longitude and latitude from POINT column.

    Example
    -------
    POINT (-122.41 37.75)
    """

    coordinates = series.str.extract(
        r"POINT\s*\((-?\d+\.\d+)\s+(-?\d+\.\d+)\)"
    )

    coordinates.columns = [
        "longitude",
        "latitude"
    ]

    coordinates = coordinates.astype(float)

    return coordinates


# ==========================================================
# DATE COLUMNS
# ==========================================================

def clean_dates(df: pd.DataFrame) -> pd.DataFrame:

    date_columns = [
        "occupancy_or_vacancy_date",
        "vacancy_date",
        "signature_date",
        "data_as_of",
        "data_loaded_at"
    ]

    for col in date_columns:

        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

    return df


# ==========================================================
# MASTER CLEANING FUNCTION
# ==========================================================

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run complete ETL cleaning pipeline.
    """

    df = df.copy()

    print("Cleaning monthly rent...")

    df["monthly_rent_mid"] = clean_monthly_rent(
        df["monthly_rent"]
    )

    print("Cleaning square footage...")

    df["square_footage_mid"] = clean_square_footage(
        df["square_footage"]
    )

    print("Cleaning bedrooms...")

    df["bedroom_num"] = clean_bedroom_count(
        df["bedroom_count"]
    )

    print("Cleaning bathrooms...")

    df["bathroom_num"] = clean_bathroom_count(
        df["bathroom_count"]
    )

    print("Extracting coordinates...")

    coords = extract_coordinates(
        df["point"]
    )

    df = pd.concat(
        [df, coords],
        axis=1
    )

    print("Cleaning dates...")

    df = clean_dates(df)

    print("Done!")

    return df