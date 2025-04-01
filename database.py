
import sqlite3
import csv

class Database:
    def __init__(self, db_name="database.db"):
        """Initialize the database connection and create the table if it doesn't exist."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()
        self.add_codes_from_csv("codes.csv")

    def _create_table(self):
        """Create a table with columns id and code if it doesn't already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL
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

    def close(self):
        """Close the database connection."""
        self.connection.close()

# Example usage:
# db = Database()
# db.add_codes_from_csv("codes.csv")  # Overwrites all existing codes with new ones from the CSV
# db.close()