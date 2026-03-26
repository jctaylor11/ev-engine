import pandas as pd
from sqlalchemy import text

from database.utils import get_or_create_lookup
from ingestion.binance_ohlcv import fetch_binance_ohlcv_all



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

        # Insert candles df to postgres unless already entered
        conn.execute(text("""
            INSERT INTO candles (open_timestamp, open_price, high_price, low_price, close_price, volume, pair_id, interval_id)
            VALUES (:open_timestamp, :open_price, :high_price, :low_price, :close_price, :volume, :pair_id, :interval_id)
            ON CONFLICT (open_timestamp, pair_id, interval_id) DO NOTHING   -- These columns are the UNIQUE constraint
        """), candles_df.to_dict(orient='records'))


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