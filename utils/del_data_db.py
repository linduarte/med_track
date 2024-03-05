# delete_data_db.py

import os

from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from tabulate import tabulate

base_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(base_dir, "../database", "presc_drugs.db")


# def delete_data(database_path):
engine = create_engine(f"sqlite:///{database_path}")

# table name
MEDIC = "medic"

# Create a metadata object
metadata = MetaData()

# Define the columns of the table
medic = Table(
    "medic",
    metadata,
    Column("idx_column", Integer),
    Column("last_updated", String),
    Column("medicine", String, primary_key=True),
    Column("stock_medicine_box", Integer),
    Column("drug_dosage", Integer),
    Column("prescription_valid_until", String),
    Column("drug_container", Integer),
)

# Establish a connection
with engine.begin() as conn:
    stmt = medic.delete()
    conn.execute(stmt)

    # Check if the deletion was successful
    m = medic.select()
    result = conn.execute(m).fetchall()
    print(tabulate(result, headers="keys", tablefmt="psql"))

if __name__ == "__main__":
    print("OK - Deleted")
