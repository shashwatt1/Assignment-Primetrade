import matplotlib.pyplot as plt
import seaborn as sns

def set_style():
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)

def plot_pnl_vs_sentiment(df):
    set_style()
    if 'sentiment_category' not in df.columns or 'profit' not in df.columns:
        return
    plt.figure()
    sns.barplot(data=df, x='sentiment_category', y='profit', estimator=sum, errorbar=None, palette="coolwarm")
    plt.title("Total PnL vs Sentiment")
    plt.ylabel("Total Profit")
    plt.xlabel("Sentiment Category")
    plt.tight_layout()
    plt.savefig('outputs/plots/pnl_vs_sentiment.png')
    plt.close()

def plot_win_rate_vs_sentiment(df):
    set_style()
    if 'sentiment_category' not in df.columns or 'win' not in df.columns:
        return
    plt.figure()
    sns.barplot(data=df, x='sentiment_category', y='win', errorbar=None, palette="viridis")
    plt.title("Win Rate vs Sentiment")
    plt.ylabel("Win Rate")
    plt.xlabel("Sentiment Category")
    plt.tight_layout()
    plt.savefig('outputs/plots/win_rate_vs_sentiment.png')
    plt.close()

def plot_leverage_vs_sentiment(df):
    set_style()
    if 'sentiment_category' not in df.columns or 'leverage' not in df.columns:
        return
    plt.figure()
    sns.boxplot(data=df, x='sentiment_category', y='leverage', palette="mako")
    plt.title("Leverage vs Sentiment")
    plt.ylabel("Leverage")
    plt.xlabel("Sentiment Category")
    plt.tight_layout()
    plt.savefig('outputs/plots/leverage_vs_sentiment.png')
    plt.close()
