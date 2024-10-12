import numpy as np
import matplotlib.pyplot as plt



def simulate_equity_price_with_stochastic_vol(mu, kappa, theta, sigma_v, rho, V0, S0, T, N, M):
    """ Simulate equity price paths using the Heston model.
        mu: Drift
        kappa: Speed of mean reversion for variance
        theta: Long-term variance
        sigma_v: Volatility of variance
        rho: Correlation between asset and variance
        V0: Initial variance
        S0: Initial SPY price
        T: Total time in years
        N: Number of time steps (daily)
    """
    # Initialize arrays
    S = np.zeros((M, N+1)) # Matrix to store simulated asset prices
    V = np.zeros((M, N+1)) # Matrix to store simulated variance
    S[:, 0] = S0         # Initial asset price
    V[:, 0] = V0        # Initial variance
    dt = T / N          # Time step

    # Cholesky decomposition for correlated Brownian motions
    corr_matrix = np.array([[1.0, rho],
                            [rho, 1.0]])
    L = np.linalg.cholesky(corr_matrix)

    for t in range(1, N+1):
        # Generate two independent random variables (Z1, Z2) from standard normal distribution (brownian motions)
        Z = np.random.normal(size=(M, 2))
        # Introduce correlation between two brownian motions
        correlated_Z = Z @ L.T
        dW1 = correlated_Z[:, 0] * np.sqrt(dt)
        dW2 = correlated_Z[:, 1] * np.sqrt(dt)

        # Ensure variance remains positive using Full Truncation Euler
        V_prev = V[:, t-1]
        V_prev_sqrt = np.sqrt(np.maximum(V_prev, 0))

        # Update variance: This is the Euler discretization of the Heston model
        V[:, t] = V_prev + kappa * (theta - V_prev) * dt + sigma_v * V_prev_sqrt * dW2
        V[:, t] = np.maximum(V[:, t], 0)  # Full truncation to prevent negative variance

        # Update asset price
        S[:, t] = S[:, t-1] * np.exp((mu - 0.5 * V_prev) * dt + V_prev_sqrt * dW1)

    return S, V

def plot_equity_price_and_volatility(S, V, T, N, M):
    """ Plot simulated equity price paths and volatility paths.
        S: Matrix of simulated asset prices
        V: Matrix of simulated variance
        T: Total time in years
        N: Number of time steps (daily)
        M: Number of simulations
    """
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
