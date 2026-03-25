from ingestion.binance_ohlcv import fetch_binance_ohlcv_all
import pandas as pd
from sqlalchemy import text

def populate_candles(engine, client, pair, interval, start, end):
    """Populate candles table with candlestick data from Binance"""
    # Fetch and clean data from Binance
    candles_df = fetch_binance_ohlcv_all(client, pair, interval, start, end)
    candles_df = clean_candles(candles_df)
    candles_df = format_candles(candles_df)

    # Map df columns to sql column names 
    candles_df.reset_index(inplace=True)
    candles_df.rename(columns={
        "date": "open_timestamp",
        "open": "open_price",
        "high": "high_price",
        "low": "low_price",
        "close": "close_price"
        }, inplace=True)

    with engine.begin() as conn: 
        # Get or create interval id and pair id in lookup table
        pair_id = get_or_create_lookup(conn, "pair_lookup", "coin_pair", pair)
        interval_id = get_or_create_lookup(conn, "interval_lookup", "interval_name", interval)

        # Add pair id and interval id foreign keys to candles df
        candles_df["pair_id"] = pair_id
        candles_df["interval_id"] = interval_id

        # Insert candles df to postgres
        candles_df.to_sql('candles', conn, if_exists='append', index=False)


def get_or_create_lookup(conn, table, column, value):
    """Return the id for the value, or create a new id if it doesn't exist"""
    row_id = conn.execute(text(f"SELECT id FROM {table} WHERE {column} = :symbol;"), {"symbol": value}).scalar()
    if row_id is None: 
        row_id = conn.execute(text(f"INSERT INTO {table} ({column}) VALUES (:symbol) RETURNING id"), {"symbol": value}).scalar()
    
    return row_id


def clean_candles(df):
    # Remove any duplicates
    duplicates = df.index.duplicated()
    df = df[~duplicates]
    print(f"Duplicates removed: {duplicates.sum()}. (Should be 0 - non-zero suggests logic error)")

    return df


def format_candles(df):
    df.columns = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "num_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]

    df["date"] = pd.to_datetime(df["open_time"], unit='ms')
    df.set_index("date", inplace = True)

    df = df[["open", "high", "low", "close", "volume"]].copy()

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors = "coerce")

    return df