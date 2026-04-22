import pandas as pd

def merge_data(historical_df, sentiment_df):
    if historical_df.empty or sentiment_df.empty:
        return pd.DataFrame()

    # Merge on the 'date' column
    if 'date' not in historical_df.columns or 'date' not in sentiment_df.columns:
        return pd.DataFrame()

    merged = pd.merge(historical_df, sentiment_df, on='date', how='inner', suffixes=('', '_sentiment'))

    # Normalise the classification/sentiment column to a single canonical name 'sentiment'
    # so assign_sentiment_category() always finds it regardless of suffix variations.
    classification_candidates = [
        'classification', 'Classification',
        'classification_sentiment', 'Classification_sentiment',
        'Classification_x', 'Classification_y',
        'sentiment',
    ]
    for col in classification_candidates:
        if col in merged.columns and col != 'sentiment':
            merged.rename(columns={col: 'sentiment'}, inplace=True)
            break

    return merged
