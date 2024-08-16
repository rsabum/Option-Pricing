import numpy as np

class StochasticVolatilityModel():
    """
    An extension of the Stationary Model to include a mean-reverting stochastic volatility component.

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

    Methods:
    --------
    simulate(S0, T, M, N):
        Simulates the path of the asset price over time incorporating stochastic volatility.
    """

    def __init__(
        self,
        mu: float = 0.05,
        kappa: float = 2.0,
        theta: float = 0.04,
        sigma: float = 0.5,
        rho: float = -0.5
    ):
        """
        Initializes the Stochastic Volatility Model with the given parameters.

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
        """
        self.mu = mu
        self.kappa = kappa
        self.theta = theta
        self.sigma = sigma
        self.rho = rho

    def simulate(self, S0: float, T: float, M: int, N: int):
        """
        Simulates the path of the asset price and variance over time incorporating stochastic volatility.

        Parameters:
        -----------
        S0 : float
            Initial asset price.
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

            # Simulate the asset price process with stochastic volatility
            S[:, t] = S[:, t - 1] * np.exp(
                (self.mu - 0.5 * V[:, t - 1]) * dt +
                np.sqrt(V[:, t - 1]) * dW_1
            )

        return S
