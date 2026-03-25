from sqlalchemy import text


def populate_outcomes(engine, threshold):
    """
    Calculate the number of candles passed before the given threshold is hit, for each candle. 

    Assumes candle IDs are in order of date and contiguously stored. 
    """
    with engine.begin() as conn: 
        if threshold > 0: 
            # If threshold is positive, threshold is hit when the high exceeds the close
            join_condition = "b.high_price > a.close_price * (1 + :threshold)"
        else:
            # If threshold is negative, threshold is hit when the low goes below the close
            join_condition = "b.low_price < a.close_price * (1 + :threshold)"

        # LEFT JOIN used so applies to each parent candle, rather than silently dropping
        conn.execute(text(f"""
            INSERT INTO outcomes (candle_id, return_threshold, candles_to_hit)
            SELECT 
                a.id AS candle_id,
                :threshold AS return_threshold,
                MIN(b.id) - a.id AS candles_to_hit      -- Assumes candle IDs are in order of date and contiguously stored
            FROM candles a
            LEFT JOIN candles b ON b.id > a.id AND {join_condition}
            GROUP BY a.id, a.high_price
            ORDER BY a.id
            LIMIT 1000
            ON CONFLICT (candle_id, return_threshold) DO UPDATE
                SET candles_to_hit = EXCLUDED.candles_to_hit
        """), {"threshold": threshold})