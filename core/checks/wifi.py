import subprocess

def get_wifi_signal_strength():
    """
    Returns the current Wi-Fi signal strength as a string (e.g., '72%').
    Returns None if Wi-Fi is not connected or unavailable.
    """
    try:
        wifi_strength = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
        signal_lines = [line for line in wifi_strength.stdout.splitlines() if 'Signal' in line]
        if signal_lines:
            signal_strength = signal_lines[0].split(': ')[1].strip()
            print(f"[✓] Wi-Fi signal strength: {signal_strength}")
            return signal_strength
        else:
            print("[i] Wi-Fi not detected — likely using Ethernet.")
            return None
    except Exception as e:
        print(f"[!] Error checking Wi-Fi: {e}")
        return None