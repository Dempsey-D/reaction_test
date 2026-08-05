from scipy.stats import f_oneway
import statistics
import sqlite3
import os
import pandas as pd


DB_FILE = '/var/data/reactions.db'



df = pd.read_sql_query("SELECT * FROM reactions WHERE time_ms < 400", sqlite3.connect(DB_FILE))

f_stat, p_value = f_oneway(df[df['color']=='green']['time_ms'], df[df['color']=='blue']['time_ms'], df[df['color']=='red']['time_ms'], df[df['color']=='yellow']['time_ms'])

print("F-statistic:", f_stat)
print("p-value:", p_value)

for color in df['color'].unique():
    data = df[df['color'] == color]['time_ms']
    print(f"\nStatistics for {color}:")
    
    # Calculate individual metrics
    summary_stats = {
        "Length (Count)": len(data),
        "Min": min(data),
        "Max": max(data),
        "Mean (Average)": statistics.mean(data),
        "Median": statistics.median(data),
        "Mode": statistics.mode(data),
        "Standard Deviation": statistics.stdev(data),
        "Variance": statistics.variance(data)
    }

    for stat, value in summary_stats.items():
        print(f"{stat}: {value:.2f}" if isinstance(value, float) else f"{stat}: {value}")

