import os

import duckdb

DUCKDB_PATH = os.getenv("DUCKDB_PATH", "./data/analytics.duckdb")


def get_duckdb_connection() -> duckdb.DuckDBPyConnection:
    # TODO: Introduce a managed connection pool strategy if needed.
    return duckdb.connect(DUCKDB_PATH)
