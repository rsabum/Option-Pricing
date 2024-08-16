import numpy as np

class StationaryModel():
    """
    A Stationary Model for simulating the dynamics of an asset price
    using Geometric Brownian Motion (GBM) with constant drift and volatility.

    Attributes:
    -----------
    mu : float
        The drift rate of the asset's return, representing the average rate of return of the asset.
    sigma : float
        The volatility of the asset's return, representing the standard deviation of the return.

    Methods:
    --------
    simulate(S0, T, M, N):
        Simulates the path of the asset price over time using GBM.
    """

    def __init__(
        self,
        mu: float = 0.05,
        sigma: float = 0.04
    ):
        """
        Initializes a StationaryModel with the given parameters.

        Parameters:
        -----------
        mu : float
            The drift rate of the asset's return. Default is 0.05.
        sigma : float
            The volatility of the asset's return. Default is 0.04.
        """
        
        self.mu = mu
        self.sigma = sigma

    def simulate(self, S0: float, T: float, M: int, N: int):
        """
        Simulates the path of the asset price over time using Geometric Brownian Motion (GBM).

        Parameters:
        -----------
        S0 : float
            Initial asset price, the starting value of the asset.
        T : float
            Total time horizon for the simulation, usually in years.
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

        # Initialize array to hold asset price paths
        S = np.zeros((M, N + 1))  

        S[:, 0] = S0    # Set initial price for all paths

        for t in range(1, N + 1):
            # Generate Brownian motion increment
            dW = np.random.normal(scale=np.sqrt(dt), size=M)
            
            # Calculate price process with GBM
            S[:, t] = S[:, t - 1] * np.exp(
                (self.mu - 0.5 * self.sigma ** 2) * dt +
                self.sigma * dW
            )

        return S
