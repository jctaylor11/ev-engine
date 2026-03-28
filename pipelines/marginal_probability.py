"""Pipeline for marginal probability contingency analysis"""

import pandas as pd

from database.connection import get_engine
from queries.contingency import get_marginal_query
from analysis.contingency import probability_contingency
from visualisation.heatmap import plot_heatmap


HOLDING_PERIOD = 14

def marginal_probabilities(holding_period=HOLDING_PERIOD):
    """Compute and plot contingent probability of hitting threshold A before threshold B for each threshold pair"""
    engine = get_engine()
    query = get_marginal_query()
    outcomes_counts = pd.read_sql(query, engine, params={"holding_period": holding_period})
    contingency_table = probability_contingency(outcomes_counts)  
    title = f"P(A before B) and resolved within {holding_period} periods"
    plot_heatmap(contingency_table, title)


if __name__ == "__main__":
    marginal_probabilities()