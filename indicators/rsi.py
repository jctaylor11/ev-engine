from sqlalchemy import text
from database.utils import get_or_create_lookup


def populate_indicator_rsi(engine, rsi_period=14):
    """Compute RSI for all candles and insert into indicator_values table.
    
    Args:
        engine: SQLAlchemy engine connected to the Postgres databse. 
        rsi_periods: Number of periods used to calculate RSI. Default is the standard 14 periods.  
    """
    with engine.begin() as conn:
        indicator_id = get_or_create_lookup(conn, "indicator_lookup", "indicator_name", "rsi")

        conn.execute(text("""
            WITH deltas AS (            -- CTE for difference with prior period
                SELECT 
                    id AS candle_id,
                    open_timestamp,
                    pair_id,
                    interval_id,
                    close_price - LAG(close_price) OVER (PARTITION BY pair_id, interval_id ORDER BY open_timestamp) AS delta 	-- Parition by pair_id and interval_id since they define a unique candle
                FROM candles
            ),
            gain_losses AS (            -- CTE to separate the gains from the losses 
                SELECT 
                    *, 
                    GREATEST(delta, 0) AS gain,
                    GREATEST(-delta, 0) AS loss
                FROM deltas
            ),
            rsi AS (                    -- CTE for RSI calculation
                SELECT
                    *,
                    100 - (100.0 / (1 + 
                        AVG(gain) OVER (PARTITION BY pair_id, interval_id ORDER BY open_timestamp ROWS BETWEEN (:rsi_period - 1) PRECEDING AND CURRENT ROW) / 
                        NULLIF (AVG(loss) OVER (PARTITION BY pair_id, interval_id ORDER BY open_timestamp ROWS BETWEEN (:rsi_period - 1) PRECEDING AND CURRENT ROW), 0))) AS rsi_value,        -- NULIF required to avoid division by zero
                    ROW_NUMBER() OVER (PARTITION BY pair_id, interval_id ORDER BY open_timestamp) AS row_num		                                                            -- Assigns row number so we can filter for >= 14 
                FROM gain_losses
            )
            INSERT INTO indicator_values (candle_id, indicator_id, indicator_value)
            SELECT
                candle_id,
                :indicator_id,
                rsi_value
            FROM rsi
            WHERE row_num > (:rsi_period - 1)
            ;"""), {"indicator_id": indicator_id, "rsi_period": rsi_period})
        

