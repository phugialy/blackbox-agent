import sqlite3
import os

def view_logs():
    db_path = os.path.join('db', 'lightdb.sqlite')

    # Check if the database file exists
    if not os.path.exists(db_path):
        print("Database file not found. Please ensure 'lightdb.sqlite' exists in the 'db' directory.")
        return

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Fetch the 5 most recent event-based scans
        print("Recent Event-Based Scans:")
        cursor.execute('''
            SELECT timestamp, incident_type FROM scans
            WHERE type = 'event'
            ORDER BY timestamp DESC
            LIMIT 5
        ''')
        scans = cursor.fetchall()
        for scan in scans:
            print(f"• {scan[0]} | {scan[1]}")
        
        print("\nUnresolved Incidents:")
        # Fetch all unresolved incidents
        cursor.execute('''
            SELECT * FROM incidents
            WHERE notified = 0
        ''')
        incidents = cursor.fetchall()
        for incident in incidents:
            print(incident)

        # Close the connection
        conn.close()

    except sqlite3.Error as e:
        print(f"An error occurred while accessing the database: {e}")

if __name__ == "__main__":
    view_logs()