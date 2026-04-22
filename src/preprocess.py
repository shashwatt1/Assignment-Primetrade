import pandas as pd

def preprocess_historical(df):
    if df.empty:
        return df
    # Assuming 'timestamp' or 'date' column exists, try to parse it
    date_col = 'timestamp' if 'timestamp' in df.columns else 'date' if 'date' in df.columns else None
    if date_col:
        df['datetime'] = pd.to_datetime(df[date_col])
        df['date'] = df['datetime'].dt.date
    
    # Handle basic cleaning
    # Additional cleaning can be added here
    return df

def preprocess_sentiment(df):
    if df.empty:
        return df
    # Assuming 'timestamp' or 'date' exists
    date_col = 'timestamp' if 'timestamp' in df.columns else 'date' if 'date' in df.columns else None
    if date_col:
        df['datetime'] = pd.to_datetime(df[date_col])
        df['date'] = df['datetime'].dt.date
        
    # Ensure sentiment value is numeric
    if 'value' in df.columns:
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    return df
