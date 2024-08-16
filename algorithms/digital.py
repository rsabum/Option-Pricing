from models import model
import numpy as np


def Cash_Digital_Option(
    asset_model: model,
    initial_price: float,
    strike: float,
    payoff: float,
    periods: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    european_exercise: bool = True
):
    """
    Calculates the price of a Cash-or-Nothing digital option using Monte Carlo simulation.

    A Cash-or-Nothing digital option is a financial derivative that provides a fixed cash payoff if the option is in-the-money at maturity, regardless of the magnitude by which it is in-the-money.

    Parameters:
    -----------
    asset_model : model
        An instance of the asset model used to simulate the price path of the underlying asset.
    initial_price : float
        The initial price of the underlying asset.
    strike : float
        The strike price of the option, which determines if the option is in-the-money.
    payoff : float
        The fixed cash payoff received if the option is exercised and is in-the-money.
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
        The estimated price of the Cash-or-Nothing digital option based on the Monte Carlo simulations and the provided parameters.
    """

    # Define the exercise value function based on the type of option (call or put).
    if call_option:
        # For a call option, the payoff is received if the asset price exceeds the strike price
        exercise_value = lambda s: payoff if s > strike else 0
    else:
        # For a put option, the payoff is received if the asset price is below the strike price
        exercise_value = lambda s: payoff if s < strike else 0

    # Simulate the price path for the underlying asset.
    PRICE = asset_model.simulate(
        S0=initial_price,   # Initial price of the asset
        T=periods,          # Time to maturity
        M=num_simulations,  # Number of simulations
        N=num_timesteps     # Number of time steps
    )

    # Calculate the option value based on the exercise style.
    if european_exercise:
        # For European-style options, calculate the payoff at maturity for each simulation.
        VALUE = np.zeros(shape=(num_simulations))
        
        for i in range(num_simulations):
            VALUE[i] = exercise_value(PRICE[i][-1])
        
        return np.mean(VALUE)  # Return the average payoff across all simulations
    
    else:
        # For American-style options, allow for early exercise.
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    # At the last timestep, the value is the payoff
                    VALUE[i][t] = exercise_value(PRICE[i][t])
                else:
                    # Before the last timestep, compare the payoff to continuing
                    VALUE[i][t] = max(exercise_value(PRICE[i][t]), VALUE[i][t + 1])
        
        return np.mean(VALUE[:, 0])  # Return the average initial payoff across all simulations

    

def Asset_Digital_Option(
    asset_model: model,
    initial_price: float,
    strike: float,
    periods: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    european_exercise: bool = True
):
    """
    Calculates the price of an Asset-or-Nothing digital option using Monte Carlo simulation.

    An Asset-or-Nothing digital option is a financial derivative that provides the value of the underlying asset if the option is in-the-money at maturity. If the option is out-of-the-money, the payoff is zero.

    Parameters:
    -----------
    asset_model : model
        An instance of the asset model used to simulate the price path of the underlying asset.
    initial_price : float
        The initial price of the underlying asset.
    strike : float
        The strike price of the option, which determines if the option is in-the-money.
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
        The estimated price of the Asset-or-Nothing digital option based on the Monte Carlo simulations and the provided parameters.
    """


    # Define the exercise value function based on the type of option (call or put).
    if call_option:
        # For a call option, the payoff is the asset price if it exceeds the strike price
        exercise_value = lambda s: s if s > strike else 0
    else:
        # For a put option, the payoff is the asset price if it is below the strike price
        exercise_value = lambda s: s if s < strike else 0

    # Simulate the price path for the underlying asset.
    PRICE = asset_model.simulate(
        S0=initial_price,   # Initial price of the asset
        T=periods,          # Time to maturity
        M=num_simulations,  # Number of simulations
        N=num_timesteps     # Number of time steps
    )

    # Calculate the option value based on the exercise style.
    if european_exercise:
        # For European-style options, calculate the payoff at maturity for each simulation.
        VALUE = np.zeros(shape=(num_simulations))
        
        for i in range(num_simulations):
            VALUE[i] = exercise_value(PRICE[i][-1])
        
        return np.mean(VALUE)  # Return the average payoff across all simulations
    
    else:
        # For American-style options, allow for early exercise.
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    # At the last timestep, the value is the payoff
                    VALUE[i][t] = exercise_value(PRICE[i][t])
                else:
                    # Before the last timestep, compare the payoff to continuing
                    VALUE[i][t] = max(exercise_value(PRICE[i][t]), VALUE[i][t + 1])
        
        return np.mean(VALUE[:, 0])  # Return the average initial payoff across all simulations

    

def Cash_Double_Digital_Option(
    asset_model: model,
    initial_price: float,
    lower_strike: float,
    upper_strike: float,
    payoff: float,
    periods: int,
    num_simulations: int,
    num_timesteps: int,
    european_exercise: bool = True
):
    """
    Calculates the price of a Cash-or-Nothing Double Digital option using Monte Carlo simulation.

    A Cash-or-Nothing Double Digital option is a financial derivative that pays a fixed amount if the underlying asset's price at maturity is within a specified range defined by two strike prices. If the asset's price is outside this range, the payoff is zero.

    Parameters:
    -----------
    asset_model : model
        An instance of the asset model used to simulate the price path of the underlying asset.
    initial_price : float
        The initial price of the underlying asset.
    lower_strike : float
        The lower strike price of the option, defining the lower bound of the payoff range.
    upper_strike : float
        The upper strike price of the option, defining the upper bound of the payoff range.
    payoff : float
        The fixed payoff received if the asset price at maturity is between the lower and upper strike prices.
    periods : int
        The time to maturity of the option, typically expressed in years.
    num_simulations : int
        The number of Monte Carlo simulations to perform for estimating the option price.
    num_timesteps : int
        The number of discrete time steps within each simulation path.
    european_exercise : bool, optional
        Specifies whether the option is European-style (True) or American-style (False). Defaults to True.

    Returns:
    --------
    float
        The estimated price of the Cash-or-Nothing Double Digital option based on the Monte Carlo simulations and the provided parameters.
    """


    # Define the exercise value function for the double digital option.
    # The payoff is received if the asset price is between the lower and upper strike prices.
    exercise_value = lambda s: payoff if lower_strike <= s <= upper_strike else 0

    # Simulate the price path for the underlying asset.
    PRICE = asset_model.simulate(
        S0=initial_price,   # Initial price of the asset
        T=periods,          # Time to maturity
        M=num_simulations,  # Number of simulations
        N=num_timesteps     # Number of time steps
    )

    # Calculate the option value based on the exercise style.
    if european_exercise:
        # For European-style options, calculate the payoff at maturity for each simulation.
        VALUE = np.zeros(shape=(num_simulations))
        
        for i in range(num_simulations):
            VALUE[i] = exercise_value(PRICE[i][-1])
        
        return np.mean(VALUE)  # Return the average payoff across all simulations
    
    else:
        # For American-style options, allow for early exercise.
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    # At the last timestep, the value is the payoff
                    VALUE[i][t] = exercise_value(PRICE[i][t])
                else:
                    # Before the last timestep, compare the payoff to continuing
                    VALUE[i][t] = max(exercise_value(PRICE[i][t]), VALUE[i][t + 1])
        
        return np.mean(VALUE[:, 0])  # Return the average initial payoff across all simulations

    

def Asset_Double_Digital_Option(
    asset_model: model,
    initial_price: float,
    lower_strike: float,
    upper_strike: float,
    periods: int,
    num_simulations: int,
    num_timesteps: int,
    european_exercise: bool = True
):
    """
    Calculates the price of an Asset-or-Nothing Double Digital option using Monte Carlo simulation.

    An Asset-or-Nothing Double Digital option is a financial derivative that pays the value of the underlying asset if its price at maturity is within a specified range defined by two strike prices. If the asset's price is outside this range, the payoff is zero.

    Parameters:
    -----------
    asset_model : model
        An instance of the asset model used to simulate the price path of the underlying asset.
    initial_price : float
        The initial price of the underlying asset.
    lower_strike : float
        The lower strike price of the option, defining the lower bound of the payoff range.
    upper_strike : float
        The upper strike price of the option, defining the upper bound of the payoff range.
    periods : int
        The time to maturity of the option, typically expressed in years.
    num_simulations : int
        The number of Monte Carlo simulations to perform for estimating the option price.
    num_timesteps : int
        The number of discrete time steps within each simulation path.
    european_exercise : bool, optional
        Specifies whether the option is European-style (True) or American-style (False). Defaults to True.

    Returns:
    --------
    float
        The estimated price of the Asset-or-Nothing Double Digital option based on the Monte Carlo simulations and the provided parameters.
    """


    # Define the exercise value function for the double digital option.
    # The payoff is the asset price if it is between the lower and upper strike prices.
    exercise_value = lambda s: s if lower_strike <= s <= upper_strike else 0

    # Simulate the price path for the underlying asset.
    PRICE = asset_model.simulate(
        S0=initial_price,   # Initial price of the asset
        T=periods,          # Time to maturity
        M=num_simulations,  # Number of simulations
        N=num_timesteps     # Number of time steps
    )

    # Calculate the option value based on the exercise style.
    if european_exercise:
        # For European-style options, calculate the payoff at maturity for each simulation.
        VALUE = np.zeros(shape=(num_simulations))
        
        for i in range(num_simulations):
            VALUE[i] = exercise_value(PRICE[i][-1])
        
        return np.mean(VALUE)  # Return the average payoff across all simulations
    
    else:
        # For American-style options, allow for early exercise.
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    # At the last timestep, the value is the payoff
                    VALUE[i][t] = exercise_value(PRICE[i][t])
                else:
                    # Before the last timestep, compare the payoff to continuing
                    VALUE[i][t] = max(exercise_value(PRICE[i][t]), VALUE[i][t + 1])
        
        return np.mean(VALUE[:, 0])  # Return the average initial payoff across all simulations
