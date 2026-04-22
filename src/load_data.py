import pandas as pd
import os

# Anchor paths relative to the project root (parent of src/)
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SRC_DIR)

def load_historical_data(filepath=None):
    if filepath is None:
        filepath = os.path.join(_PROJECT_ROOT, 'data', 'historical_data.csv')
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Returning empty DataFrame.")
        return pd.DataFrame()
    return pd.read_csv(filepath)

def load_sentiment_data(filepath=None):
    if filepath is None:
        filepath = os.path.join(_PROJECT_ROOT, 'data', 'fear_greed_index.csv')
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Returning empty DataFrame.")
        return pd.DataFrame()
    return pd.read_csv(filepath)
