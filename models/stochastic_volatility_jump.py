import numpy as np

class StochasticVolatilityJumpModel():
    """
    An extension of the Heston Stochastic Volatility model to incorporate sochastic 
    jumps in the asset price.

    Attributes:
    -----------
    mu : float
        The drift rate of the asset's return.
    kappa : float
        The rate at which the variance reverts to the long-term mean.
    theta : float
        The long-term mean of the variance.
    sigma : float
        The volatility of the variance process.
    rho : float
        The correlation between the asset price and variance processes.
    lambda_J : float
        The intensity (or rate) of the jump process, i.e., the average number of jumps per unit time.
    mu_J : float
        The mean of the log-normal distribution for jump sizes.
    sigma_J : float
        The standard deviation of the log-normal distribution for jump sizes.

    Methods:
    --------
    simulate_path(S0, V0, T, M, N):
        Simulates the path of the asset price over time.

    """

    def __init__(
        self,
        mu: float,
        kappa: float,
        theta: float,
        sigma: float,
        rho: float,
        lambda_J: float,
        mu_J: float,
        sigma_J: float
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
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho
        self.lambda_J = lambda_J
        self.mu_J = mu_J
        self.sigma_J = sigma_J

    def simulate_path(self, S0: float, V0: float, T: float, M: int, N: int):
        """
        Simulates the path of the asset price and variance over time using the Bates model.

        Parameters:
        -----------
        S0 : float
            Initial asset price.
        V0 : float
            Initial variance.
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
        V = np.zeros((M, N + 1))

        S[:, 0] = S0
        V[:, 0] = V0

        for t in range(1, N+1):
            Z1 = np.random.normal(size=(M,))
            Z2 = np.random.normal(size=(M,))
            dW_1 = np.sqrt(dt) * Z1
            dW_2 = np.sqrt(dt) * (self.rho * Z1 + np.sqrt(1 - self.rho**2) * Z2)

            # Variance process
            V[:, t] = np.maximum(
                V[:, t-1] + self.kappa * (self.theta - V[:, t-1]) * dt +
                self.sigma * np.sqrt(V[:, t-1]) * dW_2, 0
            )

            # Price process without jumps
            S[:, t] = S[:, t-1] * np.exp(
                (self.mu - 0.5 * V[:, t-1]) * dt + 
                np.sqrt(V[:, t-1]) * dW_1
            )

            # Jump component
            Jumps = np.random.poisson(self.lambda_J * dt, M)  # Number of jumps
            JumpSizes = np.exp(
                np.random.normal(self.mu_J, self.sigma_J, M)
            ) - 1

            # Adjust Price for jumps
            S[:, t] *= (1 + Jumps * JumpSizes)

        return S
    
    