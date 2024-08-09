# Suported Contracts
In this section we go over the supported contracts as well as their respective dynamic programming formulations

## Vanilla Option

Given a strike price $K$ let our option's exercise value, $C(S_t)$, can be defined as $C(S_t) = \max\{S_t - K, 0\}$ in the case of a call option and $C(S_t) = \max\{K - S_t, 0\}$ in the case of a put.

$$
V(S_t) = 
\begin{cases}
t = T \Rightarrow C(S_t)
\\\\
t \lt T \Rightarrow \max\left\{ C(S_t), ~~\mathbb{E}\bigg[V(S_{t + dt})\bigg]\right\}
\end{cases}
$$

and in the case of european exercise:

$$
V(S_t) = 
\begin{cases}
t = T \Rightarrow C(S_t)
\\\\
t \lt T \Rightarrow \mathbb{E}\bigg[V(S_{t + dt})\bigg]
\end{cases}
$$
