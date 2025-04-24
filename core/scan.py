import os
import subprocess
import socket
import time
import datetime
import ctypes
import json
import sqlite3
from core.checks.wifi import get_wifi_signal_strength

def run_scheduled_scan(scan_type="time", incident_type=None):
    data = {}

    # Collect Timestamp
    try:
        data['timestamp'] = datetime.datetime.now().isoformat()
    except Exception as e:
        print(f"Error collecting timestamp: {e}")

    # Collect IP Address
    try:
        data['ip'] = socket.gethostbyname(socket.gethostname())
    except Exception as e:
        print(f"Error collecting IP address: {e}")

    # Collect DNS Status
    try:
        dns_status = subprocess.run(['nslookup', 'google.com'], capture_output=True, text=True)
        data['dns_status'] = 'success' if 'Address' in dns_status.stdout else 'failure'
    except Exception as e:
        print(f"Error collecting DNS status: {e}")

    # Collect Latency
    try:
        latency = subprocess.run(['ping', '-n', '1', '8.8.8.8'], capture_output=True, text=True)
        data['latency_ms'] = int(latency.stdout.split('Average = ')[-1].split('ms')[0])
    except Exception as e:
        print(f"Error collecting latency: {e}")

    # Collect VPN Status
    try:
        vpn_status = subprocess.run(['ipconfig'], capture_output=True, text=True)
        data['vpn_status'] = 'active' if 'VPN' in vpn_status.stdout else 'inactive'
    except Exception as e:
        print(f"Error collecting VPN status: {e}")

    # Collect Wi-Fi Strength
    wifi_strength = get_wifi_signal_strength()
    data['wifi_strength'] = wifi_strength

    # Collect Uptime
    try:
        uptime = subprocess.run(['net', 'stats', 'workstation'], capture_output=True, text=True)
        data['uptime'] = uptime.stdout.split('Statistics since ')[-1].strip()
    except Exception as e:
        print(f"Error collecting uptime: {e}")

    # Set Type and Incident Type
    data['type'] = scan_type
    data['incident_type'] = incident_type

    # Convert data to JSON
    try:
        data['raw_json'] = json.dumps(data)
    except Exception as e:
        print(f"Error converting data to JSON: {e}")

    # Connect to SQLite database and insert data
    try:
        db_path = os.path.join('db', 'lightdb.sqlite')
        if not os.path.exists('db'):
            os.makedirs('db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scans (timestamp, type, ip, dns_status, latency_ms, vpn_status, wifi_strength, uptime, incident_type, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['timestamp'], data['type'], data['ip'], data['dns_status'], data['latency_ms'], data['vpn_status'], data['wifi_strength'], data['uptime'], data['incident_type'], data['raw_json']))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error inserting data into database: {e}")

    print("[✓] Scheduled scan complete and inserted into LightDB.")

if __name__ == "__main__":
    run_scheduled_scan()