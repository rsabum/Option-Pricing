import numpy as np
from ._model import model

class MeanRevertingModel(model):
    """
    An Ornstein-Uhlenbeck model for simulating the dynamics of a mean reverting asset
    with constant volatility.

    Attributes:
    -----------
    mu : float
        The long-term mean of the proceess.
    theta : float
        The rate of mean reversion
    sigma : float
        The volatility of the process.

    Methods:
    --------
    simulate_path(S0, T, M, N):
        Simulates the path of the asset price over time.

    """

    def __init__(
        self,
        mu: float,
        theta: float,
        sigma: float,
    ):
        """
        Initializes the Bates model with the given parameters.

        Parameters:
        -----------
        mu : float
            The drift rate of the asset's return.
        kappa : float
            The rate of mean reversion for the variance process.
        theta : float
            The long-term mean of the variance.
        sigma : float
            The volatility of the variance process.
        rho : float
            The correlation between the asset price and variance processes.
        lambda_J : float
            The intensity (or rate) of the jump process.
        mu_J : float
            The mean of the log-normal distribution for jump sizes.
        sigma_J : float
            The standard deviation of the log-normal distribution for jump sizes.
        """
        self.mu = mu
        self.theta = theta
        self.sigma = sigma

    def simulate_path(self, S0: float, T: float, M: int, N: int):
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
            S[:, t] = S[:, t-1] + self.theta * (self.mu - S[:, t-1]) * dt + self.sigma * dW

        return S
    
    