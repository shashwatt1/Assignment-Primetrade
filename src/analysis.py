import pandas as pd
import numpy as np

def calculate_metrics(df):
    if df.empty:
        return df

    pnl_col = 'closedPnL' if 'closedPnL' in df.columns else 'pnl' if 'pnl' in df.columns else None
    if pnl_col:
        df['profit'] = pd.to_numeric(df[pnl_col], errors='coerce')
        df['win'] = (df['profit'] > 0).astype(int)

    if 'leverage' in df.columns:
        df['leverage'] = pd.to_numeric(df['leverage'], errors='coerce')

    return df


def assign_sentiment_category(df):
    # Detect the sentiment column dynamically — handles lowercase, suffixed, and aliased variants
    candidates = ['sentiment', 'classification', 'Classification',
                  'Classification_x', 'Classification_y',
                  'classification_sentiment', 'sentiment_sentiment']
    sentiment_col = next((c for c in candidates if c in df.columns), None)
    if sentiment_col is None:
        raise KeyError(
            f"No sentiment column found in DataFrame. "
            f"Available columns: {list(df.columns)}"
        )
    df['sentiment_category'] = df[sentiment_col]
    return df


def get_sentiment_wise_performance(df):
    """Aggregate key performance metrics per sentiment category."""
    if df.empty or 'profit' not in df.columns:
        return pd.DataFrame()

    df = assign_sentiment_category(df)

    agg = {}
    agg['avg_pnl'] = ('profit', 'mean')
    agg['total_pnl'] = ('profit', 'sum')
    agg['pnl_std'] = ('profit', 'std')
    agg['win_rate'] = ('win', 'mean')
    agg['trade_count'] = ('profit', 'count')
    if 'leverage' in df.columns:
        agg['avg_leverage'] = ('leverage', 'mean')

    perf = df.groupby('sentiment_category', observed=True).agg(**agg).reset_index()

    # Risk-adjusted: coefficient of variation (lower = more consistent)
    perf['pnl_cv'] = perf['pnl_std'] / perf['avg_pnl'].abs()

    return perf


def segment_traders(df):
    """Segment traders into Top 10% vs Bottom 90% by cumulative PnL."""
    if df.empty or 'profit' not in df.columns:
        return df

    # Identify a trader id column
    id_col = None
    for candidate in ['account', 'trader_id', 'trader', 'user', 'address']:
        if candidate in df.columns:
            id_col = candidate
            break

    if id_col is None:
        df['segment'] = 'All Traders'
        return df

    trader_profits = df.groupby(id_col)['profit'].sum().reset_index()
    threshold = trader_profits['profit'].quantile(0.90)
    trader_profits['segment'] = np.where(trader_profits['profit'] >= threshold, 'Top 10%', 'Bottom 90%')
    df = df.merge(trader_profits[[id_col, 'segment']], on=id_col, how='left')
    return df


def get_segmented_sentiment_performance(df):
    """Compare Top 10% vs Bottom 90% behavior across sentiment buckets."""
    if 'segment' not in df.columns or 'sentiment_category' not in df.columns:
        return pd.DataFrame()

    agg = {}
    agg['avg_pnl'] = ('profit', 'mean')
    agg['win_rate'] = ('win', 'mean')
    agg['trade_count'] = ('profit', 'count')
    if 'leverage' in df.columns:
        agg['avg_leverage'] = ('leverage', 'mean')

    return df.groupby(['segment', 'sentiment_category'], observed=True).agg(**agg).reset_index()


def run_simulation(df):
    """
    Mini simulation: compare baseline (all trades) vs
    sentiment-filtered strategy (trades placed only during Fear / Extreme Fear).
    """
    if df.empty or 'sentiment_category' not in df.columns:
        return {}

    baseline = {
        'avg_pnl': df['profit'].mean(),
        'win_rate': df['win'].mean(),
        'trade_count': len(df)
    }

    fear_df = df[df['sentiment_category'].isin(['Fear', 'Extreme Fear'])]
    fear_strategy = {
        'avg_pnl': fear_df['profit'].mean() if not fear_df.empty else 0,
        'win_rate': fear_df['win'].mean() if not fear_df.empty else 0,
        'trade_count': len(fear_df)
    }

    return {'Baseline (All Trades)': baseline, 'Fear-Only Strategy': fear_strategy}
