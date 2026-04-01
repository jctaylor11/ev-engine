"""Pipeline for marginal probability contingency analysis"""

import matplotlib.pyplot as plt
import pandas as pd

from database.connection import get_engine
from queries.contingency import get_marginal_query, get_conditional_query
from analysis.contingency import compute_conditional_probability , compute_marginal_probability, compute_evs, contingency_pivot
from visualisation.heatmap import plot_heatmap, plot_heatmap_grid


HOLDING_PERIOD = 20

INDICATOR_ID = 1
PERCENTILE_BIN = 8
N_BINS = 10


def marginal_ev(holding_period=HOLDING_PERIOD):
    """Compute and plot unconditional EV for each threshold pair."""
    engine = get_engine()
    query = get_marginal_query()
    outcome_counts = pd.read_sql(query, engine, params={"holding_period": holding_period})
    outcome_probabilities = compute_marginal_probability(outcome_counts)
    outcome_evs = compute_evs(outcome_probabilities)
    contingency_table = contingency_pivot(outcome_evs, values='ev')  

    title = f"EV, resolved within {holding_period} periods"
    plot_heatmap(contingency_table, title)


def conditional_ev(holding_period=HOLDING_PERIOD, number_of_bins=N_BINS, indicator_id=INDICATOR_ID, percentile_bin=PERCENTILE_BIN):
    """Compute and plot conditional EV for a given percentile bin of a given indicator for each threshold pair."""
    engine = get_engine()
    query = get_conditional_query()
    outcome_counts = pd.read_sql(query, engine, params={"holding_period": holding_period, "number_of_bins": number_of_bins})
    outcome_probabilities = compute_conditional_probability(outcome_counts)
    outcome_evs = compute_evs(outcome_probabilities)   
    contingency_table = contingency_pivot(outcome_evs, values='ev', indicator_id=indicator_id, percentile_bin=percentile_bin)     # Filtered for indicator ID and percentile bin at this stage

    title = f"EV, Indicator {indicator_id}, Percentile Bin {percentile_bin} and resolved within {holding_period} periods"
    plot_heatmap(contingency_table, title)
    plt.show()


def conditional_ev_grid(holding_period=HOLDING_PERIOD, number_of_bins=N_BINS, indicator_id=INDICATOR_ID):
    """Compute and plot conditional EV for all percentile bins of a given indicator as a grid of heatmaps."""
    engine = get_engine()
    query = get_conditional_query()
    outcome_counts = pd.read_sql(query, engine, params={"holding_period": holding_period, "number_of_bins": number_of_bins})
    outcome_probabilities = compute_conditional_probability(outcome_counts)
    outcome_evs = compute_evs(outcome_probabilities)

    # Compute contingency table for each bin and store in dictionary to pass to plotting function
    contingencies = {}
    for bin_n in range(1, number_of_bins + 1):
        contingencies[bin_n] = contingency_pivot(outcome_evs, values='ev', indicator_id=indicator_id, percentile_bin=bin_n)

    title = f"EV by Percentile Bin — Indicator {indicator_id}, resolved within {holding_period} periods"
    plot_heatmap_grid(contingencies, title=title)
    plt.show()


if __name__ == "__main__":
    # conditional_ev()
    conditional_ev_grid()
