import numpy as np

class model(object):
    """
    Base Model Class

    Attributes:
    -----------
    mu : float
        The drift rate of the asset's return.
    sigma : float
        The volatility of the asset's return.

    Methods:
    --------
    simulate(S0, T, M, N):
        Simulates the path of the asset price over time.
    fit(prices):
        Fits the GBM model to historical price data using Maximum Likelihood Estimation.

    """

    def __init__(
        self,
        *args,
        **kwargs
    ):
        """
        Initializes an assets price model with the given parameters.
        """

        raise NotImplementedError

    def simulate(self, *args, **kwargs):
        """
        Simulates the path of the asset price over time.

        Returns:
        --------
        S : ndarray
            Simulated asset price paths, shape (N + 1, M).
        """
        
        raise NotImplementedError