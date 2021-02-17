import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

def plot_anim(
    pos_history,
    mark,
    figsize,
    limits,
    title="Trajectory"
    
):
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    # Get number of iterations
    n_iters = len(pos_history)
    # Customize plot
    ax.set_title(title)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_xlim(limits[0])
    ax.set_ylim(limits[1])
    # Mark global best if possible
    if mark is not None:
        ax.scatter(mark[0], mark[1], color="red", marker="x")
    # Put scatter skeleton
    plot = ax.scatter(x=[], y=[], c="black", alpha=0.6)
    # Do animation
    anim = animation.FuncAnimation(
        fig=fig,
        func=_animate,
        frames=range(n_iters),
        fargs=(pos_history, plot),
        interval=30,
        repeat=True
        )
    return anim

def _animate(i, data, plot):
    current_pos = data[i]
    if np.array(current_pos).shape[1] == 2:
        plot.set_offsets(current_pos)
    else:
        plot._offsets3d = current_pos.T
    return (plot,)