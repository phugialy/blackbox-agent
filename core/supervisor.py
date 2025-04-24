import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.scan import run_scheduled_scan
from core.triggers import detect_dns_health, detect_interface_status, detect_vpn_status
import time
import datetime

SCHEDULE_INTERVAL_HOURS = 8
EVENT_CHECK_INTERVAL_SECONDS = 60

def supervisor_loop():
    last_scheduled_scan_time = datetime.datetime.now() - datetime.timedelta(hours=SCHEDULE_INTERVAL_HOURS)

    while True:
        current_time = datetime.datetime.now()
        time_since_last_scan = (current_time - last_scheduled_scan_time).total_seconds() / 3600

        # Check for critical events
        if not detect_dns_health():
            print("DNS health check failed.")
            run_scheduled_scan(scan_type="event", incident_type="dns_fail")
        elif not detect_vpn_status():
            print("VPN status check failed.")
            run_scheduled_scan(scan_type="event", incident_type="vpn_drop")
        elif not detect_interface_status():
            print("Interface status check failed.")
            run_scheduled_scan(scan_type="event", incident_type="interface_down")

        # Check if it's time for a scheduled scan
        if time_since_last_scan >= SCHEDULE_INTERVAL_HOURS:
            print("Running scheduled scan.")
            run_scheduled_scan(scan_type="time")
            last_scheduled_scan_time = current_time

        # Sleep before the next event check
        time.sleep(EVENT_CHECK_INTERVAL_SECONDS)
        print("[Loop] Waiting for next check...")

if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    
    from core.supervisor import supervisor_loop
    supervisor_loop()