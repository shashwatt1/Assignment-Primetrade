# Crypto Market Sentiment vs Trader Performance Analysis

## Problem Statement
This project analyzes the relationship between trader performance (profitability, leverage behavior, and risk-taking) and market sentiment, driven primarily by the Fear and Greed index. By evaluating historical data against market psychology, we aim to uncover actionable insights into trader decision-making under varying market conditions.

## Objectives
- **Analyze profitability vs sentiment:** Determine how trading success fluctuates with extreme fear or greed.
- **Study leverage and risk behavior:** Understand how position sizing and leverage adjust to market sentiment.
- **Identify trading patterns:** Discover recurring behavioral trends among successful versus unsuccessful trades.
- **Derive actionable insights:** Provide data-driven recommendations for strategy optimization.

## Project Structure
```text
.
├── data/
│   ├── historical_data.csv
│   └── fear_greed_index.csv
├── notebooks/
│   └── analysis.ipynb
├── outputs/
│   └── plots/
├── src/
├── .gitignore
├── README.md
└── requirements.txt
```

## How to Run
1. Ensure you have Python installed.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Navigate to the `notebooks/` directory and start Jupyter:
   ```bash
   cd notebooks
   jupyter notebook analysis.ipynb
   ```
