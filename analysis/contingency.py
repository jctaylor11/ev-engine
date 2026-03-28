"""Contingency analysis functions"""


def probability_contingency(df):
    """Compute probability contingency table from outcome counts dataframe"""
    # Calculate probabilities from contingency values using total_candles as denominator
    total_candles = df['total_candles'][0]
    df['probability'] = df['count_a_before_b'] / total_candles

    # The df is in long format, and therefore pivoted to create a contingency table to count values where row threshold is hit before colum threshold
    contingency_table = df.pivot_table(index='threshold_a', columns='threshold_b', values='probability')

    return contingency_table