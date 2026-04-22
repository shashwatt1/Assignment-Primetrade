import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd

PALETTE = {
    'Extreme Fear': '#d62728',
    'Fear':         '#ff7f0e',
    'Neutral':      '#bcbd22',
    'Greed':        '#2ca02c',
    'Extreme Greed':'#1f77b4',
}
ORDERED_CATS = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']

def _style():
    sns.set_theme(style="whitegrid", font_scale=1.1)
    plt.rcParams.update({
        'figure.figsize': (11, 6),
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelsize': 12,
    })

def _ordered(df, col='sentiment_category'):
    df = df.copy()
    df[col] = pd.Categorical(df[col], categories=ORDERED_CATS, ordered=True)
    return df.sort_values(col)

def _save(save_dir, filename):
    """Safely create output directory and return full save path."""
    os.makedirs(save_dir, exist_ok=True)
    return os.path.join(save_dir, filename)


def plot_pnl_vs_sentiment(df, save_dir='outputs/plots/'):
    _style()
    if 'sentiment_category' not in df.columns or 'profit' not in df.columns:
        return
    agg = df.groupby('sentiment_category', observed=True)['profit'].agg(['mean', 'std']).reset_index()
    agg = _ordered(agg)
    colors = [PALETTE.get(c, '#888') for c in agg['sentiment_category']]

    fig, ax = plt.subplots()
    ax.bar(agg['sentiment_category'], agg['mean'], yerr=agg['std'],
           color=colors, capsize=5, edgecolor='white', linewidth=0.8)
    ax.axhline(0, color='grey', linewidth=0.8, linestyle='--')
    ax.set_title("Average PnL per Trade by Sentiment\n(Error bars = ±1 std dev)")
    ax.set_ylabel("Avg PnL (USD)")
    ax.set_xlabel("Sentiment Category")
    plt.tight_layout()
    plt.savefig(_save(save_dir, 'pnl_vs_sentiment.png'), dpi=150)
    plt.show()


def plot_win_rate_vs_sentiment(df, save_dir='outputs/plots/'):
    _style()
    if 'sentiment_category' not in df.columns or 'win' not in df.columns:
        return
    agg = df.groupby('sentiment_category', observed=True)['win'].mean().reset_index()
    agg = _ordered(agg)
    colors = [PALETTE.get(c, '#888') for c in agg['sentiment_category']]

    fig, ax = plt.subplots()
    ax.bar(agg['sentiment_category'], agg['win'] * 100, color=colors, edgecolor='white', linewidth=0.8)
    ax.axhline(50, color='grey', linewidth=0.8, linestyle='--', label='Break-even (50%)')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_title("Win Rate by Sentiment Category")
    ax.set_ylabel("Win Rate (%)")
    ax.set_xlabel("Sentiment Category")
    ax.legend()
    plt.tight_layout()
    plt.savefig(_save(save_dir, 'win_rate_vs_sentiment.png'), dpi=150)
    plt.show()


def plot_leverage_vs_sentiment(df, save_dir='outputs/plots/'):
    _style()
    if 'sentiment_category' not in df.columns or 'leverage' not in df.columns:
        return
    plot_df = _ordered(df)

    fig, ax = plt.subplots()
    sns.boxplot(data=plot_df, x='sentiment_category', y='leverage',
                hue='sentiment_category', palette=PALETTE, order=ORDERED_CATS,
                legend=False, ax=ax,
                flierprops=dict(marker='o', markersize=3, alpha=0.4))
    ax.set_title("Leverage Distribution by Sentiment Category")
    ax.set_ylabel("Leverage (x)")
    ax.set_xlabel("Sentiment Category")
    plt.tight_layout()
    plt.savefig(_save(save_dir, 'leverage_vs_sentiment.png'), dpi=150)
    plt.show()


def plot_risk_adjusted(perf_df, save_dir='outputs/plots/'):
    """Side-by-side: avg PnL vs PnL standard deviation per sentiment."""
    _style()
    if perf_df.empty or 'avg_pnl' not in perf_df.columns:
        return
    perf_df = _ordered(perf_df)
    colors = [PALETTE.get(c, '#888') for c in perf_df['sentiment_category']]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].bar(perf_df['sentiment_category'], perf_df['avg_pnl'], color=colors, edgecolor='white')
    axes[0].set_title("Average PnL by Sentiment")
    axes[0].set_ylabel("Avg PnL (USD)")
    axes[0].set_xlabel("Sentiment Category")

    axes[1].bar(perf_df['sentiment_category'], perf_df['pnl_std'], color=colors, edgecolor='white')
    axes[1].set_title("Return Volatility (Std Dev) by Sentiment")
    axes[1].set_ylabel("PnL Std Dev")
    axes[1].set_xlabel("Sentiment Category")

    fig.suptitle("Return vs Risk by Sentiment Category", fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig(_save(save_dir, 'risk_adjusted.png'), dpi=150)
    plt.show()


def plot_segmented_performance(seg_df, save_dir='outputs/plots/'):
    """Compare Top 10% vs Bottom 90% win rate across sentiment buckets."""
    _style()
    if seg_df.empty or 'win_rate' not in seg_df.columns:
        return
    seg_df = _ordered(seg_df)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=seg_df, x='sentiment_category', y='win_rate',
                hue='segment', order=ORDERED_CATS, palette=['#1f77b4', '#aec7e8'], ax=ax)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.axhline(0.5, color='red', linewidth=0.8, linestyle='--', label='Break-even')
    ax.set_title("Win Rate: Top 10% vs Bottom 90% Traders by Sentiment")
    ax.set_ylabel("Win Rate")
    ax.set_xlabel("Sentiment Category")
    ax.legend(title='Trader Segment')
    plt.tight_layout()
    plt.savefig(_save(save_dir, 'segmented_performance.png'), dpi=150)
    plt.show()


def plot_simulation(sim_results, save_dir='outputs/plots/'):
    """Bar chart comparing baseline vs fear-only strategy."""
    _style()
    if not sim_results:
        return

    labels = list(sim_results.keys())
    avg_pnl   = [sim_results[k]['avg_pnl'] for k in labels]
    win_rates = [sim_results[k]['win_rate'] * 100 for k in labels]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].bar(labels, avg_pnl, color=['#aec7e8', '#1f77b4'], edgecolor='white')
    axes[0].set_title("Avg PnL: Baseline vs Strategy")
    axes[0].set_ylabel("Avg PnL (USD)")

    axes[1].bar(labels, win_rates, color=['#aec7e8', '#1f77b4'], edgecolor='white')
    axes[1].yaxis.set_major_formatter(mtick.PercentFormatter())
    axes[1].set_title("Win Rate: Baseline vs Strategy")
    axes[1].set_ylabel("Win Rate (%)")
    axes[1].axhline(50, color='red', linewidth=0.8, linestyle='--')

    fig.suptitle("Simulation: All Trades vs Fear-Only Sentiment Strategy", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(_save(save_dir, 'simulation.png'), dpi=150)
    plt.show()
