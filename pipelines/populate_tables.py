"""Run after create_tables.py to populate candlestick data, compute outcomes, and compute indicators."""


import tomllib

from binance.client import Client
from database.connection import get_engine
from database.populate_candles import populate_candles
from outcomes.return_sequence import populate_outcomes
from indicators.rsi import populate_indicator_rsi


def main():
    # Configuration for which tables are populated
    REBUILD_CANDLES = True
    REBUILD_OUTCOMES = True
    REBUILD_RSI_INDICATOR = True

    with open("config/config.toml", "rb") as config_file:
        config = tomllib.load(config_file)

    # Pull inputs from config
    pair = config["data"]["pair"]
    interval = config["data"]["interval"]
    start = config["data"]["start"]
    end = config["data"]["end"]

    # Custom thresholds ranging from -10% to +10%, excluding zero (meaningless as a 'candles_to_hit' threshold).
    # Long format of outcomes schema accommodates customisation of thresholds.
    thresholds = [i / 100 for i in range(-10, 11) if i != 0] 

    engine = get_engine()

    if REBUILD_CANDLES:
        client = Client(tld="com")
        populate_candles(engine, client, pair, interval, start, end)

    if REBUILD_OUTCOMES:
        for threshold in thresholds:
            populate_outcomes(engine, threshold)

    if REBUILD_RSI_INDICATOR:
        populate_indicator_rsi(engine)


if __name__ == "__main__":
    main()