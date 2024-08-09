# Dynamic Programming for Exotic Option Pricing


# General Dynamic Programming Formulation
We assume that the present value of an option contract is recursively dependent on the expected future value of the option. Therefore, we employ the Bellman Equations to express the value of an option in terms of the expectation of fututre information. Let's first define the following:
- $t$ the current time step.
- $T$ expiry time step.
- $S_t$ the contract's underliying price at time $t$
- $K$ the strike price of our option.
- $C(S_t)$ is a call option's exercise value given its current price $S_t$.
- $P(S_t)$ is a put option's exercise value given its current price $S_t$.
- $V_C(S_t)$ is the call options expected value when its underlying asset is valued at $S_t$.
- $V_P(S_t)$ is the put options expected value when its underlying asset is valued at $S_t$.

### European Exercise
European style options only allow exercise at $t = T$, therefore we only need to consider expectation over all the terminal states calculating our option's value.

$$
\begin{align*}
V_C(S_t) &= \mathbb{E}\bigg[C(S_{T}) ~~\bigg\vert~~ S_t\bigg]
\\
V_P(S_t) &= \mathbb{E}\bigg[P(S_{T}) ~~\bigg\vert~~ S_t\bigg]
\end{align*}
$$


### American Exercise
American style options allow exercise at any $t \le T$. To account for this possiblity we must use backwards dynamic programming on possible price trajectories accounting for possible early exercise at each time step. This results in the following recurrence relations:

$$
V_C(S_t) = 
\begin{cases}
\begin{align*}
t = T &\implies C(S_t)
\\
t \lt T &\implies \max\bigg\lbrace C(S_t), ~~\mathbb{E}\bigg[V_C(S_{t + dt}) ~~\vert~~ S_t\bigg]\bigg\rbrace
\end{align*}
\end{cases}
$$

$$
V_P(S_t) = 
\begin{cases}
\begin{align*}
t = T &\implies P(S_t)
\\
t \lt T &\implies \max\bigg\lbrace P(S_t), ~~\mathbb{E}\bigg[V_P(S_{t + dt}) ~~\vert~~ S_t\bigg]\bigg\rbrace
\end{align*}
\end{cases}
$$

from this we can see that with all else being equal, the value of a European contract can never exceed that of an American Exercise contract. 

# Contract Specifics
Below we will give short explanations for each type of contract we will be considering as well as mathematically define their payoff functions.

## Asian Options
An Asian option's payoff depends on the arithmetic or geometric average price of the underlying asset over its lifetime, rather than the price at a specific point in time. Let $\mu(S_t)$ denote the running arithmetic or geometric average of our underlying up to time $t$:
$$
\begin{align*}
C(S_t) &= \max\bigg\lbrace{\mu(S_t) - K,~~ 0}\bigg\rbrace
\\\\
P(S_t) &= \max\bigg\lbrace{K - \mu(S_t),~~ 0}\bigg\rbrace
\end{align*}
$$

View in [algorithms/asian.py](algorithms/asian.py).

## Barrier Options
Barrier options are options where the payoff depends on whether the underlying asset's price breaches a certain predetermined barrier level $B$ during the option's life. We consider four types of barrier options, up-and-in, up-and-out, down-and-in, and down-and-out.
#### Up and In
The option is only activated if we breach the upper barrier during the lifetime of our option:
$$
\begin{align*}
C(S_t) &= 
\begin{cases}
\max(S_t - K, 0) ~~~~\text{ if } S_{i} \ge B \text{ for some } i \le t
\\
0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\text{otherwise}
\end{cases}
\\\\
P(S_t) &= 
\begin{cases}
\max(K - S_t, 0) ~~~~\text{ if } S_{i} \ge B \text{ for some } i \le t
\\
0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\text{otherwise}
\end{cases}
\end{align*}
$$

#### Up and Out
The option is remains active unless we breach the upper barrier at some point during its liftime after which it is deactivated:
$$
\begin{align*}
C(S_t) &= 
\begin{cases}
\max(S_t - K, 0) ~~~~\text{ if } S_{i} \lt B \text{ for all } i \le t
\\
0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\text{otherwise}
\end{cases}
\\\\
P(S_t) &= 
\begin{cases}
\max(K - S_t, 0) ~~~~\text{ if } S_{i} \lt B \text{ for all } i \le t
\\
0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\text{otherwise}
\end{cases}
\end{align*}
$$

#### Down and In
The option is only activated if we breach the lower barrier during the lifetime of our option:
$$
\begin{align*}
C(S_t) &= 
\begin{cases}
\max(S_t - K, 0) ~~~~\text{ if } S_{i} \le B \text{ for some } i \le t
\\
0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\text{otherwise}
\end{cases}
\\\\
P(S_t) &= 
\begin{cases}
\max(K - S_t, 0) ~~~~\text{ if } S_{i} \le B \text{ for some } i \le t
\\
0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\text{otherwise}
\end{cases}
\end{align*}
$$

#### Down and Out
The option is remains active unless we breach the lower barrier at some point during its liftime after which it is deactivated:
$$
\begin{align*}
C(S_t) &= 
\begin{cases}
\max(S_t - K, 0) ~~~~\text{ if } S_{i} \gt B \text{ for all } i \le t
\\
0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\text{otherwise}
\end{cases}
\\\\
P(S_t) &= 
\begin{cases}
\max(K - S_t, 0) ~~~~\text{ if } S_{i} \gt B \text{ for all } i \le t
\\
0 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\text{otherwise}
\end{cases}
\end{align*}
$$

View in [algorithms/barrier.py](algorithms/barrier.py).

## Basket Options
Basket options are options on a portfolio or basket of assets. The payoff depends on the weighted sum of the prices of the assets in the basket, rather than on a single asset. Let $\mathbf{w}$ and $\mathbf{S_t}$ be vectors denoting our asset weights and individual asset prices at time $t$ respectively. Our payoff functions are therefore:
$$
\begin{align*}
C(\mathbf{S_t}) &= \max\bigg\lbrace{\mathbf{w}\cdot\mathbf{S_t} - K,~~ 0}\bigg\rbrace
\\\\
P(\mathbf{S_t}) &= \max\bigg\lbrace{K - \mathbf{w}\cdot\mathbf{S_t},~~ 0}\bigg\rbrace
\end{align*}
$$
View in [algorithms/basket.py](algorithms/basket.py).

## Digital Options
Digital options pay a fixed amount if the underlying asset meets a certain condition at maturity.

#### Digitals
Digitals have a single strike $K$ and operate similarly to Vanilla Contracts however with a fixed payoff $Q$:
$$
\begin{align*}
C(S_t) &= 
\begin{cases}
Q ~~~~\text{ if } S_{t} \gt K
\\
0 ~~~~~~\text{otherwise}
\end{cases}
\\\\
P(S_t) &= 
\begin{cases}
Q ~~~~\text{ if } S_{t} \lt K
\\
0 ~~~~~~\text{otherwise}
\end{cases}
\end{align*}
$$

#### Double Digitals
Double Digitals involve two strike prices $K_1$ and $K_2$ and pays out $Q$ if our underlying's price falls between the two:
$$
C(S_t) = 
\begin{cases}
Q ~~~~\text{ if } K_1 \lt S_{t} \lt K_2
\\
0 ~~~~~~\text{otherwise}
\end{cases}
$$

View in [algorithms/digital.py](algorithms/digital.py).

## Lookback Options
Lookback options are exotic options where the payoff depends on the minimum or maximum price of the underlying asset during the option's life. We consider two types of lookback options, Fixed Strike and Floating Strike:

#### Fixed Strike
In this case the payoff is dependent on a predetermined strike price as well as the maximum or minimum underlying price over the option's lifetime:
$$
\begin{align*}
C(S_t) &= \max\bigg\lbrace{\max_{0 \le i \le t}(S_i) - K,~~ 0}\bigg\rbrace
\\\\
P(S_t) &= \max\bigg\lbrace{K - \min_{0 \le i \le t}(S_i),~~ 0}\bigg\rbrace
\end{align*}
$$

#### Floating Strike
In this case the payoff is dependent on the current underlying price and a varying strike equal to the maximum or minimum of the underlying price over the option's lifetime:
$$
\begin{align*}
C(S_t) &= \max\bigg\lbrace{S_t - \min_{0 \le i \le t}(S_i),~~ 0}\bigg\rbrace
\\\\
P(S_t) &= \max\bigg\lbrace{\max_{0 \le i \le t}(S_i) - S_t,~~ 0}\bigg\rbrace
\end{align*}
$$

View in [algorithms/lookback.py](algorithms/lookback.py).

## Spread Options
Spread options are options on the difference between the prices of two underlying assets. Given two assets $S^{(1)}$ and $S^{(2)}$ our payoff is calculated as follows:
$$
\begin{align*}
C(S_t) &= \max\bigg\lbrace{(S_t^{(1)} - S_t^{(2)}) - K,~~ 0}\bigg\rbrace
\\\\
P(S_t) &= \max\bigg\lbrace{K - (S_t^{(1)} - S_t^{(2)}),~~ 0}\bigg\rbrace
\end{align*}
$$
View in [algorithms/spread.py](algorithms/spread.py).


# Price Models
Below we describe the built in underlying price models.

### Stationary Model
The [Stationary Model](models/stationary.py) follows a Geometric Brownian Motion with constant drift and volatility:

$$ dS_t = \mu S_t ~ dt + \sigma S_t ~ dW $$ 

where $\mu$ is the drift rate, $\sigma$ is the volatility, and $dW$ is a Wiener processes increment.

### Stochastic Volatility Model
The [Stochastic Volatility (Heston) Model](models/stochastic_volatility.py) extends Geometric Brownian motion to incorporate a mean reverting stochastic volatility process:

$$ dS_t = \mu S_t ~ dt + \sqrt{V_t} S_t ~ dW_{S,t} $$

$$ dV_t = \kappa (\theta - V_t) ~ dt + \sigma \sqrt{V_t} ~ dW_{V,t} $$ 

where $V_t$ denotes the stochastic volatility process, $\mu$ is the asset's drift rate, $\kappa$ is the mean-reversion rate of volatility, $\theta$ is the long-term average volatility, $\sigma$ is the volatility of volatility, and $dW_{S,t}$ and $dW_{V,t}$ are $\rho$ correlated Wiener processes for the stock price and volatility, respectively.

### Jump Diffusion Model
The [Jump Diffusion Model](models/jump_diffusion.py) extends Geometric Brownian Motion to incorporate log normal jumps in the asset's price:

$$ dS_t = \mu S_t ~ dt + \sigma S_t ~ dW_t + S_t ~ dJ_t $$ 

where $\mu$ is the drift rate, $\sigma$ is the volatility, $dW_t$ is an increment of a Wiener processes, and $dJ_t$ is an increment of a Poisson process of intensity $\lambda_J$ and normally distributed sizes modeled by $\mu_J$ and $\sigma_J$.

### Stochastic Volatility Jump Model
The [Stochastic Volatility Jump (Bates) Model](models/stochastic_volatility_jump.py) combines the Heston Stochastic Volatility model with the Jump Diffusion model:

$$ dS_t = \mu S_t ~ dt + \sqrt{V_t} S_t ~ dW_{S,t} + S_t ~ dJ_t $$

$$ dV_t = \kappa (\theta - V_t) ~ dt + \sigma \sqrt{V_t} ~ dW_{V,t} $$ 

the parameter definitions follow naturally from the Stochastic Volatility and Jump Diffusion Models.

You can also use your own custom models by defining the `simulate(S0, T, M, N)` method where `S0` is the initial asset price, `T` is the number of periods to consider, `M` is the number of simultaneous simulations to run, and `N` is the number of timesteps in each simulation.