"""Queries for contingency analysis"""

from sqlalchemy import text

def get_marginal_query():
    """Return query for unconditional probability of P(A before B) for all threshold pairs"""
    query = text("""
        WITH candle_count AS (
            SELECT
                COUNT (DISTINCT candle_id) AS total_candles
            FROM OUTCOMES
        )
        SELECT
            a.return_threshold AS threshold_a,
            b.return_threshold AS threshold_b,
            COUNT(*) AS count_a_before_b,
            total_candles
        FROM outcomes a
        JOIN outcomes b ON a.candle_id = b.candle_id AND (a.return_threshold * b.return_threshold < 0)
        CROSS JOIN candle_count
        WHERE (a.candles_to_hit < b.candles_to_hit
            OR (a.candles_to_hit IS NOT NULL AND b.candles_to_hit IS NULL)) 
            AND a.candles_to_hit <= :holding_period
        GROUP BY threshold_a, threshold_b, total_candles
        ORDER BY threshold_a;
    """)

    return query