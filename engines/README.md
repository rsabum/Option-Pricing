# Suported Contracts
In this section we go over the supported contracts as well as their respective dynamic programming formulations

## Vanilla Option

Given a strike price $K$ let our option's exercise value, $C(S_t)$, can be defined as $C(S_t) = \max\{S_t - K, 0\}$ in the case of a call option and $C(S_t) = \max\{K - S_t, 0\}$ in the case of a put.

$$
V(S_t) = 
\begin{cases}
t = T \implies C(S_t)
\\\\
t \lt T \implies \max\left\lbrace C(S_t), ~~\mathbb{E}\bigg[V(S_{t + dt})\bigg]\right\rbrace
\end{cases}
$$

and in the case of european exercise:

$$
V(S_t) = 
\begin{cases}
t = T \implies C(S_t)
\\\\
t \lt T \implies \mathbb{E}\bigg[V(S_{t + dt})\bigg]
\end{cases}
$$


## Asian Option

Let $\mu(S_t)$ denote the geometric or arithmetic mean of our underlying asset at time $t$. Given a strike price $K$ let our option's exercise value, $C(S_t)$, can be defined as $C(S_t) = \max\{\mu(S_t) - K, 0\}$ in the case of a call option and $C(S_t) = \max\{K - \mu(S_t), 0\}$ in the case of a put.

$$
V(S_t) = 
\begin{cases}
t = T \implies C(S_t)
\\\\
t \lt T \implies \max\left\lbrace C(S_t), ~~\mathbb{E}\bigg[V(S_{t + dt})\bigg]\right\rbrace
\end{cases}
$$

and in the case of european exercise:

$$
V(S_t) = 
\begin{cases}
t = T \implies C(S_t)
\\\\
t \lt T \implies \mathbb{E}\bigg[V(S_{t + dt})\bigg]
\end{cases}
$$
