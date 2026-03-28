SELECT 
    candles.id,
    candles.open_timestamp,
    candles.high_price,
    MAX(CASE WHEN o.return_threshold = -0.10 THEN o.candles_to_hit END) AS "hit_-0.10",
    MAX(CASE WHEN o.return_threshold = -0.09 THEN o.candles_to_hit END) AS "hit_-0.09",
    MAX(CASE WHEN o.return_threshold = -0.08 THEN o.candles_to_hit END) AS "hit_-0.08",
    MAX(CASE WHEN o.return_threshold = -0.07 THEN o.candles_to_hit END) AS "hit_-0.07",
    MAX(CASE WHEN o.return_threshold = -0.06 THEN o.candles_to_hit END) AS "hit_-0.06",
    MAX(CASE WHEN o.return_threshold = -0.05 THEN o.candles_to_hit END) AS "hit_-0.05",
    MAX(CASE WHEN o.return_threshold = -0.04 THEN o.candles_to_hit END) AS "hit_-0.04",
    MAX(CASE WHEN o.return_threshold = -0.03 THEN o.candles_to_hit END) AS "hit_-0.03",
    MAX(CASE WHEN o.return_threshold = -0.02 THEN o.candles_to_hit END) AS "hit_-0.02",
    MAX(CASE WHEN o.return_threshold = -0.01 THEN o.candles_to_hit END) AS "hit_-0.01",
    MAX(CASE WHEN o.return_threshold = 0.01 THEN o.candles_to_hit END) AS "hit_+0.01",
    MAX(CASE WHEN o.return_threshold = 0.02 THEN o.candles_to_hit END) AS "hit_+0.02",
    MAX(CASE WHEN o.return_threshold = 0.03 THEN o.candles_to_hit END) AS "hit_+0.03",
    MAX(CASE WHEN o.return_threshold = 0.04 THEN o.candles_to_hit END) AS "hit_+0.04",
    MAX(CASE WHEN o.return_threshold = 0.05 THEN o.candles_to_hit END) AS "hit_+0.05",
    MAX(CASE WHEN o.return_threshold = 0.06 THEN o.candles_to_hit END) AS "hit_+0.06",
    MAX(CASE WHEN o.return_threshold = 0.07 THEN o.candles_to_hit END) AS "hit_+0.07",
    MAX(CASE WHEN o.return_threshold = 0.08 THEN o.candles_to_hit END) AS "hit_+0.08",
    MAX(CASE WHEN o.return_threshold = 0.09 THEN o.candles_to_hit END) AS "hit_+0.09",
    MAX(CASE WHEN o.return_threshold = 0.10 THEN o.candles_to_hit END) AS "hit_+0.10"
FROM candles
JOIN outcomes AS o ON candles.id = o.candle_id
GROUP BY candles.id, candles.open_timestamp, candles.high_price;  