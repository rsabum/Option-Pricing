from .stationary import StationaryModel
from .jump_diffusion import JumpDiffusionModel
from .stochastic_volatility import StochasticVolatilityModel
from .stochastic_volatility_jump import StochasticVolatilityJumpModel

from typing import Union
model = Union[
    StationaryModel,
    JumpDiffusionModel,
    StochasticVolatilityModel,
    StochasticVolatilityJumpModel
]