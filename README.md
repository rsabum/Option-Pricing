# Dynamic Programming for Theoretcial Option Pricing

In this project we approach theoretical option pricing as a dynamic programming problem in which at each time step we have information $s_t \in \mathcal{S}$ such as the underlying price, time till expiry, interest rates, etc. We also have a set of actions we can take at each time step $a \in \mathcal{A}$ such as early exercise, hedging adjustment, taking no action, etc. We also have functions defining the cost/reward of taking an action $C(s_t, a_t)$ and probabilty of transitioning from one state to another $P(s_{t + 1} ~|~ s_t, a_t)$ typically independent of $a_t$ and corresponds to price movements of the underlying. Our goal therefore is to find $V^*(s_t)$ which denotes the theoretical value of an option under the assumtion that the holder of the contract takes the most optional actions during the lifetime of the contract. By the Bellman Optimality Principle, $V^*(s_t)$ can be recursively defined as:

$$
\begin{equation*}
V^*(s_t) = 
    \max_{a_t \in \mathcal{A}} 
    \left\{
        C(s_t, a_t) + \int_{s_{t+1}} P(s_{t + 1} ~|~ s_t, a_t) V^*(s_{t + 1})  
    \right\}
\end{equation*}
$$


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




# Suported Contracts
In this section we go over the supported contracts as well as their respective dynamic programming formulations

## Vanilla Option

Given a strike price $K$ let our option's pay off, $C(S, t)$, after exercising at time $t$ is $\max\{S - K, 0\}$. Further more since this is an American call option, we can exercise at any time $t \ge 0$. Therefore at each time step we have the choice of exercising and recieving a payoff of $\max\{0, S - K\}$ or not exercising. If we dont exercise, our underlying stock and variance processes move to new values $S_{t + dt}$ and $V_{t + dt}$ and we have a new decision to make of whether or not we should exercise. This recursive relationship can be modeled as follows:

$$
\begin{align*}
V_0(S_t) &= \max\{S_t - K, 0\} \\
V_{t > 0}(S_t) &= \max\left\{ \max\{S_t - K, 0\}, \mathbb{E}\bigg[V_{t - dt}(S_{t + dt})\bigg]\right\}
\end{align*}
$$

and in the case of a put option:

$$
\begin{align*}
V_0(S_t) &= \max\{K - S_t, 0\} \\
V_{t > 0}(S_t) &= \max\left\{ \max\{K - S_t, 0\}, \mathbb{E}\bigg[V_{t - dt}(S_{t + dt})\bigg]\right\}
\end{align*}
$$
