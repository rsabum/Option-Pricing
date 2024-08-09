from models import model
import numpy as np


def Price_Asian_Option(
    asset_model: model,
    asset_price: float,
    strike: float,
    period: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    arithmetic_averaging: bool = True,
    european_exercise: bool = True
):
    
    if call_option:
        exercise_value = lambda mean: max(mean - strike, 0)

    else:
        exercise_value = lambda mean: max(strike - mean, 0)
    

    PRICE = asset_model.simulate(
        S0=asset_price, 
        T=period, 
        M=num_simulations, 
        N=num_timesteps
    )

    # calculating ruinning average of the asset's price
    MEAN = np.zeros(shape=(num_simulations, num_timesteps + 1))
    MEAN[:, 0] = PRICE[:, 0]

    if arithmetic_averaging:
        for t in range(1, num_timesteps + 1):
            MEAN[:, t] = (MEAN[:, t - 1] * t + PRICE[:, t]) / (t + 1)
    
    else:
        for t in range(1, num_timesteps + 1):
            MEAN[:, t] = (PRICE[:, t] * MEAN[:, t - 1] ** t) ** (1 / (t + 1))


    if european_exercise:
        VALUE = np.zeros(shape=(num_simulations))
        for i in range(num_simulations):
            VALUE[i] = exercise_value(MEAN[i][-1])

        return np.mean(VALUE)
    
    else:
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    VALUE[i][t] = exercise_value(MEAN[i][t])
                
                else:
                    VALUE[i][t] = max(exercise_value(MEAN[i][t]), VALUE[i][t + 1])

        return np.mean(VALUE[:, 0])