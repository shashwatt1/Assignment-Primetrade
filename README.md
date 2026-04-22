# Crypto Market Sentiment vs Trader Performance Analysis

## Problem Statement
This project analyzes the relationship between trader performance (profitability, leverage behavior, and risk-taking) and market sentiment, driven primarily by the Fear and Greed index. We seek to uncover behavioral patterns that distinguish successful trades from unsuccessful ones under varying market conditions.

## Approach
This project uses a hybrid approach to maintain clean engineering practices while delivering clear insights:
- **Modular Python Code (`src/`)**: Handles data loading, preprocessing, merging, analysis, and visualization in a clean, maintainable way.
- **Jupyter Notebook (`notebooks/final_analysis.ipynb`)**: Serves as the presentation layer, pulling from the modular backend to narrate insights, segmentation, and strategy.

## Key Objectives
- Analyze profitability vs sentiment.
- Study leverage and risk behavior under Fear vs Greed.
- Segment top traders vs average traders.
- Formulate a sentiment-based trading strategy.

## Project Structure
```text
.
├── data/
│   ├── historical_data.csv
│   └── fear_greed_index.csv
├── src/
│   ├── load_data.py
│   ├── preprocess.py
│   ├── merge.py
│   ├── analysis.py
│   └── visualize.py
├── notebooks/
│   └── final_analysis.ipynb
├── outputs/
│   └── plots/
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run Project
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the full data pipeline** (ETL & Visualizations):
   ```bash
   python main.py
   ```
3. **Explore the Insights**:
   Open the Jupyter Notebook to read the final presentation:
   ```bash
   jupyter notebook notebooks/final_analysis.ipynb
   ```
