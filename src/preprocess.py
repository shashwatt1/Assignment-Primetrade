import pandas as pd

def preprocess_historical(df):
    if df.empty:
        return df

    # ── Date extraction ──────────────────────────────────────────────────────
    # Real CSV uses 'Timestamp IST' (e.g. '02-12-2024 22:50', dayfirst format)
    # Fallback to epoch-ms 'Timestamp' column if present.
    if 'Timestamp IST' in df.columns:
        df['datetime'] = pd.to_datetime(df['Timestamp IST'], dayfirst=True, errors='coerce')
    elif 'timestamp' in df.columns:
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', errors='coerce')
    elif 'date' in df.columns:
        df['datetime'] = pd.to_datetime(df['date'], errors='coerce')

    if 'datetime' in df.columns:
        df['date'] = df['datetime'].dt.date

    # ── Column normalisation ─────────────────────────────────────────────────
    # Map real CSV headers to the canonical names expected by analysis.py
    rename_map = {}
    if 'Closed PnL' in df.columns and 'closedPnL' not in df.columns:
        rename_map['Closed PnL'] = 'closedPnL'
    if 'Account' in df.columns and 'account' not in df.columns:
        rename_map['Account'] = 'account'
    # 'Size USD' is a reasonable leverage proxy when no explicit leverage column exists
    if 'Size USD' in df.columns and 'leverage' not in df.columns:
        rename_map['Size USD'] = 'leverage'
    if rename_map:
        df = df.rename(columns=rename_map)

    return df


def preprocess_sentiment(df):
    if df.empty:
        return df

    # ── Date extraction ──────────────────────────────────────────────────────
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    elif 'timestamp' in df.columns:
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
        df['date'] = df['datetime'].dt.date

    # Ensure sentiment value is numeric
    if 'value' in df.columns:
        df['value'] = pd.to_numeric(df['value'], errors='coerce')

    return df
