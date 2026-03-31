"""Contingency analysis functions"""


def compute_marginal_probability(df): 
    """Compute marginal probability of threshold A hit before threshold Bn.
    
    Args:
        df: Raw threshold pair counts dataframe.
        
    Returns:
        Dataframe: Original dataframe including outcome probabilities."""
    df = df.copy()

    # Extract total number of candles from dataframe, and use to calculate probably of threshold A hit before threshold B
    total_candles = df['total_candles'][0]
    df['probability'] = df['count_a_before_b'] / total_candles

    return df


def compute_conditional_probability(df):
    """Compute conditional probability of threshold A before threshold B for a given indicator's percentile bin.
    
    Args:
        df: Raw threshold pair counts dataframe.
        
    Returns:
        Dataframe: Original dataframe including outomce probabillities."""
    df = df.copy()
    
    # Calculate the conditional probability that of the candles in the given percentile bin for the given indicator, 
    # the outcome was threshold A hit before threshold B
    df['probability'] = df['a_hit_before_b'] / df['bin_candle_count']

    return df


def contingency_pivot(df, indicator_id=None, percentile_bin=None):
    """Pivot dataframe to contingency table"""
    if indicator_id is not None and percentile_bin is not None:
        # Filter for the given indicator_id, and then for the given percentile bin
        df = df.loc[df['indicator_id'] == indicator_id]
        df = df.loc[df['percentile_bin'] == percentile_bin] 

    # The df is in long format, and therefore pivoted to create a contingency table to count values where row threshold is hit before colum threshold
    contingency_table = df.pivot_table(index='threshold_a', columns='threshold_b', values='probability')

    return contingency_table

