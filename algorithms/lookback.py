from models import model
import numpy as np


def Fixed_Strike_Lookback_Option(
    asset_model: model,
    initial_price: float,
    strike: float,
    period: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    european_exercise: bool = True
):
    """
    Calculates the price of a Fixed-Strike Lookback option using Monte Carlo simulation.

    A Fixed-Strike Lookback option is a financial derivative that allows the holder to 
    exercise the option at the best price observed over the life of the option, with the 
    strike price fixed at the time of option issuance.

    Parameters:
    -----------
    asset_model : model
        An instance of the asset model used to simulate the price path of the underlying asset.
    initial_price : float
        The initial price of the underlying asset.
    strike : float
        The fixed strike price of the option, set at the time of issuance.
    period : int
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
        The estimated price of the Fixed-Strike Lookback option based on the Monte Carlo 
        simulations and the provided parameters.
    """


    # Simulate the price path for the underlying asset.
    PRICE = asset_model.simulate(
        S0=initial_price,  # Initial price of the asset
        T=period,          # Time to maturity
        M=num_simulations, # Number of simulations
        N=num_timesteps    # Number of time steps
    )

    # Initialize an array to track the running minimum or maximum of the asset's price.
    MIN_MAX = np.zeros(shape=(num_simulations, num_timesteps + 1))

    if call_option:
        # For a call option, the payoff is based on the maximum asset price during the option's life.
        # The exercise value is the maximum price minus the strike price, or zero if the strike is not exceeded.
        exercise_value = lambda maximum: max(maximum - strike, 0)
        
        # Calculate the running maximum for each simulation.
        for i in range(num_simulations):
            MIN_MAX[i][0] = PRICE[i][0]  # Initialize the first element to the initial price
            for t in range(1, num_timesteps + 1):
                MIN_MAX[i][t] = max(MIN_MAX[i][t - 1], PRICE[i][t])  # Update with the maximum price up to time t

    else:
        # For a put option, the payoff is based on the minimum asset price during the option's life.
        # The exercise value is the strike price minus the minimum price, or zero if the minimum is not below the strike.
        exercise_value = lambda minimum: max(strike - minimum, 0)
        
        # Calculate the running minimum for each simulation.
        for i in range(num_simulations):
            MIN_MAX[i][0] = PRICE[i][0]  # Initialize the first element to the initial price
            for t in range(1, num_timesteps + 1):
                MIN_MAX[i][t] = min(MIN_MAX[i][t - 1], PRICE[i][t])  # Update with the minimum price up to time t

    if european_exercise:
        # For European-style options, the option can only be exercised at maturity.
        VALUE = np.zeros(shape=(num_simulations))
        
        # Calculate the payoff at maturity for each simulation.
        for i in range(num_simulations):
            VALUE[i] = exercise_value(MIN_MAX[i][-1])  # Payoff is based on the final running max/min
        
        return np.mean(VALUE)  # Return the average payoff across all simulations
    
    else:
        # For American-style options, the option can be exercised at any time before or at maturity.
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        
        # Calculate the option value using backward induction, allowing for early exercise.
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    VALUE[i][t] = exercise_value(MIN_MAX[i][t])  # At the last timestep, the value is the payoff
                else:
                    # Before the last timestep, compare the payoff to continuing
                    VALUE[i][t] = max(exercise_value(MIN_MAX[i][t]), VALUE[i][t + 1])
        
        return np.mean(VALUE[:, 0])  # Return the average initial payoff across all simulations

    

def Floating_Strike_Lookback_Option(
    asset_model: model,
    initial_price: float,
    period: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    european_exercise: bool = True
):
    """
    Calculates the price of a Floating-Strike Lookback option using Monte Carlo simulation.

    A Floating-Strike Lookback option is a financial derivative that allows the holder to exercise 
    the option at the best price observed over the life of the option. The strike price is set based 
    on the minimum (for a call) or maximum (for a put) price observed during the option's lifetime.

    Parameters:
    -----------
    asset_model : model
        An instance of the asset model used to simulate the price path of the underlying asset.
    initial_price : float
        The initial price of the underlying asset.
    period : int
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
        The estimated price of the Floating-Strike Lookback option based on the Monte Carlo 
        simulations and the provided parameters.
    """


    # Simulate the price path for the underlying asset.
    PRICE = asset_model.simulate(
        S0=initial_price,  # Initial price of the asset
        T=period,          # Time to maturity
        M=num_simulations, # Number of simulations
        N=num_timesteps    # Number of time steps
    )

    # Initialize an array to track the running minimum or maximum of the asset's price.
    MIN_MAX = np.zeros(shape=(num_simulations, num_timesteps + 1))

    if call_option:
        # For a call option, the payoff is based on the difference between the maximum price and the asset price.
        # The exercise value is the maximum price minus the current price, or zero if the current price is not exceeded.
        exercise_value = lambda maximum, price: max(maximum - price, 0)
        
        # Calculate the running maximum for each simulation.
        for i in range(num_simulations):
            MIN_MAX[i][0] = PRICE[i][0]  # Initialize the first element to the initial price
            for t in range(1, num_timesteps + 1):
                MIN_MAX[i][t] = max(MIN_MAX[i][t - 1], PRICE[i][t])  # Update with the maximum price up to time t

    else:
        # For a put option, the payoff is based on the difference between the asset price and the minimum price.
        # The exercise value is the current price minus the minimum price, or zero if the minimum is not exceeded.
        exercise_value = lambda minimum, price: max(price - minimum, 0)
        
        # Calculate the running minimum for each simulation.
        for i in range(num_simulations):
            MIN_MAX[i][0] = PRICE[i][0]  # Initialize the first element to the initial price
            for t in range(1, num_timesteps + 1):
                MIN_MAX[i][t] = min(MIN_MAX[i][t - 1], PRICE[i][t])  # Update with the minimum price up to time t

    if european_exercise:
        # For European-style options, the option can only be exercised at maturity.
        VALUE = np.zeros(shape=(num_simulations))
        
        # Calculate the payoff at maturity for each simulation.
        for i in range(num_simulations):
            VALUE[i] = exercise_value(MIN_MAX[i][-1], PRICE[i][-1])  # Payoff is based on the final running max/min and final price
        
        return np.mean(VALUE)  # Return the average payoff across all simulations
    
    else:
        # For American-style options, the option can be exercised at any time before or at maturity.
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        
        # Calculate the option value using backward induction, allowing for early exercise.
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    VALUE[i][t] = exercise_value(MIN_MAX[i][t], PRICE[i][t])  # At the last timestep, the value is the payoff
                else:
                    # Before the last timestep, compare the payoff to continuing
                    VALUE[i][t] = max(exercise_value(MIN_MAX[i][t], PRICE[i][t]), VALUE[i][t + 1])
        
        return np.mean(VALUE[:, 0])  # Return the average initial payoff across all simulations
