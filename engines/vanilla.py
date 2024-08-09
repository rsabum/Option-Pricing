from models import model
import numpy as np

def Price_Vanilla_Option(
    asset_model: model,
    initial_price: float,
    strike: float,
    periods: int,
    num_simulations: int,
    num_timesteps: int,
    call_option: bool = True,
    european_exercise: bool = True
):
    
    if call_option:
        exercise_value = lambda price: max(price - strike, 0)

    else:
        exercise_value = lambda price: max(strike - price, 0)


    PRICE = asset_model.simulate(
        S0=initial_price, 
        T=periods, 
        M=num_simulations, 
        N=num_timesteps
    )

    if european_exercise:
        VALUE = np.zeros(shape=(num_simulations))

        for i in range(num_simulations):
            VALUE[i] = exercise_value(PRICE[i][-1])

        return np.mean(VALUE)
    
    else:
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))

        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    VALUE[i][t] = exercise_value(PRICE[i][t])
                
                else:
                    VALUE[i][t] = max(exercise_value(PRICE[i][t]), VALUE[i][t + 1])

        return np.mean(VALUE[:, 0])
    