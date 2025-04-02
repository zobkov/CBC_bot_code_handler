import sqlite3
import csv
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name="database.db"):
        """Initialize the database connection and create the tables if they don't exist."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()
        self._create_timed_table()
        self._create_user_validations_table()
        #self.add_codes_from_csv("codes.csv")

    def _create_table(self):
        """Create a table with columns id and code if it doesn't already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL
            )
        """)
        self.connection.commit()

    def _create_timed_table(self):
        """Create a table for timed entries with columns id, code, and datetime."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS timed_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                datetime TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def _create_user_validations_table(self):
        """Create a table to track which users have validated which codes."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_validations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                UNIQUE(user_id, code)
            )
        """)
        self.connection.commit()

    def check_code_exists(self, code):
        """Check if a code exists in the table."""
        self.cursor.execute("SELECT 1 FROM entries WHERE code = ?", (code,))
        return self.cursor.fetchone() is not None

    def delete_code(self, code):
        """Delete a code from the table."""
        self.cursor.execute("DELETE FROM entries WHERE code = ?", (code,))
        self.connection.commit()

    def add_codes_from_csv(self, csv_file_path):
        """Overwrite all existing codes and add new ones from a CSV file."""
        # Clear the table
        self.cursor.execute("DELETE FROM entries")
        self.connection.commit()

        # Read codes from the CSV file and insert them into the table
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Ensure the row is not empty
                    code = row[0].strip()  # Assuming the code is in the first column
                    self.cursor.execute("INSERT INTO entries (code) VALUES (?)", (code,))
        self.connection.commit()

    def add_timed_code(self, code, start_time):
        """Add a code with a start time to the timed_entries table."""
        self.cursor.execute("INSERT INTO timed_entries (code, datetime) VALUES (?, ?)", (code, start_time))
        self.connection.commit()

    def is_code_valid(self, code, user_id):
        """Check if a code is valid for a specific user within a 15-minute window."""
        # Check if the code exists and is within the validity window
        self.cursor.execute("SELECT datetime FROM timed_entries WHERE code = ?", (code,))
        result = self.cursor.fetchone()
        if result:
            start_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            if current_time <= start_time + timedelta(minutes=15):
                # Check if the user has already validated this code
                self.cursor.execute("SELECT 1 FROM user_validations WHERE user_id = ? AND code = ?", (user_id, code))
                if self.cursor.fetchone() is None:
                    # The code is valid and the user has not validated it yet
                    self.cursor.execute("INSERT INTO user_validations (user_id, code) VALUES (?, ?)", (user_id, code))
                    self.connection.commit()
                    return True
        return False

    def add_timed_codes_from_csv(self, csv_file_path):
        """Overwrite all existing timed codes and add new ones from a CSV file."""
        # Clear the timed_entries table
        self.cursor.execute("DELETE FROM timed_entries")
        self.connection.commit()

        # Read timed codes from the CSV file and insert them into the table
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 2:  # Ensure the row has enough columns
                    code = row[0].strip()
                    start_time = row[1].strip()
                    self.cursor.execute("INSERT INTO timed_entries (code, datetime) VALUES (?, ?)", (code, start_time))
        self.connection.commit()

    def close(self):
        """Close the database connection."""
        self.connection.close()

# Example usage:
# db = Database()
# db.add_timed_code("example_code", "2025-04-02 12:00:00")  # Add a timed code
# print(db.is_code_valid("example_code", 1))  # Check if the code is valid for user_id 1
# db.add_timed_codes_from_csv("timed_codes.csv")  # Overwrite timed codes from a CSV file
# db.close()