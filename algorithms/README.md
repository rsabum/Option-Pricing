# Pricing Algorithms

## Dynamic Programming Formulation
In this project we assume that the theoretica value of an option contract is recursively dependent on the theoretical value of future states. Therefore we employ the bellman optimality condition to model their value given undelying price $S_t$ and exercise (Terminal) value function $C(S_t, \dots)$. We first define the following:
- $t$ the current time step.
- $T$ expiry time step.
- $S_t$ the contract's underliying price at time $t$
- $V(S_t)$ is the options theoretical value when its underlying asset is valued at $S_t$.
- $C(S_t, \dots)$ is the options exercise value given its current price $S_t$ and some additional variables.
- $K$ the strike price of our option or $K_1, \dots, K_n$ if there are multiple strikes.

### European Exercise
European exercise only allows one to exercise the contract at $t = T$ and therefore we only need to recursively consider the terminal states in our option valuation.

$$
V(S_t ~~\vert~~ C(S_t, \dots)) =  \mathbb{E}\bigg[C(S_{T}, \dots) ~~\bigg\vert~~ S_t\bigg]
$$


### American Exercise
American exercise allows for exercise at any $t \le T$ therefore, to calculate the value we must use backwards dynamic programming on possible price trajectories accounting for possible early exercise at each time step. This results in the following recurrence relation:

$$
V(S_t ~~\vert~~ C(S_t, \dots)) = 
\begin{cases}
t = T \implies C(S_t, \dots)
\\\\
t \lt T \implies \max\bigg\lbrace C(S_t), ~~\mathbb{E}\bigg[V(S_{t + dt} ~~\vert~~ C(S_t, \dots)) ~~\vert~~ S_t\bigg]\bigg\rbrace
\end{cases}
$$

from this we can see that with all else being equal, the value of a European contract can never exceed that of an American Exercise contract. Below we will simply define our payoff functions as well as any modifications we make to the recurrence relation for each option contract.

