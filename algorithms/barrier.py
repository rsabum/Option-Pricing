from models import model
import numpy as np


def Barrier_Option(
    asset_model: model,
    initial_price: float,
    barrier: float,
    strike: float,
    period: int,
    num_simulations: int,
    num_timesteps: int,
    barrier_up: bool = True,
    knock_in: bool = True,
    call_option: bool = True,
    european_exercise: bool = True
):
    """
    Calculates the price of a Barrier option using Monte Carlo simulation.

    A Barrier option is a type of financial derivative where the payoff depends on whether the underlying asset's price reaches a certain barrier level. The option is activated or deactivated based on this barrier.

    Parameters:
    -----------
    asset_model : model
        An instance of the asset model used to simulate the price paths of the underlying asset.
    initial_price : float
        The initial price of the underlying asset.
    barrier : float
        The barrier price that activates or deactivates the option.
    strike : float
        The strike price of the option, which is the price at which the option can be exercised.
    period : int
        The time to maturity of the option, typically expressed in years.
    num_simulations : int
        The number of Monte Carlo simulations to perform for estimating the option price.
    num_timesteps : int
        The number of discrete time steps within each simulation path.
    barrier_up : bool, optional
        Specifies whether the barrier is an upper (True) or lower (False) barrier. Defaults to True.
    knock_in : bool, optional
        Specifies whether the option is a knock-in (True) or knock-out (False) option. Defaults to True.
    call_option : bool, optional
        Specifies whether the option is a call (True) or a put (False). Defaults to True.
    european_exercise : bool, optional
        Specifies whether the option is European-style (True) or American-style (False). Defaults to True.

    Returns:
    --------
    float
        The estimated price of the Barrier option based on the Monte Carlo simulations and the provided parameters.
    """


    # Define the exercise value function based on the type of option and knock-in/out feature.
    if knock_in:
        if call_option:
            # Knock-in call option: payoff is nonzero only if the barrier is hit
            exercise_value = lambda hit, price: max(price - strike, 0) if hit else 0
        else:
            # Knock-in put option: payoff is nonzero only if the barrier is hit
            exercise_value = lambda hit, price: max(strike - price, 0) if hit else 0
    else:
        if call_option:
            # Knock-out call option: payoff is zero if the barrier is hit
            exercise_value = lambda hit, price: 0 if hit else max(price - strike, 0)
        else:
            # Knock-out put option: payoff is zero if the barrier is hit
            exercise_value = lambda hit, price: 0 if hit else max(strike - price, 0)

    # Simulate the price paths of the underlying asset using the asset model.
    PRICE = asset_model.simulate(
        S0=initial_price,  # Initial asset price
        T=period,          # Time to maturity
        M=num_simulations, # Number of simulations
        N=num_timesteps    # Number of time steps
    )

    # Initialize an array to keep track of whether the barrier is hit in each simulation.
    HIT_BARRIER = np.zeros(shape=(num_simulations, num_timesteps + 1))

    # Determine if the barrier is hit in each simulation.
    if barrier_up:
        # For an upper barrier, check if the price is ever above the barrier.
        for i in range(num_simulations):
            HIT_BARRIER[i][0] = PRICE[i][0] >= barrier
            for t in range(1, num_timesteps + 1):
                HIT_BARRIER[i, t] = max(HIT_BARRIER[i][t - 1], PRICE[i][t] >= barrier)
    else:
        # For a lower barrier, check if the price is ever below the barrier.
        for i in range(num_simulations):
            HIT_BARRIER[i][0] = PRICE[i][0] <= barrier
            for t in range(1, num_timesteps + 1):
                HIT_BARRIER[i, t] = max(HIT_BARRIER[i][t - 1], PRICE[i][t] <= barrier)

    # Calculate the option value based on the exercise style.
    if european_exercise:
        VALUE = np.zeros(shape=(num_simulations))

        for i in range(num_simulations):
            # Calculate the payoff at maturity for each simulation
            VALUE[i] = exercise_value(HIT_BARRIER[i][-1], PRICE[i][-1])
        
        return np.mean(VALUE)  # Return the average payoff across all simulations
    
    else:
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    # At the last timestep, the value is the payoff
                    VALUE[i][t] = exercise_value(HIT_BARRIER[i][t], PRICE[i][t])
                else:
                    # Before the last timestep, compare the payoff to continuing
                    VALUE[i][t] = max(
                        exercise_value(HIT_BARRIER[i][t], PRICE[i][t]), 
                        VALUE[i][t + 1]
                    )
        
        return np.mean(VALUE[:, 0])  # Return the average initial payoff across all simulations
