# prescription_tracker.py

import datetime

import pandas as pd
from sqlalchemy import Table  # noqa: E501
from sqlalchemy import Column, Integer, MetaData, String, create_engine, text
from tabulate import tabulate

# Table name:
MEDIC = "medic"


class PrescriptionTracker:
    def __init__(self, database_path):  # type: ignore[assignment]
        self.database_path = database_path
        self.engine = create_engine(f"sqlite:///{database_path}")
        self.metadata = MetaData()
        self.medic_table = Table(
            "medic",
            self.metadata,
            Column("idx_column", Integer),
            Column("last_updated", String),
            Column("medicine", String, primary_key=True),
            Column("stock_medicine_box", Integer),
            Column("drug_dosage", Integer),
            Column("prescription_valid_until", String),
            Column("drug_container", Integer),
        )

    def update_drug_container(self):
        with self.engine.connect() as conn:
            rows = conn.execute(text("SELECT * FROM medic"))

            current_date = datetime.datetime.now().strftime("%d/%m/%Y")

            for row in rows:
                idx_column = row[0]
                medicine_name = row[2]
                dosage = row[4]
                container = row[6]
                last_updated = datetime.datetime.strptime(row[1], "%d/%m/%Y")

                # Check prescription validity
                prescription_valid_until = datetime.datetime.strptime(
                    row[5], "%d/%m/%Y"
                )
                days_until_expiry = (
                    prescription_valid_until - datetime.datetime.now()
                ).days
                if days_until_expiry <= 30:
                    print(
                        f"It's time to renew the prescription for {medicine_name}."  # noqa: E501
                    )  # noqa: E501

                # Check last updated date
                days_since_update = (datetime.datetime.now() - last_updated).days  # noqa: E501
                if days_since_update > 0:
                    container -= dosage * days_since_update
                    conn.execute(
                        text(
                            "UPDATE medic SET drug_container = :container, last_updated = :current_date WHERE idx_column = :idx_column"  # noqa: E501
                        ).params(
                            container=container,
                            current_date=current_date,
                            idx_column=idx_column,
                        )
                    )
                    print(
                        f"Updated drug container for {medicine_name}. Current container value: {container}."  # noqa: E501
                    )

            conn.commit()

    def refill_drug_container(self):
        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT medicine, drug_container, stock_medicine_box FROM medic WHERE drug_container <= 2"  # noqa: E501
                )
            )

            rows = result.fetchall()

            if len(rows) == 0:
                print("No drugs need to be refilled.")
            else:
                print("The following drug containers need to be refilled:")
                for row in rows:
                    medicine = row[0]
                    stock_medicine_box = row[2]

                    if stock_medicine_box > 0:
                        refill_qty = stock_medicine_box
                        new_stock = 0
                    else:
                        refill_qty = 2
                        new_stock = (
                            0 if stock_medicine_box == 0 else stock_medicine_box  # noqa: E501
                        )  # noqa: E501

                    new_container = refill_qty
                    conn.execute(
                        text(
                            "UPDATE medic SET stock_medicine_box=:new_stock, drug_container=:new_container WHERE medicine=:medicine"  # noqa: E501
                        ).params(
                            new_stock=new_stock,
                            new_container=new_container,
                            medicine=medicine,
                        )
                    )
                    print(
                        f"Refilled {medicine} container with {refill_qty} units."  # noqa: E501
                    )  # noqa: E501

            conn.commit()

    def access_database(self):
        result = pd.read_sql("SELECT * FROM medic", self.engine)  # type: ignore[assignment] # noqa: E501
        print(tabulate(result, headers="keys", tablefmt="psql"))  # type: ignore[assignment] # noqa: E501
