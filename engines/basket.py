from models import model
import numpy as np

def Price_Basket_Option(
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
    
    if call_option:
        exercise_value = lambda s: max(s - strike, 0)

    else:
        exercise_value = lambda s: max(strike - s, 0)


    PRICES = np.array([
            asset_models[i].simulate(
            S0=initial_prices[i], 
            T=periods, 
            M=num_simulations, 
            N=num_timesteps
        ) for i in range(len(asset_models))
    ])

    BASKET_PRICE = np.einsum('i,ijk->jk', asset_weights, PRICES)

    if european_exercise:
        VALUE = np.zeros(shape=(num_simulations))

        for i in range(num_simulations):
            VALUE[i] = exercise_value(BASKET_PRICE[i][-1])

        return np.mean(VALUE)
    
    else:
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))

        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    VALUE[i][t] = exercise_value(BASKET_PRICE[i][t])
                
                else:
                    VALUE[i][t] = max(exercise_value(BASKET_PRICE[i][t]), VALUE[i][t + 1])

        return np.mean(VALUE[:, 0])
    