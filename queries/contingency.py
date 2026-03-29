"""Queries for contingency analysis"""

from sqlalchemy import text

def get_marginal_query():
    """Return query for unconditional counts of threshold A hit before threshold B for all threshold pairs"""
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


def get_conditional_query():
    """Return query for counts of threshold A hit before threshold B conditional on the percentile bin of indicator value.
    
    Conditions on each indicator independently, and includes the total count for downstream probability calculations.
    """
    query = text("""
        WITH indicator_binned AS (
            SELECT                              -- Discretises the indicators values into bins of specified number
                candle_id,
                indicator_id,
                NTILE(:number_of_bins) OVER (PARTITION BY indicator_id ORDER BY indicator_value) AS percentile_bin
            FROM indicator_values              
            WHERE candle_id IN (SELECT candle_id FROM outcomes)
        ),
        indicator_binned_counts AS (            -- CTE for count of candles in each bin, only for pandas to pull through in one database request
            SELECT                              -- (ie it's not used in the core logic)
                indicator_id,
                percentile_bin,
                COUNT(*) AS bin_candle_count
            FROM indicator_binned
            GROUP BY indicator_id, percentile_bin
        )
        SELECT
            a.return_threshold AS threshold_a,
            b.return_threshold AS threshold_b,
            ib.indicator_id,
            ib.percentile_bin,
            COUNT(*) AS a_hit_before_b,
            ibc.bin_candle_count
        FROM outcomes a
        JOIN indicator_binned ib 
            ON ib.candle_id = a.candle_id
        JOIN outcomes b 
            ON b.candle_id = a.candle_id 
            AND (a.return_threshold * b.return_threshold < 0)
        JOIN indicator_binned_counts ibc 
            ON ibc.percentile_bin = ib.percentile_bin 
            AND ibc.indicator_id = ib.indicator_id
        WHERE 
            (a.candles_to_hit < b.candles_to_hit 
            OR (a.candles_to_hit IS NOT NULL AND b.candles_to_hit IS NULL))
            AND a.candles_to_hit <= :holding_period
        GROUP BY 
            threshold_a, 
            threshold_b, 
            ib.indicator_id, 
            ib.percentile_bin, 
            ibc.bin_candle_count
        ORDER BY threshold_a;
    """)

    return query
    