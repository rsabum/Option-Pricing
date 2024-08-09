from engines.basket import Price_Basket_Option
from models import StationaryModel
import numpy as np

# np.random.seed(42)

if __name__ == '__main__':

    print(Price_Basket_Option(
        asset_models=[StationaryModel(mu=0.15, sigma=0) for i in range(5)],
        asset_weights=[0.2 for i in range(5)],
        initial_prices=[100 for i in range(5)],
        strike=100,
        periods=1,
        num_simulations=100,
        num_timesteps=252
    ))