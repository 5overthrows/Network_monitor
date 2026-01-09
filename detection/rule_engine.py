def detect_anomaly(features):
    """
    Returns a list of alerts based on hardcoded security rules.
    """
    alerts = []

    # Rule 1: Sensitive Port Monitoring
    critical_ports = [21, 22, 23, 3389, 445] # FTP, SSH, Telnet, RDP, SMB
    if features["dst_port"] in critical_ports:
        alerts.append(f"CRITICAL_PORT_ACCESS: {features['dst_port']}")

    # Rule 2: Potential Data Exfiltration (Large Packets)
    if features["packet_len"] > 1450:
        alerts.append("LARGE_PACKET_DETECTED")

    # Rule 3: Stealth Scanning (TCP Flags)
    # Checking for NULL scans or Xmas scans
    if features["flags"] in ["FPU", ""]:
        if features["protocol"] == "TCP":
            alerts.append("SUSPICIOUS_TCP_FLAGS")

    return alerts
