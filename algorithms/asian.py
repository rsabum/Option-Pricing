from models import model
import numpy as np


def Asian_Option(
    asset_model: model,
    initial_price: float,
    strike: float,
    period: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    arithmetic_averaging: bool = True,
    european_exercise: bool = True
):
    """
    Calculates the price of an Asian option using Monte Carlo simulation.

    An Asian option is a type of financial derivative where the payoff is based on the 
    average price of the underlying asset over a specified period.

    Parameters:
    -----------
    asset_model : model
        An instance of the asset model used to simulate the price paths of the underlying asset.
    initial_price : float
        The initial price of the underlying asset.
    strike : float
        The strike price of the option, which is the price at which the option can be exercised.
    period : int
        The time to maturity of the option, typically expressed in years.
    num_simulations : int
        The number of Monte Carlo simulations to perform for estimating the option price.
    num_timesteps : int
        The number of discrete time steps within each simulation path.
    call_option : bool, optional
        Specifies whether the option is a call (True) or a put (False). Defaults to True.
    arithmetic_averaging : bool, optional
        Specifies whether to use arithmetic (True) or geometric (False) averaging of the asset prices. Defaults to True.
    european_exercise : bool, optional
        Specifies whether the option is European-style (True) or American-style (False). Defaults to True.

    Returns:
    --------
    float
        The estimated price of the Asian option based on the Monte Carlo simulations and the provided parameters.
    """

    # Define the exercise value function based on the type of option (call or put).
    if call_option:
        exercise_value = lambda mean: max(mean - strike, 0)
    else:
        exercise_value = lambda mean: max(strike - mean, 0)

    # Simulate the price paths of the underlying asset using the asset model.
    PRICE = asset_model.simulate(
        S0=initial_price,  # Initial asset price
        T=period,          # Time to maturity
        M=num_simulations, # Number of simulations
        N=num_timesteps    # Number of time steps
    )

    # Initialize an array to store the running average of the asset's price.
    MEAN = np.zeros(shape=(num_simulations, num_timesteps + 1))
    MEAN[:, 0] = PRICE[:, 0]  # Set the initial price for each simulation

    # Calculate the running average of the asset's price.
    if arithmetic_averaging:
        # Use arithmetic averaging
        for t in range(1, num_timesteps + 1):
            MEAN[:, t] = (MEAN[:, t - 1] * t + PRICE[:, t]) / (t + 1)
    else:
        # Use geometric averaging
        for t in range(1, num_timesteps + 1):
            MEAN[:, t] = (PRICE[:, t] * MEAN[:, t - 1] ** t) ** (1 / (t + 1))

    # Calculate the option value based on the exercise style.
    if european_exercise:
        # European-style option: only the final average price matters
        VALUE = np.zeros(shape=(num_simulations))
        
        for i in range(num_simulations):
            VALUE[i] = exercise_value(MEAN[i][-1])  # Payoff at maturity

        return np.mean(VALUE)  # Return the average payoff across all simulations
    
    else:
        # American-style option: allow for early exercise
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))

        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    # At the last timestep, the value is the payoff
                    VALUE[i][t] = exercise_value(MEAN[i][t])
                else:
                    # Before the last timestep, compare the payoff to continuing
                    VALUE[i][t] = max(exercise_value(MEAN[i][t]), VALUE[i][t + 1])

        return np.mean(VALUE[:, 0])  # Return the average initial payoff across all simulations
