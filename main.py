import os
from src.load_data import load_historical_data, load_sentiment_data
from src.preprocess import preprocess_historical, preprocess_sentiment
from src.merge import merge_data
from src.analysis import (
    calculate_metrics, assign_sentiment_category,
    get_sentiment_wise_performance, segment_traders,
    get_segmented_sentiment_performance, run_simulation
)
from src.visualize import (
    plot_pnl_vs_sentiment, plot_win_rate_vs_sentiment, plot_leverage_vs_sentiment,
    plot_risk_adjusted, plot_segmented_performance, plot_simulation
)

def main():
    print("=" * 50)
    print("  Crypto Sentiment vs Trader Performance Pipeline")
    print("=" * 50)

    os.makedirs('outputs/plots', exist_ok=True)

    print("\n[1/6] Loading data...")
    hist_df = load_historical_data()
    sent_df = load_sentiment_data()

    if hist_df.empty or sent_df.empty:
        print("ERROR: Data files missing or empty. Populate data/ and retry.")
        return

    print("[2/6] Preprocessing...")
    hist_df = preprocess_historical(hist_df)
    sent_df = preprocess_sentiment(sent_df)

    print("[3/6] Merging datasets...")
    df = merge_data(hist_df, sent_df)

    print("[4/6] Calculating metrics...")
    df = calculate_metrics(df)
    df = assign_sentiment_category(df)
    df = segment_traders(df)

    print("[5/6] Generating insights...")
    perf_df = get_sentiment_wise_performance(df)
    seg_df  = get_segmented_sentiment_performance(df)
    sim     = run_simulation(df)

    if not perf_df.empty:
        print("\n--- Sentiment-Wise Performance ---")
        print(perf_df.to_string(index=False))

    if sim:
        print("\n--- Strategy Simulation ---")
        for name, metrics in sim.items():
            print(f"  {name}: Avg PnL={metrics['avg_pnl']:.2f}, Win Rate={metrics['win_rate']:.1%}, N={metrics['trade_count']}")

    print("\n[6/6] Saving visualizations...")
    plot_pnl_vs_sentiment(df)
    plot_win_rate_vs_sentiment(df)
    plot_leverage_vs_sentiment(df)
    plot_risk_adjusted(perf_df)
    plot_segmented_performance(seg_df)
    plot_simulation(sim)

    print("\nDone. All plots saved to outputs/plots/")
    print("=" * 50)

if __name__ == "__main__":
    main()
