# add_data_db.py

import os

from sqlalchemy import Table  # noqa: E501
from sqlalchemy import Column, Integer, MetaData, String, create_engine, insert

base_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(base_dir, "../database", "presc_drugs.db")


engine = create_engine(f"sqlite:///{database_path}")


# table name
MEDIC = "medic"

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

# Define the data to be inserted
data = [
    {
        "idx_column": 1,
        "last_updated": "23/05/2023",
        "medicine": "Losartana",
        "stock_medicine_box": 30,
        "drug_dosage": 2,
        "prescription_valid_until": "23/06/2023",
        "drug_container": 4,
    },
    {
        "idx_column": 2,
        "last_updated": "23/05/2023",
        "medicine": "AAS",
        "stock_medicine_box": 30,
        "drug_dosage": 1,
        "prescription_valid_until": "23/06/2023",
        "drug_container": 2,
    },
    {
        "idx_column": 3,
        "last_updated": "23/05/2023",
        "medicine": "Anlodipino",
        "stock_medicine_box": 30,
        "drug_dosage": 1,
        "prescription_valid_until": "23/06/2023",
        "drug_container": 2,
    },
    {
        "idx_column": 4,
        "last_updated": "23/05/2023",
        "medicine": "Hidroclorotiazida",
        "stock_medicine_box": 30,
        "drug_dosage": 1,
        "prescription_valid_until": "23/06/2023",
        "drug_container": 2,
    },
    {
        "idx_column": 5,
        "last_updated": "23/05/2023",
        "medicine": "Atorvastatina",
        "stock_medicine_box": 30,
        "drug_dosage": 1,
        "prescription_valid_until": "23/06/2023",
        "drug_container": 2,
    },
]

# Establish a connection
with engine.connect() as conn:
    conn.execute(insert(medic).values(data))

    # Commit changes
    conn.commit()

if __name__ == "__main__":
    print("OK - Data added")
