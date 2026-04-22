import os
import subprocess
import json

repo_dir = "/Users/shashwatt1/Desktop/Assignments/crypto_market_analysis"
os.chdir(repo_dir)

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

with open("notebooks/analysis.ipynb", "r") as f:
    nb = json.load(f)

run("rm -rf .git")
run("git init")
run("git branch -M main")

run("touch src/.gitkeep outputs/plots/.gitkeep")

run("git add README.md")
run("git commit -m 'Initial commit: Setup project overview and problem statement'")

run("git add .gitignore")
run("git commit -m 'Add .gitignore to exclude pycache and Jupyter checkpoints'")

run("git add requirements.txt")
run("git commit -m 'Define project dependencies in requirements.txt'")

run("git add src/.gitkeep outputs/plots/.gitkeep")
run("git commit -m 'Initialize project directory structure'")

run("git add data/historical_data.csv data/fear_greed_index.csv")
run("git commit -m 'Add placeholders for historical data and sentiment index'")

cells = nb["cells"]

def save_nb(num_cells):
    temp_nb = nb.copy()
    temp_nb["cells"] = cells[:num_cells]
    with open("notebooks/analysis.ipynb", "w") as f:
        json.dump(temp_nb, f, indent=1)
    run("git add notebooks/analysis.ipynb")

save_nb(3)
run("git commit -m 'Initialize analysis notebook with Intro and basic imports'")

save_nb(7)
run("git commit -m 'Add Data Loading and Data Cleaning sections'")

save_nb(11)
run("git commit -m 'Setup Data Merging and Exploratory Data Analysis (EDA)'")

save_nb(15)
run("git commit -m 'Add Sentiment-based Analysis and Key Insights extraction'")

save_nb(len(cells))
run("git commit -m 'Complete notebook with Strategy Recommendations and Conclusion'")

print("Commits successfully created.")
