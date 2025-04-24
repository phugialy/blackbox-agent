import os
import sqlite3

# Define the database path
db_path = os.path.join('db', 'lightdb.sqlite')

# Ensure the db directory exists
if not os.path.exists('db'):
    os.makedirs('db')

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the scans table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    type TEXT,
    ip TEXT,
    dns_status TEXT,
    latency_ms INTEGER,
    vpn_status TEXT,
    wifi_strength TEXT,
    uptime TEXT,
    incident_type TEXT,
    raw_json TEXT
)
''')

# Create the incidents table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_id INTEGER,
    event_type TEXT,
    severity TEXT CHECK(severity IN ('info', 'warning', 'critical')),
    resolved INTEGER CHECK(resolved IN (0, 1)),
    notified INTEGER CHECK(notified IN (0, 1)),
    FOREIGN KEY(scan_id) REFERENCES scans(id)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("[✓] LightDB initialized and ready.")