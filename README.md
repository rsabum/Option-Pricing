## Exotic Option Pricing
In the realm of financial derivatives, exotic options present distinctive features beyond those of vanilla options. While standard options offer straightforward payoffs based on the price of a single asset, exotic options incorporate complex structures to capitalize on unique market conditions. In this project we approximate the value of various exotic options, leveraging Monte Carlo simulation and Backward Dynamic Programming.

## Dynamic Programming Formulation
We assume that the present value of an option contract is recursively dependent on the expected future value of the option. Therefore, we employ the Bellman Equations to express the value of an option in terms of the expectation of fututre information. 

#### European Exercise
European style options only allow exercise at $t = T$, therefore we only need to consider expectation over all the terminal states calculating our option's value.

$$
\begin{align*}
V_C(S_t) &= \mathbb{E}\bigg[C(S_{T}) ~~\bigg\vert~~ S_t\bigg]
\\
V_P(S_t) &= \mathbb{E}\bigg[P(S_{T}) ~~\bigg\vert~~ S_t\bigg]
\end{align*}
$$


#### American Exercise
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

where
- $t$ the current time step.
- $T$ expiry time step.
- $S_t$ the contract's underliying price at time $t$
- $C(S_t)$ is a call option's exercise value given its current price $S_t$.
- $P(S_t)$ is a put option's exercise value given its current price $S_t$.
- $V_C(S_t)$ is the call options expected value when its underlying asset is valued at $S_t$.
- $V_P(S_t)$ is the put options expected value when its underlying asset is valued at $S_t$.


## Contracts Considered

### [Asians](algorithms/asian.py) (Geometric and Arithmetic Averaging)
An Asian option's payoff is determined by the arithmetic or geometric average price of the underlying asset over its duration, rather than its price at a particular moment. Let $\mu(S_t)$ represent the running arithmetic or geometric average of the underlying asset up to time $t$:
$$
\begin{align*}
C(S_t) &= \max\left\{\mu(S_t) - K,~~ 0\right\} \\
P(S_t) &= \max\left\{K - \mu(S_t),~~ 0\right\}
\end{align*}
$$




### [Barriers](algorithms/barrier.py) (Up-and-In, Up-and-Out, Down-and-In, Down-and-Out)

Barrier options have payoffs that depend on whether the underlying asset's price crosses a predetermined barrier level $B$.

#### Up-and-In
Activated only if the price breaches the upper barrier:
$$
\begin{align*}
C(S_t) &= 
\begin{cases}
\max(S_t - K, 0) & \text{if } \exists i \le t \text{ such that } S_{i} \ge B \\
0 & \text{otherwise}
\end{cases} \\
P(S_t) &= 
\begin{cases}
\max(K - S_t, 0) & \text{if } \exists i \le t \text{ such that } S_{i} \ge B \\
0 & \text{otherwise}
\end{cases}
\end{align*}
$$

#### Up-and-Out
Active unless the price breaches the upper barrier:
$$
\begin{align*}
C(S_t) &= 
\begin{cases}
\max(S_t - K, 0) & \text{if } \forall i \le t, S_{i} < B \\
0 & \text{otherwise}
\end{cases} \\
P(S_t) &= 
\begin{cases}
\max(K - S_t, 0) & \text{if } \forall i \le t, S_{i} < B \\
0 & \text{otherwise}
\end{cases}
\end{align*}
$$

#### Down-and-In
Activated only if the price breaches the lower barrier:
$$
\begin{align*}
C(S_t) &= 
\begin{cases}
\max(S_t - K, 0) & \text{if } \exists i \le t \text{ such that } S_{i} \le B \\
0 & \text{otherwise}
\end{cases} \\
P(S_t) &= 
\begin{cases}
\max(K - S_t, 0) & \text{if } \exists i \le t \text{ such that } S_{i} \le B \\
0 & \text{otherwise}
\end{cases}
\end{align*}
$$

#### Down-and-Out
Active unless the price breaches the lower barrier:
$$
\begin{align*}
C(S_t) &= 
\begin{cases}
\max(S_t - K, 0) & \text{if } \forall i \le t, S_{i} > B \\
0 & \text{otherwise}
\end{cases} \\
P(S_t) &= 
\begin{cases}
\max(K - S_t, 0) & \text{if } \forall i \le t, S_{i} > B \\
0 & \text{otherwise}
\end{cases}
\end{align*}
$$



### [Digitals](algorithms/digital.py) (Cash, Asset, Cash Double, Asset Double)

Digital options provide a fixed payoff if the underlying asset meets a specified condition at maturity.

#### Cash Digitals
Cash Digitals have a single strike $K$ and pay a fixed amount $Q$:
$$
\begin{align*}
C(S_t) &= 
\begin{cases}
Q & \text{if } S_{t} > K \\
0 & \text{otherwise}
\end{cases} \\
P(S_t) &= 
\begin{cases}
Q & \text{if } S_{t} < K \\
0 & \text{otherwise}
\end{cases}
\end{align*}
$$

#### Asset Digitals
Asset Digitals have a similar structure but the payoff is based on the asset price rather than a cash amount. 

#### Double Cash Digitals
Double Cash Digitals use two strike prices, $K_1$ and $K_2$, and pay out $Q$ if the underlying price is between these strikes:
$$
C(S_t) = 
\begin{cases}
Q & \text{if } K_1 < S_{t} < K_2 \\
0 & \text{otherwise}
\end{cases}
$$

#### Double Asset Digitals
Double Asset Digitals have a similar payoff structure but based on the asset price.


### [Lookbacks](algorithms/lookback.py) (Fixed Strike and Floating Strike)

Lookback options are exotic options where the payoff depends on the best observed price of the underlying asset over the option's lifetime.

#### Fixed Strike
The payoff depends on a predetermined strike price and the maximum or minimum price of the underlying asset:
$$
\begin{align*}
C(S_t) &= \max\left\{\max_{0 \le i \le t}(S_i) - K,~~ 0\right\} \\
P(S_t) &= \max\left\{K - \min_{0 \le i \le t}(S_i),~~ 0\right\}
\end{align*}
$$

#### Floating Strike
The payoff is based on the current underlying price and the maximum or minimum price observed during the option's lifetime:
$$
\begin{align*}
C(S_t) &= \max\left\{S_t - \min_{0 \le i \le t}(S_i),~~ 0\right\} \\
P(S_t) &= \max\left\{\max_{0 \le i \le t}(S_i) - S_t,~~ 0\right\}
\end{align*}
$$


### [Baskets](algorithms/basket.py)

Basket options are based on a portfolio of assets. The payoff depends on the weighted sum of the asset prices, rather than a single asset. Let $\mathbf{w}$ and $\mathbf{S_t}$ denote the asset weights and individual asset prices at time $t$, respectively. The payoff functions are:

$$
\begin{align*}
C(\mathbf{S_t}) &= \max\left\{\mathbf{w} \cdot \mathbf{S_t} - K,~~ 0\right\} \\
P(\mathbf{S_t}) &= \max\left\{K - \mathbf{w} \cdot \mathbf{S_t},~~ 0\right\}
\end{align*}
$$


### [Spreads](algorithms/spread.py)

Spread options are designed to profit from the difference between the prices of two underlying assets. For two assets, $S^{(1)}$ and $S^{(2)}$, the payoff is determined as follows:

$$
\begin{align*}
C(S_t) &= \max\left\{(S_t^{(1)} - S_t^{(2)}) - K,~~ 0\right\} \\
P(S_t) &= \max\left\{K - (S_t^{(1)} - S_t^{(2)}),~~ 0\right\}
\end{align*}
$$



<!-- 
# Price Models
Below we describe the built in underlying price models.

#### Stationary Model
The [Stationary Model](models/stationary.py) follows a Geometric Brownian Motion with constant drift and volatility:

$$ dS_t = \mu S_t ~ dt + \sigma S_t ~ dW $$ 

where $\mu$ is the drift rate, $\sigma$ is the volatility, and $dW$ is a Wiener processes increment.

#### Stochastic Volatility Model
The [Stochastic Volatility (Heston) Model](models/stochastic_volatility.py) extends Geometric Brownian motion to incorporate a mean reverting stochastic volatility process:

$$ dS_t = \mu S_t ~ dt + \sqrt{V_t} S_t ~ dW_{S,t} $$

$$ dV_t = \kappa (\theta - V_t) ~ dt + \sigma \sqrt{V_t} ~ dW_{V,t} $$ 

where $V_t$ denotes the stochastic volatility process, $\mu$ is the asset's drift rate, $\kappa$ is the mean-reversion rate of volatility, $\theta$ is the long-term average volatility, $\sigma$ is the volatility of volatility, and $dW_{S,t}$ and $dW_{V,t}$ are $\rho$ correlated Wiener processes for the stock price and volatility, respectively.

#### Jump Diffusion Model
The [Jump Diffusion Model](models/jump_diffusion.py) extends Geometric Brownian Motion to incorporate log normal jumps in the asset's price:

$$ dS_t = \mu S_t ~ dt + \sigma S_t ~ dW_t + S_t ~ dJ_t $$ 

where $\mu$ is the drift rate, $\sigma$ is the volatility, $dW_t$ is an increment of a Wiener processes, and $dJ_t$ is an increment of a Poisson process of intensity $\lambda_J$ and normally distributed sizes modeled by $\mu_J$ and $\sigma_J$.

#### Stochastic Volatility Jump Model
The [Stochastic Volatility Jump (Bates) Model](models/stochastic_volatility_jump.py) combines the Heston Stochastic Volatility model with the Jump Diffusion model:

$$ dS_t = \mu S_t ~ dt + \sqrt{V_t} S_t ~ dW_{S,t} + S_t ~ dJ_t $$

$$ dV_t = \kappa (\theta - V_t) ~ dt + \sigma \sqrt{V_t} ~ dW_{V,t} $$ 

the parameter definitions follow naturally from the Stochastic Volatility and Jump Diffusion Models. -->