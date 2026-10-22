"""Pipeline for marginal probability contingency analysis"""

import tomllib

import matplotlib.pyplot as plt
import pandas as pd

from database.connection import get_engine
from queries.contingency import get_marginal_query, get_conditional_query
from analysis.contingency import compute_conditional_probability , compute_marginal_probability, compute_evs, contingency_pivot, contingency_pivot_all_bins
from visualisation.heatmap import plot_heatmap, plot_heatmap_grid


HOLDING_PERIOD = 72

INDICATOR_ID = 1
PERCENTILE_BIN = 1
N_BINS = 10


def unconditional_ev(holding_period, date_range):
    """Compute and plot unconditional EV for each threshold pair."""
    engine = get_engine()
    query = get_marginal_query()
    outcome_counts = pd.read_sql(query, engine, params={"holding_period": holding_period})
    outcome_probabilities = compute_marginal_probability(outcome_counts)
    outcome_evs = compute_evs(outcome_probabilities)
    contingency_table = contingency_pivot(outcome_evs, values='ev')  

    title = f"Unconditional EV, resolved within {holding_period} periods\n{date_range}"
    plot_heatmap(contingency_table, title)
    plt.show()


def conditional_ev(indicator_id, number_of_bins, percentile_bin, holding_period, date_range):
    """Compute and plot conditional EV for a given percentile bin of a given indicator for each threshold pair."""
    engine = get_engine()
    query = get_conditional_query()
    outcome_counts = pd.read_sql(query, engine, params={"holding_period": holding_period, "number_of_bins": number_of_bins})
    outcome_probabilities = compute_conditional_probability(outcome_counts)
    outcome_evs = compute_evs(outcome_probabilities)   
    contingency_table = contingency_pivot(outcome_evs, values='ev', indicator_id=indicator_id, percentile_bin=percentile_bin)     # Filtered for indicator ID and percentile bin at this stage

    title = f"EV, Indicator ID {indicator_id}, Percentile Bin {percentile_bin}, Resolved Within {holding_period} Periods\n{date_range}"
    plot_heatmap(contingency_table, title)
    plt.show()


def conditional_ev_grid(indicator_id, number_of_bins, holding_period, date_range):
    """Compute and plot conditional EV for all percentile bins of a given indicator as a grid of heatmaps."""
    engine = get_engine()
    query = get_conditional_query()
    outcome_counts = pd.read_sql(query, engine, params={"holding_period": holding_period, "number_of_bins": number_of_bins})
    outcome_probabilities = compute_conditional_probability(outcome_counts)
    outcome_evs = compute_evs(outcome_probabilities)
    contingencies = contingency_pivot_all_bins(outcome_evs, indicator_id=indicator_id, number_of_bins=number_of_bins)

    title = f"EV by Percentile Bin — Indicator ID {indicator_id}, Resolved Within {holding_period} Periods, {date_range}"
    plot_heatmap_grid(contingencies, title=title)
    plt.show()


if __name__ == "__main__":
    with open("config/config.toml", "rb") as config_file:
        config = tomllib.load(config_file)
    date_range = f"{config['data']['start']} to {config['data']['end']}"

    unconditional_ev(
        holding_period=HOLDING_PERIOD,
        date_range=date_range
    )

    conditional_ev(
        indicator_id=INDICATOR_ID, 
        number_of_bins=N_BINS, 
        percentile_bin=PERCENTILE_BIN, 
        holding_period=HOLDING_PERIOD,
        date_range=date_range
    )
    
    conditional_ev_grid(
        indicator_id=INDICATOR_ID, 
        number_of_bins=N_BINS, 
        holding_period=HOLDING_PERIOD,
        date_range=date_range
    )
