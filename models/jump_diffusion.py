import numpy as np

class JumpDiffusionModel():
    """
    An extension of the Stationary Model to incorporate jumps in the asset's price process.

    Attributes:
    -----------
    mu : float
        The drift rate of the asset's return, representing the average rate of return of the asset.
    sigma : float
        The volatility of the asset's return, representing the standard deviation of the return.
    lambda_J : float
        The intensity (or rate) of the jump process, representing the average number of jumps per unit time.
    mu_J : float
        The mean of the log-normal distribution for jump sizes, indicating the average size of the jumps.
    sigma_J : float
        The standard deviation of the log-normal distribution for jump sizes, indicating the variability of jump sizes.

    Methods:
    --------
    simulate(S0, T, M, N):
        Simulates the path of the asset price over time incorporating stochastic jumps.
    """

    def __init__(
        self,
        mu: float = 0.05,
        sigma: float = 0.04,
        lambda_J: float = 0.1,
        mu_J: float = 0.02,
        sigma_J: float = 0.1
    ):
        """
        Initializes a Jump Diffusion model with the given parameters.

        Parameters:
        -----------
        mu : float
            The drift rate of the asset's return. Default is 0.05.
        sigma : float
            The volatility of the asset's return. Default is 0.04.
        lambda_J : float
            The intensity (or rate) of the jump process. Default is 0.1.
        mu_J : float
            The mean of the log-normal distribution for jump sizes. Default is 0.02.
        sigma_J : float
            The standard deviation of the log-normal distribution for jump sizes. Default is 0.1.
        """

        self.mu = mu
        self.sigma = sigma
        self.lambda_J = lambda_J    # Jump intensity: average number of jumps per time unit
        self.mu_J = mu_J            # Mean of jump size: average magnitude of jumps
        self.sigma_J = sigma_J      # Volatility of jump size: variability in jump magnitudes

    def simulate(self, S0: float, T: float, M: int, N: int):
        """
        Simulates the path of the asset price over time incorporating jumps.

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
        """\
        
        # Calculate time increment for each step
        dt = T / N  

        # Initialize array to hold asset price paths
        S = np.zeros((M, N + 1))  
        
        S[:, 0] = S0  # Set initial price for all paths

        for t in range(1, N + 1):
            # Generate Brownian motion increment
            dW = np.random.normal(scale=np.sqrt(dt), size=M)

            # Calculate price process without jumps
            S[:, t] = S[:, t - 1] * np.exp(
                (self.mu - 0.5 * self.sigma ** 2) * dt + 
                self.sigma * dW
            )

            # Generate jump component
            Jumps = np.random.poisson(self.lambda_J * dt, M)  # Number of jumps per path
            JumpSizes = np.exp(
                np.random.normal(self.mu_J, self.sigma_J, M)
            ) - 1  # Size of each jump

            # Adjust asset price for jumps
            S[:, t] *= (1 + Jumps * JumpSizes)

        return S
