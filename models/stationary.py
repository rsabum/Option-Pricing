import numpy as np

class StationaryModel():
    """
    A Stationary Model for simulating the dynamics of an asset price
    usgin Geometric Brownian Motion with constant drift and volatility.

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
        mu: float,
        sigma: float
    ):
        """
        Initializes a Jump Diffusion model with the given parameters.

        Parameters:
        -----------
        mu : float
            The drift rate of the asset's return.
        sigma : float
            The volatility of the asset's return.
        """

        self.mu = mu
        self.sigma = sigma

    def simulate(self, S0: float, T: float, M: int, N: int):
        """
        Simulates the path of the asset price and variance over time using the Bates model.

        Parameters:
        -----------
        S0 : float
            Initial asset price.
        T : float
            Total time horizon.
        M : int
            Number of simulated paths.
        N : int
            Number of time steps.

        Returns:
        --------
        S : ndarray
            Simulated asset price paths, shape (N + 1, M).
        """
        dt = T / N

        S = np.zeros((M, N + 1))

        S[:, 0] = S0

        for t in range(1, N+1):
            dW = np.random.normal(scale=np.sqrt(dt))
            S[:, t] = S[:, t-1] * np.exp(
                (self.mu - 0.5 * self.sigma ** 2) * dt + 
                self.sigma * dW
            )

        return S