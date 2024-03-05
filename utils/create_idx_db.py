# create_idx.py

import os

from sqlalchemy import create_engine, text

base_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(base_dir, "../database", "presc_drugs.db")


engine = create_engine(f"sqlite:///{database_path}")

with engine.connect() as conn:
    conn.execute(text("CREATE INDEX idx_med ON medic (idx_column)"))

if __name__ == "__main__":
    print("OK - idx - created!")
