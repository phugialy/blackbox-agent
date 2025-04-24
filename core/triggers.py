import os
import subprocess
import socket
import time
from core.scan import run_scheduled_scan

def detect_vpn_status() -> bool:
    try:
        vpn_status = subprocess.run(['ipconfig'], capture_output=True, text=True)
        return 'VPN' in vpn_status.stdout
    except Exception as e:
        print(f"Error detecting VPN status: {e}")
        return False

def detect_dns_health() -> bool:
    try:
        socket.gethostbyname('google.com')
        return True
    except socket.error:
        return False

def detect_interface_status() -> bool:
    try:
        interface_status = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
        return 'Disconnected' not in interface_status.stdout
    except Exception as e:
        print(f"Error detecting interface status: {e}")
        return False

def listen_for_events():
    while True:
        vpn_active = detect_vpn_status()
        dns_healthy = detect_dns_health()
        interfaces_up = detect_interface_status()

        if not vpn_active:
            print("VPN connection dropped.")
            run_scheduled_scan(scan_type="event", incident_type="vpn_drop")
        if not dns_healthy:
            print("DNS resolution failed.")
            run_scheduled_scan(scan_type="event", incident_type="dns_fail")
        if not interfaces_up:
            print("One or more interfaces are down.")
            run_scheduled_scan(scan_type="event", incident_type="interface_down")

        time.sleep(60)

if __name__ == "__main__":
    listen_for_events()