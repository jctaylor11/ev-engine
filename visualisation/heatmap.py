"""Functions to visualise heatmaps"""

import matplotlib.pyplot as plt
import seaborn as sns

def plot_heatmap(contingency_table, title):

    # Seaborn to plot the contingency table
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(contingency_table, annot=False, cmap="RdBu")

    ax.invert_yaxis()   # More intuitive format
    plt.title(title)
    plt.show()