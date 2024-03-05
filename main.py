# main.py

import os

from prescription_tracker import PrescriptionTracker

base_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(base_dir, "database", "presc_drugs.db")

tracker = PrescriptionTracker(database_path)

# Update dosages based on user input
tracker.update_drug_container()

# Refill drug containers based on user input
tracker.refill_drug_container()

# Access the database and print the data
tracker.access_database()


if __name__ == "__main__":
    print("OK - Success!")
