# Dynamic Programming for Theoretcial Option Pricing


<!-- In this project we approach theoretical option pricing as a dynamic programming problem in which at each time step we have information $S_t \in \mathcal{S}$ such as the underlying price, time till expiry, interest rates, etc. We also have a set of actions we can take at each time step $a \in \mathcal{A}$ such as early exercise, taking no action, etc. We also have functions defining the cost/reward of taking an action $C(s_t, a_t)$ and probabilty of transitioning from one state to another $P(s_{t + 1} ~|~ s_t, a_t)$ typically independent of $a_t$ and corresponds to price movements of the underlying. Our goal therefore is to find $V^*(s_t)$ which denotes the theoretical value of an option under the assumtion that the holder of the contract takes the most optional actions during the lifetime of the contract. By the Bellman Optimality Principle, $V^*(s_t)$ can be recursively defined as:

$$
\begin{equation}
V^*(s_t) = 
    \max_{a_t \in \mathcal{A}} 
    \bigg\lbrace
        C(s_t, a_t) + \int_{s_{t+1}} P(s_{t + 1} ~|~ s_t, a_t) V^*(s_{t + 1})  
    \bigg\rbrace
\end{equation}
$$ -->


To learn more see [models](models/README.md) and [algorithms](algorithms/README.md)