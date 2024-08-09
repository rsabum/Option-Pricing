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
    
    if call_option:
        exercise_value = lambda price_1, price_2: max((price_1 - price_2) - strike, 0)

    else:
        exercise_value = lambda price_1, price_2: max(strike - (price_1 - price_2), 0)


    PRICE_1 = asset_model_1.simulate(
        S0=initial_price_1, 
        T=periods, 
        M=num_simulations, 
        N=num_timesteps
    )

    PRICE_2 = asset_model_2.simulate(
        S0=initial_price_2, 
        T=periods, 
        M=num_simulations, 
        N=num_timesteps
    )

    if european_exercise:
        VALUE = np.zeros(shape=(num_simulations))

        for i in range(num_simulations):
            VALUE[i] = exercise_value(PRICE_1[i][-1], PRICE_2[i][-1])

        return np.mean(VALUE)
    
    else:
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))

        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    VALUE[i][t] = exercise_value(PRICE_1[i][t], PRICE_2[i][t])
                
                else:
                    VALUE[i][t] = max(exercise_value(PRICE_1[i][t], PRICE_2[i][t]), VALUE[i][t + 1])

        return np.mean(VALUE[:, 0])
    