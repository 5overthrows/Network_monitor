import os
import csv
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live

from capture.packet_sniffer import capture_packets
from features.feature_extractor import extract_features
from detection.rule_engine import detect_anomaly

# --- LOGGING CONFIGURATION (Updated for unique files) ---
# 1. Create a unique timestamp for this specific run
session_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 2. Define the unique log file path
LOG_FILE = f"logs/traffic_log_{session_timestamp}.csv"

console = Console()

# Ensure logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# 3. Initialize the NEW CSV file with headers (This happens once per run)
with open(LOG_FILE, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Src_IP", "Dst_IP", "Proto", "Port", "Len", "Alerts"])
# -------------------------------------------------------

def process_packet(packet):
    # 1. Extract
    feat = extract_features(packet)
    if feat["src_ip"] == "N/A": return # Skip non-IP traffic for now

    # 2. Detect
    alerts = detect_anomaly(feat)
    alert_str = "|".join(alerts) if alerts else "None"

    # 3. Log to the specific session CSV
    with open(LOG_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%H:%M:%S"),
            feat["src_ip"],
            feat["dst_ip"],
            feat["protocol"],
            feat["dst_port"],
            feat["packet_len"],
            alert_str
        ])

    # 4. Detailed Live Output (Kept exactly as you had it)
    color = "red" if alerts else "green"
    status = "⚠️  ALERT" if alerts else "✅ OK"
    
    console.print(f"[{color}][{status}][/{color}] {feat['protocol']} | {feat['src_ip']} -> {feat['dst_ip']}:{feat['dst_port']} | Size: {feat['packet_len']} bytes | {alert_str}")

if __name__ == "__main__":
    console.print("[bold blue]Adaptive Network Monitor v1.0[/bold blue]", justify="center")
    # Show the user which file is being used for this session
    console.print(f"[bold white]Session Log:[/bold white] [cyan]{LOG_FILE}[/cyan]")
    console.print("[italic yellow]Press Ctrl+C to stop sniffing[/italic yellow]\n")
    
    # Start Capture (Change 'eth0' to your interface, e.g., 'wlan0' or 'lo')
    capture_packets(process_packet, iface="eth0")
