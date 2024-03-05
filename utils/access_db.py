# access_db.py

import os

from pandas import DataFrame, read_sql  # type: ignore[import]
from sqlalchemy import create_engine
from tabulate import tabulate

base_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(base_dir, "../database", "presc_drugs.db")

db_engine = create_engine(f"sqlite:///{database_path}")

result: DataFrame = read_sql("SELECT * FROM medic", db_engine)


print(tabulate(result, headers="keys", tablefmt="psql"))  # type: ignore

# Save as markdown
# result.to_html(("access.md"))  # type: ignore


if __name__ == "__main__":
    print("OK - Access OK!")
