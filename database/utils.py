from sqlalchemy import text


def get_or_create_lookup(conn, table, column, value):
    """Return the id for the value, or create a new entry if it doesn't exist.

    Args:
        conn: SQLAlchemy connection to Postgres database.
        table: Name of the lookup table.
        column: Name of the column to search for the value.
        value: The value to find or insert.

    Returns:
        int: ID for the queried value in the lookup table.
    """
    row_id = conn.execute(text(f"SELECT id FROM {table} WHERE {column} = :symbol;"), {"symbol": value}).scalar()
    if row_id is None:
        row_id = conn.execute(text(f"INSERT INTO {table} ({column}) VALUES (:symbol) RETURNING id"), {"symbol": value}).scalar()

    return row_id
