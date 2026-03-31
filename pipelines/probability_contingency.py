"""Pipeline for marginal probability contingency analysis"""

import pandas as pd

from database.connection import get_engine
from queries.contingency import get_marginal_query, get_conditional_query
from analysis.contingency import compute_conditional_probability , compute_marginal_probability, compute_evs, contingency_pivot
from visualisation.heatmap import plot_heatmap


HOLDING_PERIOD = 20

INDICATOR_ID = 1
PERCENTILE_BIN = 8
N_BINS = 10


def marginal_probabilities(holding_period=HOLDING_PERIOD):
    """Compute and plot marginal probabilities of hitting threshold A before threshold B for each threshold pair."""
    engine = get_engine()
    query = get_marginal_query()
    outcome_counts = pd.read_sql(query, engine, params={"holding_period": holding_period})
    outcome_probabilities = compute_marginal_probability(outcome_counts)
    outcome_evs = compute_evs(outcome_probabilities)
    contingency_table = contingency_pivot(outcome_evs, values='ev')  

    title = f"P(A before B) and resolved within {holding_period} periods"
    plot_heatmap(contingency_table, title)


def conditional_probabilities(holding_period=HOLDING_PERIOD, number_of_bins=N_BINS, indicator_id=INDICATOR_ID, percentile_bin=PERCENTILE_BIN):
    """Compute and plot conditional probabilities of hitting threshold A before threshold B, for a candle in a given percentile bin for a given indicator."""
    engine = get_engine()
    query = get_conditional_query()
    outcome_counts = pd.read_sql(query, engine, params={"holding_period": holding_period, "number_of_bins": number_of_bins})
    outcome_probabilities = compute_conditional_probability(outcome_counts)
    outcome_evs = compute_evs(outcome_probabilities)    
    contingency_table = contingency_pivot(outcome_evs, values='ev', indicator_id=indicator_id, percentile_bin=percentile_bin)     # Filtered for indicator ID and percentile bin at this stage

    title = f"EV {indicator_id}, Percentile Bin {percentile_bin} and resolved within {holding_period} periods"
    plot_heatmap(contingency_table, title)


if __name__ == "__main__":
    conditional_probabilities()
