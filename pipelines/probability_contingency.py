"""Pipeline for marginal probability contingency analysis"""

import pandas as pd

from database.connection import get_engine
from queries.contingency import get_marginal_query, get_conditional_query
from analysis.contingency import marginal_probability_contingency, conditional_probability_contingency
from visualisation.heatmap import plot_heatmap


HOLDING_PERIOD = 50

INDICATOR_ID = 1
PERCENTILE_BIN = 1
N_BINS = 10

def marginal_probabilities(holding_period=HOLDING_PERIOD):
    """Compute and plot marginal probabilities of hitting threshold A before threshold B for each threshold pair."""
    engine = get_engine()
    query = get_marginal_query()
    outcomes_counts = pd.read_sql(query, engine, params={"holding_period": holding_period})
    contingency_table = marginal_probability_contingency(outcomes_counts)  
    title = f"P(A before B) and resolved within {holding_period} periods"
    plot_heatmap(contingency_table, title)


def conditional_probabilities(holding_period=HOLDING_PERIOD, number_of_bins=N_BINS, indicator_id=INDICATOR_ID, percentile_bin=PERCENTILE_BIN):
    """Compute and plot conditional probabilities of hitting threshold A before threshold B, for a candle in a given percentile bin for a given indicator."""
    engine = get_engine()
    query = get_conditional_query()
    outcome_counts = pd.read_sql(query, engine, params={"holding_period": holding_period, "number_of_bins": number_of_bins})
    contingency_table = conditional_probability_contingency(outcome_counts, indicator_id, percentile_bin)
    title = f"P(A before B | Indicator ID {indicator_id}, Percentile Bin {percentile_bin}) and resolved within {holding_period} periods"
    plot_heatmap(contingency_table, title)


if __name__ == "__main__":
    conditional_probabilities()
