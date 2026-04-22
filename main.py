import os
from src.load_data import load_historical_data, load_sentiment_data
from src.preprocess import preprocess_historical, preprocess_sentiment
from src.merge import merge_data
from src.analysis import calculate_metrics, get_sentiment_wise_performance, segment_traders
from src.visualize import plot_pnl_vs_sentiment, plot_win_rate_vs_sentiment, plot_leverage_vs_sentiment

def main():
    print("Starting pipeline...")
    
    # Ensure output directory exists
    os.makedirs('outputs/plots', exist_ok=True)
    
    print("Loading data...")
    hist_df = load_historical_data()
    sent_df = load_sentiment_data()
    
    if hist_df.empty or sent_df.empty:
        print("Data files are empty or not found. Please populate data/ directory. Pipeline halted.")
        return
        
    print("Preprocessing data...")
    hist_df = preprocess_historical(hist_df)
    sent_df = preprocess_sentiment(sent_df)
    
    print("Merging datasets...")
    merged_df = merge_data(hist_df, sent_df)
    
    print("Calculating metrics...")
    analyzed_df = calculate_metrics(merged_df)
    
    print("Generating insights...")
    perf_df = get_sentiment_wise_performance(analyzed_df)
    
    # Segment traders
    analyzed_df = segment_traders(analyzed_df)
    
    if not perf_df.empty:
        print("\nSentiment-Wise Performance:")
        print(perf_df)
    else:
        print("\nNo matching data found to aggregate sentiment metrics. Please verify columns.")
    
    print("\nGenerating visualizations...")
    plot_pnl_vs_sentiment(analyzed_df)
    plot_win_rate_vs_sentiment(analyzed_df)
    plot_leverage_vs_sentiment(analyzed_df)
    
    print("\nPipeline complete. Plots saved to outputs/plots/")

if __name__ == "__main__":
    main()
