"""Functions to visualise heatmaps"""

import math

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_heatmap(contingency_table, title):

    # Seaborn to plot the contingency table
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(contingency_table, annot=False, cmap="RdBu", ax=ax)

    ax.invert_yaxis()   # More intuitive format
    ax.set_title(title)

    return fig


def plot_heatmap_grid(contingencies, title=None, colour='RdBu'):
    """Returns figure of all bin probability suplots"""
    n = len(contingencies)
    aspect_ratio = 16 / 9
    cols = max(math.ceil(math.sqrt(n * aspect_ratio)), 1)
    rows = math.ceil(n / cols)
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
    axs = np.array(axs).flatten()     # To make it iterable

    # To ensure all subplots have the same scale for visual comparison
    p_min = min(np.nanmin(c.values) for c in contingencies.values())    # Finds min 
    p_max = max(np.nanmax(c.values) for c in contingencies.values()) 

    # Iterate through each contingency to add it to axs
    for i, (bin_num, contingency) in enumerate(contingencies.items()):
        sns.heatmap(contingency, ax=axs[i], cmap=colour, vmin=p_min, vmax=p_max, cbar=False)
        axs[i].set_title(f"Percentile Bin {bin_num}")
        axs[i].set_ylabel("Take Profit")
        axs[i].set_xlabel("Stop Loss")
        axs[i].invert_yaxis()
        
    for j in range(n, rows * cols):
        # axs[j].set_visible(False)
        fig.delaxes(axs.flat[j])

    # Plot and colour bar spacings
    fig.subplots_adjust(left=0.06, right=0.89, top=0.9, bottom=0.11, hspace=0.6, wspace=0.4)   
    cbar_ax = fig.add_axes([0.93, 0.12, 0.02, 0.78])  # [left, bottom, width, height]

    # One colour bar normalised by the global min and max probabilities
    fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(p_min, p_max), cmap=colour), cax=cbar_ax)
    fig.suptitle(title, fontsize=24)

    return fig