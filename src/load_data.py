import pandas as pd
import os

def load_historical_data(filepath="data/historical_data.csv"):
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Returning empty DataFrame.")
        return pd.DataFrame()
    return pd.read_csv(filepath)

def load_sentiment_data(filepath="data/fear_greed_index.csv"):
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Returning empty DataFrame.")
        return pd.DataFrame()
    return pd.read_csv(filepath)
