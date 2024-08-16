import numpy as np

class StochasticVolatilityJumpModel():
    """
    An extension of the Stochastic Volatility model to incorporate stochastic
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
    simulate(S0, V0, T, M, N):
        Simulates the path of the asset price over time incorporating stochastic volatility and jumps.
    """

    def __init__(
        self,
        mu: float = 0.05,
        kappa: float = 2.0,
        theta: float = 0.04,
        sigma: float = 0.5,
        rho: float = -0.5,
        lambda_J: float = 0.1,
        mu_J: float = 0.02,
        sigma_J: float = 0.1
    ):
        """
        Initializes the Stochastic Volatility Jump Model with the given parameters.

        Parameters:
        -----------
        mu : float
            The drift rate of the asset's return. Default is 0.05.
        kappa : float
            The rate of mean reversion for the variance process. Default is 2.0.
        theta : float
            The long-term mean of the variance. Default is 0.04.
        sigma : float
            The volatility of the variance process. Default is 0.5.
        rho : float
            The correlation between the asset price and variance processes. Default is -0.5.
        lambda_J : float
            The intensity (or rate) of the jump process. Default is 0.1.
        mu_J : float
            The mean of the log-normal distribution for jump sizes. Default is 0.02.
        sigma_J : float
            The standard deviation of the log-normal distribution for jump sizes. Default is 0.1.
        """

        self.mu = mu
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho
        self.lambda_J = lambda_J
        self.mu_J = mu_J
        self.sigma_J = sigma_J

    def simulate(self, S0: float, T: float, M: int, N: int):
        """
        Simulates the path of the asset price and variance over time incorporating
        stochastic volatility and jumps.

        Parameters:
        -----------
        S0 : float
            Initial asset price.
        V0 : float
            Initial variance.
        T : float
            Total time horizon for the simulation.
        M : int
            Number of simulated paths (trajectories) to generate.
        N : int
            Number of time steps in each path.

        Returns:
        --------
        S : ndarray
            Simulated asset price paths with shape (M, N + 1), where M is the number of paths and N + 1 is the number of time steps.
        """

        # Calculate time increment for each step
        dt = T / N  

        # Initialize arrays to hold asset price paths and variance paths
        S = np.zeros((M, N + 1))
        V = np.zeros((M, N + 1))

        S[:, 0] = S0            # Set initial price for all paths
        V[:, 0] = self.theta    # Set initial variance to the long-term mean

        for t in range(1, N + 1):
            # Generate correlated Brownian motion increments
            Z1 = np.random.normal(size=(M,))
            Z2 = np.random.normal(size=(M,))
            dW_1 = np.sqrt(dt) * Z1
            dW_2 = np.sqrt(dt) * (self.rho * Z1 + np.sqrt(1 - self.rho**2) * Z2)

            # Simulate the variance process
            V[:, t] = np.maximum(
                V[:, t - 1] + self.kappa * (self.theta - V[:, t - 1]) * dt +
                self.sigma * np.sqrt(V[:, t - 1]) * dW_2, 0
            )

            # Simulate the asset price process without jumps
            S[:, t] = S[:, t - 1] * np.exp(
                (self.mu - 0.5 * V[:, t - 1]) * dt +
                np.sqrt(V[:, t - 1]) * dW_1
            )

            # Generate jumps
            Jumps = np.random.poisson(self.lambda_J * dt, M)  # Number of jumps per path
            JumpSizes = np.exp(
                np.random.normal(self.mu_J, self.sigma_J, M)
            ) - 1  # Sizes of the jumps

            # Adjust price paths for jumps
            S[:, t] *= (1 + Jumps * JumpSizes)

        return S
