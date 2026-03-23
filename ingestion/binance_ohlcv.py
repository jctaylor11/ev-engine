import math
import time

from binance.client import Client           
import pandas as pd

BATCH_LIMIT = 1000
RATE_LIMIT = 0.3


def fetch_binance_ohlcv_all(client, symbol, interval, start, end):
    """Return a dataframe of all candlestick data for the specified arguments"""

    latest_timestamp = None

    # If start is earlier than earliest start, start = earliest start
    earliest_timestamp_unix = client._get_earliest_valid_timestamp(symbol, interval)
    earliest_timestamp = pd.to_datetime(earliest_timestamp_unix, unit='ms')
    if pd.to_datetime(start) < earliest_timestamp:
        start = earliest_timestamp.strftime("%Y-%m-%d")

    # Initialise array to store each batch requested from Binance 
    data_batches = []
    batch_count = 0
    total_batches = max(math.ceil((pd.Timestamp(end) - pd.Timestamp(start)) / pd.to_timedelta(interval) / BATCH_LIMIT), 1)

    # Requests the full data batch by batch to adhere to limits
    while True: 
        # Pulls a single batch from the current time cursor (start), up to the limit or 'end' (whichever is first)
        data_batch = _fetch_binance_ohlcv_batch(client, symbol, interval, start, end)   # data_batch latest timestamp <= end

        # data_batch.empty catches the edge of exact-1000 final batch, checking latest_timestamp safeguards against no-progress loops
        if data_batch.empty or latest_timestamp == data_batch.index.max():        
            break       # All requested data pulled
           
        print(f"Pulled batch: {start} - {batch_count + 1}/{total_batches}")    # + 1 due to zero-index
        data_batches.append(data_batch)

        # If batch limit is not hit, it implies all data has been fetched without needing to request empty batch to check
        if len(data_batch) < BATCH_LIMIT:
            break

        # Advances time cursor to avoid duplicates
        latest_timestamp = data_batch.index.max()
        start = str(latest_timestamp + pd.Timedelta(interval))  
        batch_count += 1    
        
    # If any data was fetched it concats, else it returns an empty data frame
    if data_batches:
        all_fetched_data = pd.concat(data_batches)
    else:
        all_fetched_data = pd.DataFrame()

    return all_fetched_data


def _fetch_binance_ohlcv_batch(client, symbol, interval, start, end=None):
    """Fetch one batch of historical OHLCV data from Binance, up to maximum request size (1000 bars)"""
    time.sleep(RATE_LIMIT)     # To ensure Binance's API rate limits are not violated

    bars = client.get_historical_klines(symbol, interval, start, end, limit=BATCH_LIMIT)

    # Returns empty dataframe if it didn't get a response
    if not bars:
        return pd.DataFrame()

    # Format bars from a list of lists to a dataframe
    df = pd.DataFrame(bars)

    # Basic formatting of raw data, including column names                 
    df = _parse_raw_ohlcv_response(df)

    return df


def _parse_raw_ohlcv_response(df):
    """Parse raw Binance kline response into datetime-indexed DataFrame with column names"""
    df.columns = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "num_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]

    df["date"] = pd.to_datetime(df["open_time"], unit='ms')
    df.set_index("date", inplace = True)

    return df


def main():
    client = Client(tld="com")
    df = fetch_binance_ohlcv_all(client, "BTCUSDT", "1d", "2020-01-01", "2024-01-01")
    print(df)

if __name__ == "__main__":
    main()