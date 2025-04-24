import sqlite3
import json
import requests
import smtplib
from email.mime.text import MIMEText
import datetime

def send_email_alert(subject: str, body: str):
    # SMTP configuration
    smtp_server = "smtp.example.com"
    smtp_port = 587
    sender_email = "sender@example.com"
    recipient_email = "recipient@example.com"
    password = "your_password"

    # Create the email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email alert sent: {subject}")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

def send_teams_alert(message: str):
    # Microsoft Teams webhook URL
    webhook_url = "https://outlook.office.com/webhook/your_webhook_url"

    # Send the POST request
    try:
        response = requests.post(webhook_url, json={"text": message})
        if response.status_code == 200:
            print("Teams alert sent successfully.")
        else:
            print(f"Failed to send Teams alert: {response.status_code}")
    except Exception as e:
        print(f"Error sending Teams alert: {e}")

def notify_if_critical(scan_data: dict):
    critical_incidents = ["vpn_drop", "dns_fail", "interface_down"]
    incident_type = scan_data.get("incident_type")

    if incident_type in critical_incidents:
        subject = f"Critical Alert: {incident_type}"
        body = f"A critical incident has been detected: {incident_type}\nDetails: {json.dumps(scan_data, indent=2)}"
        send_email_alert(subject, body)
        send_teams_alert(body)

        # Update the incidents table
        try:
            conn = sqlite3.connect('db/lightdb.sqlite')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE incidents
                SET notified = 1
                WHERE incident_type = ? AND notified = 0
            ''', (incident_type,))
            conn.commit()
            conn.close()
            print(f"Incident {incident_type} marked as notified.")
        except Exception as e:
            print(f"Error updating incidents table: {e}")

if __name__ == "__main__":
    # Example scan data for testing
    scan_data_example = {
        "incident_type": "vpn_drop",
        "timestamp": datetime.datetime.now().isoformat(),
        "details": "VPN connection lost"
    }
    notify_if_critical(scan_data_example)