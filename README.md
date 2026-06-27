# SF Housing Rent Intelligence Platform

A full-stack data analytics project for exploring and predicting San Francisco rental market trends. The project combines data cleaning, validation, geospatial analysis, machine learning, and an interactive Streamlit dashboard.

## Overview

This repository analyzes San Francisco rental inventory data from the San Francisco Rent Board to help users understand:

- neighborhood-level rent patterns
- housing market trends across the city
- property characteristics that influence rent
- recommendations for neighborhoods based on user preferences

The app is designed as an end-to-end analytics workflow, from raw data ingestion to interactive visualization and prediction.

## Features

- Market overview dashboard with rental trends and summary metrics
- Neighborhood explorer with filters, comparisons, and map-based views
- Neighborhood recommendation engine for matching user preferences
- Rent predictor for estimating monthly rent from property attributes
- Data quality and preprocessing pipeline for preparing clean, model-ready datasets

## Project Structure

- app/ — Streamlit application pages, styling, and shared utilities
- data/ — raw data, processed CSV files, and GeoJSON neighborhood files
- notebooks/ — exploratory data analysis and modeling notebooks
- src/ — data cleaning and validation modules
- models/ — trained model artifacts

## Data Source

The project uses public rental inventory data from the San Francisco Rent Board.

## Setup

1. Clone the repository.
2. Create and activate a Python environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app locally:

   ```bash
   streamlit run app/Home.py
   ```

## Requirements

The app depends on packages such as:

- streamlit
- pandas
- numpy
- plotly
- geopandas
- scikit-learn
- joblib
- matplotlib
- seaborn

## Notes

Processed datasets and geospatial files are already included under the data folder, so the dashboard can be run without reprocessing the raw source files unless you want to rebuild the pipeline from scratch.
