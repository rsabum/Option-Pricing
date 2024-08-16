from models import model
import numpy as np


def Spread_Option(
    asset_model_1: model,
    asset_model_2: model,
    initial_price_1: float,
    initial_price_2: float,
    strike: float,
    periods: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    european_exercise: bool = True
):
    """
    Calculates the price of a Spread Option using Monte Carlo simulation.

    Parameters:
    -----------
    asset_model_1 : model
        The first asset model instance used for simulating the price path of the first underlying asset.
    asset_model_2 : model
        The second asset model instance used for simulating the price path of the second underlying asset.
    initial_price_1 : float
        The initial price of the first underlying asset.
    initial_price_2 : float
        The initial price of the second underlying asset.
    strike : float
        The strike price of the option.
    periods : int
        The time to maturity of the option, typically in years.
    num_simulations : int
        The number of Monte Carlo simulations to perform.
    num_timesteps : int
        The number of time steps within each simulation.
    call_option : bool, optional
        Specifies whether the option is a call (True) or a put (False). Defaults to True.
    european_exercise : bool, optional
        Specifies whether the option is European-style (True) or American-style (False). Defaults to True.

    Returns:
    --------
    Value : float
        The estimated price of the Spread Option based on the provided parameters.
    """
    
    if call_option:
        # For a call option, the payoff is the difference between the two asset prices minus the strike price.
        # The exercise value is the maximum of the difference and zero.
        exercise_value = lambda price_1, price_2: max((price_1 - price_2) - strike, 0)
    else:
        # For a put option, the payoff is the strike price minus the difference between the two asset prices.
        # The exercise value is the maximum of the result and zero.
        exercise_value = lambda price_1, price_2: max(strike - (price_1 - price_2), 0)

    # Simulate the price path for the first underlying asset.
    PRICE_1 = asset_model_1.simulate(
        S0=initial_price_1,  # Initial price of the first asset
        T=periods,           # Time to maturity
        M=num_simulations,   # Number of simulations
        N=num_timesteps      # Number of time steps
    )

    # Simulate the price path for the second underlying asset.
    PRICE_2 = asset_model_2.simulate(
        S0=initial_price_2,  # Initial price of the second asset
        T=periods,           # Time to maturity
        M=num_simulations,   # Number of simulations
        N=num_timesteps      # Number of time steps
    )

    if european_exercise:
        # For European-style options, the option can only be exercised at maturity.
        VALUE = np.zeros(shape=(num_simulations))
        
        # Calculate the payoff at maturity for each simulation.
        for i in range(num_simulations):
            VALUE[i] = exercise_value(PRICE_1[i][-1], PRICE_2[i][-1])  # Payoff based on the final prices of the assets
        
        return np.mean(VALUE)  # Return the average payoff across all simulations
    
    else:
        # For American-style options, the option can be exercised at any time before or at maturity.
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        
        # Calculate the option value using backward induction, allowing for early exercise.
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    VALUE[i][t] = exercise_value(PRICE_1[i][t], PRICE_2[i][t])  # At the last timestep, the value is the payoff
                else:
                    # Before the last timestep, compare the payoff to continuing
                    VALUE[i][t] = max(exercise_value(PRICE_1[i][t], PRICE_2[i][t]), VALUE[i][t + 1])
        
        return np.mean(VALUE[:, 0])  # Return the average initial payoff across all simulations
