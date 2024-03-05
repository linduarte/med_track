import os

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    select,
    update,
)
from tabulate import tabulate

# Define the path to the database
base_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(base_dir, "../database", "presc_drugs.db")

# Create the database engine
engine = create_engine(f"sqlite:///{database_path}")

# Create a metadata object
metadata = MetaData()

MEDIC = "medic"

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


# Define the medic table
medic = Table("medic", metadata, autoload=True, autoload_with=engine)

# Establish a connection
with engine.begin() as conn:
    # Select all medicines with empty stock
    empty_stock_query = select(medic).where(medic.c.stock_medicine_box == 0)
    empty_stock_result = conn.execute(empty_stock_query).fetchall()
    print(tabulate(empty_stock_result, headers="keys", tablefmt="psql"))

    # Check if there are medicines with empty stock
    if empty_stock_result:
        print("Refilling stock for the following medicines:")
        print(tabulate(empty_stock_result, headers="keys", tablefmt="psql"))
        print()

        # Update the stock_medicine_box and drug_container columns for empty stock medicines # noqa: E501
        refill_query = (
            update(medic)
            .where(medic.c.stock_medicine_box == 0)
            .values(stock_medicine_box=30, drug_container=30)
        )
        conn.execute(refill_query)

        print("Stock refilled successfully!")
    else:
        print("No medicines with empty stock found.")
