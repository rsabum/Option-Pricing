import matplotlib.pyplot as plt
import numpy as np

def plot_error(
    error_history: list,
    window_size: int
): 
    """
    Plot the average TD error over the given number of batches.
    
    Parameters
    ----------
    error_history: list
        The list of TD errors for each batch.

    window_size: int
        The number of batches to average over.

    Returns
    -------
    None
    """

    N = len(error_history)
    running_avg = [np.mean(error_history[i-window_size:i+1]) for i in range(window_size, N)]
    running_std = [np.std(error_history[i-window_size:i+1]) for i in range(window_size, N)]

    fig = plt.figure()
    ax = fig.add_subplot(111, label="1")

    ax.set_ylabel('Error')
    ax.set_xlabel('Batch')
    ax.plot(range(N - window_size), running_avg)
    ax.fill_between(range(N - window_size), np.array(running_avg) - np.array(running_std), np.array(running_avg) + np.array(running_std), alpha=0.2)

    plt.title(f'TD Error Over {N} Batches')

    