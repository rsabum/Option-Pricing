from models import model
import numpy as np

def Price_Vanilla(
    asset_model: model,
    asset_price: float,
    strike: float,
    periods: int,
    num_simulations: int,
    num_timesteps: int,
    option_type: str,
    exercise_style: str,
    exercise_timesteps: set[int] = None
):
    
    if option_type == "call":
        exercise_value = lambda s: max(s - strike, 0)

    elif option_type == "put":
        exercise_value = lambda s: max(strike - s, 0)

    else:
        raise Exception("Invalid option type. Expected \"call\" or \"put\"")
    

    S = asset_model.simulate(
        S0=asset_price, 
        T=periods, 
        M=num_simulations, 
        N=num_timesteps
    )

    if exercise_style == "european":
        G = np.zeros(shape=(num_simulations))

        for i in range(num_simulations):
            G[i] = exercise_value(S[i][num_timesteps])

        return np.mean(G)
    
    elif exercise_style == "american":
        G = np.zeros(shape=(num_simulations, num_timesteps + 1))

        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    G[i][t] = exercise_value(S[i][t])
                
                else:
                    G[i][t] = max(exercise_value(S[i][t]), G[i][t + 1])

        return np.mean(G[:, 0])
    
    elif exercise_style == "bermudan":
        if not exercise_timesteps:
            raise Exception("Bermudan Exercise Option must be provided with a set of exercise times")
        
        G = np.zeros(shape=(num_simulations, num_timesteps + 1))

        for i in range(num_simulations):
            for t in reversed(range(num_timesteps + 1)):
                if t == num_timesteps:
                    G[i][t] = exercise_value(S[i][t])
                
                else:
                    if t in exercise_timesteps:
                        G[i][t] = max(exercise_value(S[i][t]), G[i][t + 1])

                    else:
                        G[i][t] = G[i][t + 1]

        return np.mean(G[:, 0])
    
    else:
        raise Exception("Invalid Option Exercise Style. Expectex \"european\", \"american\", or \"bermudan\"")