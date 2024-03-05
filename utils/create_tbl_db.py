# create_tbl_db.py

import os

from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

base_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(base_dir, "../database", "presc_drugs.db")


# table name
MEDIC = "medic"

# Create the database engine
engine = create_engine(f"sqlite:///{database_path}")

# Create a metadata object
metadata = MetaData()

# Define the columns of the table
medic = Table(
    MEDIC,
    metadata,
    Column("idx_column", Integer),
    Column("last_updated", String),
    Column("medicine", String, primary_key=True),
    Column("stock_medicine_box", Integer),
    Column("drug_dosage", Integer),
    Column("prescription_valid_until", String),
    Column("drug_container", Integer),
)

metadata.create_all(engine)
print("these are columns in our table %s" % (medic.columns.keys()))

if __name__ == "__main__":
    print("OK - tbl created!")
