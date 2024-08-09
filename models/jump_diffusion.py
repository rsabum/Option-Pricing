import numpy as np
from ._model import model

class JumpDiffusionModel(model):
    """
    An extension of the Stationary Model to incorporate stochastic jumps in the assets price.

    Attributes:
    -----------
    mu : float
        The drift rate of the asset's return.
    sigma : float
        The volatility of the asset's return.
    lambda_J : float
        The intensity (or rate) of the jump process.
    mu_J : float
        The mean of the log-normal distribution for jump sizes.
    sigma_J : float
        The standard deviation of the log-normal distribution for jump sizes.

    Methods:
    --------
    simulate_path(S0, T, M, N):
        Simulates the path of the asset price over time.

    """

    def __init__(
        self,
        mu: float,
        sigma: float,
        lambda_J: float,
        mu_J: float,
        sigma_J: float
    ):
        """
        Initializes a Jump Diffusion model with the given parameters.

        Parameters:
        -----------
        mu : float
            The drift rate of the asset's return.
        sigma : float
            The volatility of the asset's return.
        lambda_J : float
            The intensity (or rate) of the jump process.
        mu_J : float
            The mean of the log-normal distribution for jump sizes.
        sigma_J : float
            The standard deviation of the log-normal distribution for jump sizes.
        """

        self.mu = mu
        self.sigma = sigma
        self.lambda_J = lambda_J    # Jump intensity
        self.mu_J = mu_J            # Mean of jump size
        self.sigma_J = sigma_J      # Volatility of jump size

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
            # Brownian motion increment
            dW = np.random.normal(scale=np.sqrt(dt))

            # Price process without jumps
            S[:, t] = S[:, t-1] * np.exp(
                (self.mu - 0.5 * self.sigma ** 2) * dt + 
                self.sigma * dW
            )

            # Jump component
            Jumps = np.random.poisson(self.lambda_J * dt, M)  # Number of jumps
            JumpSizes = np.exp(
                np.random.normal(self.mu_J, self.sigma_J, M)
            ) - 1

            # Adjust Price for jumps
            S[:, t] *= (1 + Jumps * JumpSizes)

        return S
    
    