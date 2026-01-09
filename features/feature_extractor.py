from scapy.layers.inet import IP, TCP, UDP, ICMP

def extract_features(packet):
    features = {
        "timestamp": packet.time,
        "src_ip": "N/A",
        "dst_ip": "N/A",
        "protocol": "OTHER",
        "src_port": 0,
        "dst_port": 0,
        "packet_len": len(packet),
        "flags": "N/A"
    }

    if IP in packet:
        features["src_ip"] = packet[IP].src
        features["dst_ip"] = packet[IP].dst
        
        # Determine Protocol
        proto_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        features["protocol"] = proto_map.get(packet[IP].proto, "OTHER")

        if TCP in packet:
            features["src_port"] = packet[TCP].sport
            features["dst_port"] = packet[TCP].dport
            features["flags"] = str(packet[TCP].flags)
        elif UDP in packet:
            features["src_port"] = packet[UDP].sport
            features["dst_port"] = packet[UDP].dport

    return features
