"""Contingency analysis functions"""


def marginal_probability_contingency(df):
    """Compute probability contingency table from outcome counts dataframe
    
    Args:
        df: Long format dataframe of threshold pairs
        
    Returns: 
        DataFrame: Contigency table with threshold A as rows, threshold B as columns, and values as marginal probabilities
    """
    df = df.copy()  # Since df is mutated by adding probability column

    # Extract total number of candles from dataframe, and use to calculate probably of threshold A hit before threshold B
    total_candles = df['total_candles'][0]
    df['probability'] = df['count_a_before_b'] / total_candles

    # The df is in long format, and therefore pivoted to create a contingency table to count values where row threshold is hit before colum threshold
    contingency_table = df.pivot_table(index='threshold_a', columns='threshold_b', values='probability')

    return contingency_table


def conditional_probability_contingency(df, indicator_id, percentile_bin):
    """Compute conditional probability of threshold A before threshold B for a given indicator's percentile bin.
    
    Args:
        df: Long format dataframe of threshold pairs
        indicator_id: Indicator ID for the indicator values being conditioned on
        percentile_bin: Indicator value's percentile bin
        
    Returns: 
        DataFrame: Contingency table with threshold A as rows, threshold B as columns, values as conditional probabilities.
    """
    df = df.copy()
    
    # Calculate the conditional probability that of the candles in the given percentile bin for the given indicator, 
    # the outcome was threshold A hit before threshold B
    df['probability'] = df['a_hit_before_b'] / df['bin_candle_count']

    # Filter for the given indicator_id, and then for the given percentile bin
    df = df.loc[df['indicator_id'] == indicator_id]
    df = df.loc[df['percentile_bin'] == percentile_bin] 

    # Pivot the filtered conditional probability df to a contingency table
    single_bin_contingency = df.pivot_table(values='probability', index='threshold_a', columns='threshold_b')

    return single_bin_contingency



# maybe the df docstring needs updating to say it takes the df of COUNTS?? 