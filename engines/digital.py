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
    
    if call_option:
        exercise_value = lambda s: payoff if s > strike else 0

    else:
        exercise_value = lambda s: payoff if s < strike else 0


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
    
    if call_option:
        exercise_value = lambda s: s if s > strike else 0

    else:
        exercise_value = lambda s: s if s < strike else 0


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
    
    exercise_value = lambda s: payoff if lower_strike <= s <= upper_strike else 0

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
    
    exercise_value = lambda s: s if lower_strike <= s <= upper_strike else 0

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