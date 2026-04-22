import pandas as pd

def merge_data(historical_df, sentiment_df):
    if historical_df.empty or sentiment_df.empty:
        return pd.DataFrame()
    
    # Merge on the 'date' column
    if 'date' in historical_df.columns and 'date' in sentiment_df.columns:
        merged = pd.merge(historical_df, sentiment_df, on='date', how='inner', suffixes=('', '_sentiment'))
        return merged
    return pd.DataFrame()
