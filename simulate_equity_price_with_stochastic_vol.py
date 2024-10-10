import numpy as np
import matplotlib.pyplot as plt

# Seed for reproducibility
np.random.seed(42)

# Time parameters
T = 1.0        # Total time in years
N = 252        # Number of time steps (daily)
dt = T / N     # Time step

# Heston model parameters
mu = 0.07           # Drift
kappa = 2.0         # Speed of mean reversion for variance
theta = 0.04        # Long-term variance
sigma_v = 0.3       # Volatility of variance
rho = -0.7          # Correlation between asset and variance
V0 = 0.04           # Initial variance
S0 = 576            # Initial SPY price

# Number of simulations
M = 500               # Number of simulated paths

# Initialize arrays
S = np.zeros((M, N+1))
V = np.zeros((M, N+1))
S[:, 0] = S0
V[:, 0] = V0

# Cholesky decomposition for correlated Brownian motions
corr_matrix = np.array([[1.0, rho],
                        [rho, 1.0]])
L = np.linalg.cholesky(corr_matrix)

for t in range(1, N+1):
    # Generate two independent random variables
    Z = np.random.normal(size=(M, 2))
    # Introduce correlation
    correlated_Z = Z @ L.T
    dW1 = correlated_Z[:, 0] * np.sqrt(dt)
    dW2 = correlated_Z[:, 1] * np.sqrt(dt)

    # Ensure variance remains positive using Full Truncation Euler
    V_prev = V[:, t-1]
    V_prev_sqrt = np.sqrt(np.maximum(V_prev, 0))

    # Update variance
    V[:, t] = V_prev + kappa * (theta - V_prev) * dt + sigma_v * V_prev_sqrt * dW2
    V[:, t] = np.maximum(V[:, t], 0)  # Full truncation to prevent negative variance

    # Update asset price
    S[:, t] = S[:, t-1] * np.exp((mu - 0.5 * V_prev) * dt + V_prev_sqrt * dW1)

# Time grid
time_grid = np.linspace(0, T, N+1)

# Plot SPY Price Paths
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
for m in range(M):
    plt.plot(time_grid, S[m], label=f'Path {m+1}')
plt.title('Simulated SPY Price Paths (Heston Model)')
plt.xlabel('Time (Years)')
plt.ylabel('Price')
plt.legend()

# Plot Volatility Paths
plt.subplot(1, 2, 2)
for m in range(M):
    plt.plot(time_grid, V[m], label=f'Path {m+1}')
plt.title('Simulated Variance Paths (Heston Model)')
plt.xlabel('Time (Years)')
plt.ylabel('Variance')
plt.legend()

plt.tight_layout()
plt.show()
