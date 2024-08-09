from engines.vanilla import PriceVanillaEuropean, PriceVanillaAmerican
from models import StationaryModel
import numpy as np

# np.random.seed(42)

if __name__ == '__main__':

    print(PriceVanillaEuropean(
        asset_model=StationaryModel(mu=0.5, sigma=0.1),
        asset_price=100,
        strike=100,
        periods=1,
        num_simulations=1000,
        num_timesteps=252,
        option_type='call'

    ))

    print(PriceVanillaEuropean(
        asset_model=StationaryModel(mu=0.5, sigma=0.1),
        asset_price=100,
        strike=100,
        periods=1,
        num_simulations=1000,
        num_timesteps=252,
        option_type='put'

    ))