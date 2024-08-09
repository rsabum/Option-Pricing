from models import model
import numpy as np

def Fixed_Lookback_Option(
    asset_model: model,
    initial_price: float,
    strike: float,
    period: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    european_exercise: bool = True
):
    
    PRICE = asset_model.simulate(
        S0=initial_price, 
        T=period, 
        M=num_simulations, 
        N=num_timesteps
    )

    # calculating ruinning minimum or maximum of the asset's price
    MIN_MAX = np.zeros(shape=(num_simulations, num_timesteps + 1))

    if call_option:
        exercise_value = lambda maximum: max(maximum - strike, 0)
        for i in range(num_simulations):
            MIN_MAX[i][0] = PRICE[0]
            for t in range(1, num_timesteps + 1):
                MIN_MAX[i][t] = max(MIN_MAX[i][t - 1], PRICE[i][t])

    else:
        exercise_value = lambda minimum: max(strike - minimum, 0)
        for i in range(num_simulations):
            MIN_MAX[i][0] = PRICE[0]
            for t in range(1, num_timesteps + 1):
                MIN_MAX[i][t] = min(MIN_MAX[i][t - 1], PRICE[i][t])


    if european_exercise:
        VALUE = np.zeros(shape=(num_simulations))
        for i in range(num_simulations):
            VALUE[i] = exercise_value(MIN_MAX[i][-1])

        return np.mean(VALUE)
    
    else:
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    VALUE[i][t] = exercise_value(MIN_MAX[i][t])
                
                else:
                    VALUE[i][t] = max(exercise_value(MIN_MAX[i][t]), VALUE[i][t + 1])

        return np.mean(VALUE[:, 0])
    

def Floating_Lookback_Option(
    asset_model: model,
    initial_price: float,
    period: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    european_exercise: bool = True
):
    
    PRICE = asset_model.simulate(
        S0=initial_price, 
        T=period, 
        M=num_simulations, 
        N=num_timesteps
    )

    # calculating ruinning minimum or maximum of the asset's price
    MIN_MAX = np.zeros(shape=(num_simulations, num_timesteps + 1))

    if call_option:
        exercise_value = lambda maximum, price: max(maximum - price, 0)
        for i in range(num_simulations):
            MIN_MAX[i][0] = PRICE[0]
            for t in range(1, num_timesteps + 1):
                MIN_MAX[i][t] = max(MIN_MAX[i][t - 1], PRICE[i][t])

    else:
        exercise_value = lambda minimum, price: max(price - minimum, 0)
        for i in range(num_simulations):
            MIN_MAX[i][0] = PRICE[0]
            for t in range(1, num_timesteps + 1):
                MIN_MAX[i][t] = min(MIN_MAX[i][t - 1], PRICE[i][t])


    if european_exercise:
        VALUE = np.zeros(shape=(num_simulations))
        for i in range(num_simulations):
            VALUE[i] = exercise_value(MIN_MAX[i][-1], PRICE[i][-1])

        return np.mean(VALUE)
    
    else:
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    VALUE[i][t] = exercise_value(MIN_MAX[i][t], PRICE[i][t])
                
                else:
                    VALUE[i][t] = max(exercise_value(MIN_MAX[i][t], PRICE[i][t]), VALUE[i][t + 1])

        return np.mean(VALUE[:, 0])