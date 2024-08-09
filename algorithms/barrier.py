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
    
    if knock_in:
        if call_option:
            exercise_value = lambda hit, price: max(price - strike, 0) if hit else 0

        else:
            exercise_value = lambda hit, price: max(strike - price, 0) if hit else 0

    else:
        if call_option:
            exercise_value = lambda hit, price: 0 if hit else max(price - strike, 0)

        else:
            exercise_value = lambda hit, price: 0 if hit else max(strike - price, 0)
    

    PRICE = asset_model.simulate(
        S0=initial_price, 
        T=period, 
        M=num_simulations, 
        N=num_timesteps
    )

    # calculating running maximum of the asset's price
    HIT_BARRIER = np.zeros(shape=(num_simulations, num_timesteps + 1))

    if barrier_up:
        for i in range(num_simulations):
            HIT_BARRIER[i][0] = PRICE[i][0] >= barrier
            for t in range(1, num_timesteps + 1):
                HIT_BARRIER[i, t] = max(HIT_BARRIER[i][t - 1], PRICE[i][t] >= barrier)

    else:
        for i in range(num_simulations):
            HIT_BARRIER[i][0] = PRICE[i][0] <= barrier
            for t in range(1, num_timesteps + 1):
                HIT_BARRIER[i, t] = max(HIT_BARRIER[i][t - 1], PRICE[i][t] <= barrier)


    if european_exercise:
        VALUE = np.zeros(shape=(num_simulations))
        for i in range(num_simulations):
            VALUE[i] = exercise_value(HIT_BARRIER[i][-1], PRICE[i][-1])

        return np.mean(VALUE)
    

    else:
        VALUE = np.zeros(shape=(num_simulations, num_timesteps + 1))
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    VALUE[i][t] = exercise_value(HIT_BARRIER[i][t], PRICE[i][t])
                
                else:
                    VALUE[i][t] = max(
                        exercise_value(HIT_BARRIER[i][t], PRICE[i][t]), 
                        VALUE[i][t + 1]
                    )

        return np.mean(VALUE[:, 0])