import pandas as pd
import numpy as np

def calculate_metrics(df):
    if df.empty:
        return df
    
    # Create profit indicator
    pnl_col = 'closedPnL' if 'closedPnL' in df.columns else 'pnl' if 'pnl' in df.columns else None
    if pnl_col:
        df['profit'] = df[pnl_col]
        df['win'] = (df['profit'] > 0).astype(int)
        
    return df

def get_sentiment_wise_performance(df):
    if df.empty or 'value' not in df.columns or 'profit' not in df.columns:
        return pd.DataFrame()
    
    # Map sentiment values to categories: 0-25 Extreme Fear, 26-45 Fear, 46-54 Neutral, 55-75 Greed, 76-100 Extreme Greed
    bins = [0, 25, 45, 54, 75, 100]
    labels = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
    df['sentiment_category'] = pd.cut(df['value'], bins=bins, labels=labels, include_lowest=True)
    
    # Aggregate performance
    perf = df.groupby('sentiment_category', observed=True).agg({
        'profit': ['mean', 'sum'],
        'win': 'mean',
        'leverage': 'mean' if 'leverage' in df.columns else 'count' # fallback if leverage missing
    }).reset_index()
    
    return perf

def segment_traders(df):
    # Segment top 10% traders by total profit vs others
    if df.empty or 'trader_id' not in df.columns or 'profit' not in df.columns:
        return df
        
    trader_profits = df.groupby('trader_id')['profit'].sum().reset_index()
    threshold = trader_profits['profit'].quantile(0.9)
    
    trader_profits['segment'] = np.where(trader_profits['profit'] >= threshold, 'Top 10%', 'Bottom 90%')
    
    # Merge back
    df = df.merge(trader_profits[['trader_id', 'segment']], on='trader_id', how='left')
    return df
