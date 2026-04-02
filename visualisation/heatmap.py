"""Functions to visualise heatmaps"""

import math

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_heatmap(contingency_table, title):

    # Seaborn to plot the contingency table
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(contingency_table, annot=False, cmap="RdBu", ax=ax,
                cbar_kws={"format": lambda x, _: f"{x*100:.1f}%"})

    ax.invert_yaxis()   # More intuitive format

    ax.set_ylabel("Take Profit", fontsize=18)
    ax.set_xlabel("Stop Loss", fontsize=18)

    ax.set_xticklabels([f"{i*100:.0f}%" for i in contingency_table.columns])
    ax.set_yticklabels([f"{i*100:.0f}%" for i in contingency_table.index])

    fig.suptitle(title, fontsize=24)

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

        # Reformat the default-assigned ticks to percent instead of decimal
        axs[i].set_xticklabels([f"{float(t.get_text())*100:.0f}%" for t in axs[i].get_xticklabels()])
        axs[i].set_yticklabels([f"{float(t.get_text())*100:.0f}%" for t in axs[i].get_yticklabels()])
        
        # More intuive layout with values increasing upwards
        axs[i].invert_yaxis()

    # Removes all the excess unused plots in the grid
    for j in range(n, rows * cols):
        fig.delaxes(axs.flat[j])

    # Plot and colour bar spacings
    fig.subplots_adjust(left=0.06, right=0.89, top=0.88, bottom=0.15, hspace=0.6, wspace=0.4)   
    cbar_ax = fig.add_axes([0.93, 0.12, 0.02, 0.78])  # [left, bottom, width, height]

    # One colour bar normalised by the global min and max probabilities
    fig.colorbar(plt.cm.ScalarMappable(norm=plt.Normalize(p_min, p_max), cmap=colour), cax=cbar_ax,
                 format=plt.FuncFormatter(lambda x, _: f"{x*100:.1f}%"))
    fig.suptitle(title, fontsize=24)

    return fig