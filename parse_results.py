# coding: utf-8

# Experimental Results
# This script parses experimental logs to obtain performance metrics.

# Import LogAnalyzer objects
from tools.log_analyzer import *
import matplotlib.pyplot as plt
import os

# IMPORTANT: Specify directory and log filenames here
log_dir_path = "logs/DARM/sim/"
vehicle_log_file = "vehicle.log"
customer_log_file = "customer.log"
score_log_file = "score.log"
summary_log_file = "summary.log"

# Invoke LogAnalyzer object
l = LogAnalyzer()

def load_log_or_warn(loader_func, log_path):
    """Load log safely, handle exceptions, and print warnings if necessary."""
    try:
        df = loader_func(log_path)
        if df.empty:
            print(f"Warning: Log at '{log_path}' is empty.")
        return df
    except Exception as e:
        print(f"Error loading log from '{log_path}': {e}")
        return None

# Check if log files exist before attempting to load
log_files = [
    os.path.join(log_dir_path, vehicle_log_file),
    os.path.join(log_dir_path, customer_log_file),
    os.path.join(log_dir_path, score_log_file),
    os.path.join(log_dir_path, summary_log_file)
]

for path in log_files:
    print(f"Checking log file: {path} - Exists: {os.path.exists(path)}")

# Load dataframes safely with error handling
summary_df = load_log_or_warn(l.load_summary_log, log_dir_path)
vehicle_df = load_log_or_warn(l.load_vehicle_log, log_dir_path)
customer_df = load_log_or_warn(l.load_customer_log, log_dir_path)
score_df = load_log_or_warn(l.load_score_log, log_dir_path)

# Print summaries if data is loaded successfully
if summary_df is not None:
    print(summary_df.describe())
if vehicle_df is not None:
    print(vehicle_df.describe())
if customer_df is not None:
    print(customer_df["waiting_time"].describe())
if score_df is not None:
    print(score_df.describe())

# Ensure metrics plot directory exists
os.makedirs("DARM", exist_ok=True)

# Function to plot metrics safely
def safe_histogram(data, label, plt):
    """Plot histogram safely, skip if data is missing or invalid."""
    try:
        plt.hist(data.dropna(), bins=20, alpha=0.5, label=label)
    except ValueError as e:
        print(f"Error plotting '{label}': {e}")

# Plot metrics if the score log contains data
if score_df is not None and not score_df.empty:
    metrics = ["Profit", "Cruising Time", "Occupancy Rate", "Waiting Time", "Travel Distance"]

    plt.figure(figsize=(10, 6))
    for metric in metrics:
        if metric in score_df.columns:
            safe_histogram(score_df[metric], metric, plt)
        else:
            print(f"Metric '{metric}' not found in score log.")

    plt.legend()
    plt.savefig("logs/DARM/Metrics.pdf", bbox_inches='tight')
    plt.show()
else:
    print("Score log is empty, skipping plot generation.")

# Display the first few rows of the score log
if score_df is not None:
    print(score_df.head())
