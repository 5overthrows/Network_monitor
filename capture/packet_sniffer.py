from scapy.all import sniff
import sys

def capture_packets(callback, iface="eth0"):
    """
    Captures live traffic from the specified interface.
    iface: 'eth0' for wired, 'wlan0' for wifi, 'lo' for loopback
    """
    print(f"[*] Starting live capture on {iface}...")
    try:
        # store=0 ensures we don't eat up RAM by keeping packets in memory
        sniff(iface=iface, prn=callback, store=0)
    except PermissionError:
        print("[!] Error: You must run this script with sudo (root privileges).")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)
