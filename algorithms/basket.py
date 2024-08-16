from models import model
import numpy as np


def Basket_Option(
    asset_models: list[model],
    asset_weights: list[float],
    initial_prices: list[float],
    strike: float,
    periods: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    european_exercise: bool = True
):
    """
    Calculates the price of a Basket option using Monte Carlo simulation.

    A Basket option is a financial derivative where the payoff depends on the performance 
    of a portfolio of multiple underlying assets. The price of the option is determined by 
    the combined behavior of these assets.

    Parameters:
    -----------
    asset_models : list[model]
        A list of asset model instances used to simulate the price paths of the underlying assets.
    asset_weights : list[float]
        A list of weights for each asset in the basket. Each weight represents the proportion of the asset in the basket.
    initial_prices : list[float]
        A list of initial prices for each asset in the basket.
    strike : float
        The strike price of the option, which is the price at which the option can be exercised.
    periods : int
        The time to maturity of the option, typically expressed in years.
    num_simulations : int
        The number of Monte Carlo simulations to perform for estimating the option price.
    num_timesteps : int
        The number of discrete time steps within each simulation path.
    call_option : bool, optional
        Specifies whether the option is a call (True) or a put (False). Defaults to True.
    european_exercise : bool, optional
        Specifies whether the option is European-style (True) or American-style (False). Defaults to True.

    Returns:
    --------
    float
        The estimated price of the Basket option based on the Monte Carlo simulations and the provided parameters.
    """


    # Define the exercise value function based on the type of option (call or put).
    if call_option:
        # For a call option, the payoff is the maximum of (basket price - strike, 0)
        exercise_value = lambda s: max(s - strike, 0)
    else:
        # For a put option, the payoff is the maximum of (strike - basket price, 0)
        exercise_value = lambda s: max(strike - s, 0)

    # Simulate the price paths for each asset in the basket.
    PRICES = np.array([
        asset_models[i].simulate(
            S0=initial_prices[i],  # Initial price of the asset
            T=periods,             # Time to maturity
            M=num_simulations,     # Number of simulations
            N=num_timesteps        # Number of time steps
        ) for i in range(len(asset_models))
    ])

    # Calculate the basket price at each time step by applying the asset weights.
    # 'i,ijk->jk' einsum expression performs the weighted sum across assets and simulations.
    BASKET_PRICE = np.einsum('i,ijk->jk', asset_weights, PRICES)

    # Calculate the option value based on the exercise style.
    if european_exercise:
        # For European-style options, calculate the payoff at maturity for each simulation.
        VALUE = np.zeros(shape=(num_simulations))
        
        for i in range(num_simulations):
            VALUE[i] = exercise_value(BASKET_PRICE[i][-1])
        
        return np.mean(VALUE)  # Return the average payoff across all simulations
    
    else:
        # For American-style options, allow for early exercise.
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    # At the last timestep, the value is the payoff
                    VALUE[i][t] = exercise_value(BASKET_PRICE[i][t])
                else:
                    # Before the last timestep, compare the payoff to continuing
                    VALUE[i][t] = max(exercise_value(BASKET_PRICE[i][t]), VALUE[i][t + 1])
        
        return np.mean(VALUE[:, 0])  # Return the average initial payoff across all simulations
