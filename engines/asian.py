from models import model
import numpy as np


def Price_Asian_Option(
    asset_model: model,
    asset_price: float,
    strike: float,
    period: int,
    num_simulations: int,
    num_timesteps: int,
    option_style: str,
    averaging_style: str,
    exercise_style: str
):
    
    if option_style == "call":
        exercise_value = lambda mean: max(mean - strike, 0)

    elif option_style == "put":
        exercise_value = lambda mean: max(strike - mean, 0)

    else:
        raise Exception("Invalid option type. Expected \"call\" or \"put\"")
    

    PRICE = asset_model.simulate(
        S0=asset_price, 
        T=period, 
        M=num_simulations, 
        N=num_timesteps
    )

    # calculating ruinning mean of price
    MEAN = np.zeros(shape=(num_simulations, num_timesteps + 1))
    MEAN[:, 0] = PRICE[:, 0]

    if averaging_style == "geometric":
        for t in range(1, num_timesteps + 1):
            MEAN[:, t] = (PRICE[:, t] * MEAN[:, t - 1] ** t) ** (1 / (t + 1))

    elif averaging_style == "arithmetic":
        for t in range(1, num_timesteps + 1):
            MEAN[:, t] = (MEAN[:, t - 1] * t + PRICE[:, t]) / (t + 1)

    else:
        raise Exception("Invalid Asian Option Averaging Style. Expected \"arithmetic\" or \"geometric\"")


    if exercise_style == "european":
        G = np.zeros(shape=(num_simulations))
        for i in range(num_simulations):
            G[i] = exercise_value(MEAN[i][-1])

        return np.mean(G)
    

    if exercise_style == "american":
        G = np.zeros(shape=(num_simulations, num_timesteps + 1))
        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    G[i][t] = exercise_value(MEAN[i][t])
                
                else:
                    G[i][t] = max(exercise_value(MEAN[i][t]), G[i][t + 1])

        return np.mean(G[:, 0])
    
    
    raise Exception("Invalid Option Exercise Style. Expected \"european\" or \"american\"")