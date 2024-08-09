# Supported Price Models

## Stationary Model
the Stationary Model follows a Geometric Brownian Motion with constant drift and volatility:

$$ 
dS_t = \mu S_t ~ dt + \sigma S_t ~ dW
$$ 

where $\mu$ is the drift rate, $\sigma$ is the volatility, and $dW$ is a Wiener processes increment.


## Stochastic Volatility Model
the Stochastic Volatility Model (Heston Model) extends Geometric Brownian motion to incorporate a mean reverting stochastic volatility process:

$$ 
\begin{align*}
dS_t &= \mu S_t ~ dt + \sqrt{V_t} S_t ~ dW_{S,t}
\\\\
dV_t &= \kappa (\theta - V_t) ~ dt + \sigma \sqrt{V_t} ~ dW_{V,t}
\end{align*}
$$ 

where $V_t$ denotes the stochastic volatility process, $\mu$ is the asset's drift rate, $\kappa$ is the mean-reversion rate of volatility, $\theta$ is the long-term average volatility, $\sigma$ is the volatility of volatility, and $dW_{S,t}$ and $dW_{V,t}$ are $\rho$ correlated Wiener processes for the stock price and volatility, respectively.

## Jump Diffusion Model
the Jump Diffusion Model extends Geometric Brownian Motion to incorporate log normal jumps in the asset's price:

$$ 
\begin{align*}
dS_t &= \mu S_t ~ dt + \sigma S_t ~ dW_t + S_t ~ dJ_t
\end{align*}
$$ 

where $\mu$ is the drift rate, $\sigma$ is the volatility, $dW_t$ is an increment of a Wiener processes, and $dJ_t$ is an increment of a Poisson process of intensity $\lambda_J$ and normally distributed sizes modeled by $\mu_J$ and $\sigma_J$.


## Stochastic Volatility Jump Model
the Stochastic Volatility Jump Model (Bates Model) combines the Heston Stochastic Volatility model with the Jump Diffusion model:

$$ 
\begin{align*}
dS_t &= \mu S_t ~ dt + \sqrt{V_t} S_t ~ dW_{S,t} + S_t ~ dJ_t
\\\\
dV_t &= \kappa (\theta - V_t) ~ dt + \sigma \sqrt{V_t} ~ dW_{V,t}
\end{align*}
$$ 
