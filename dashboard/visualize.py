import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def get_latest_log():
    # Find all csv files in the logs folder
    list_of_files = glob.glob('logs/traffic_log*.csv')
    if not list_of_files:
        return None
    # Return the one with the latest creation time
    return max(list_of_files, key=os.path.getctime)

def show_stats():
    latest_file = get_latest_log()
    if not latest_file:
        print("No log files found in logs/ directory.")
        return

    print(f"Visualizing latest session: {latest_file}")
    df = pd.read_csv(latest_file)
    
    if df.empty:
        print("Log file is empty. Capture some traffic first!")
        return

    plt.figure(figsize=(12, 5))

    # Plot 1: Protocol Count
    plt.subplot(1, 2, 1)
    df['Proto'].value_counts().plot(kind='bar', color='skyblue')
    plt.title("Protocol Distribution")
    plt.ylabel("Packet Count")

    # Plot 2: Traffic Volume (Byte count over time)
    plt.subplot(1, 2, 2)
    plt.plot(df.index, df['Len'], label='Packet Size', color='orange')
    plt.title("Packet Size over Time")
    plt.xlabel("Packet Sequence")
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    show_stats()
