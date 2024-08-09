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
