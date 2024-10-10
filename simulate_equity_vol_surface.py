from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks.numerical import delta
from py_vollib.black_scholes.implied_volatility import implied_volatility
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq


def delta_to_strike(S, delta_value, T, r, sigma, option_type='call'):
    """Convert delta to strike using an inverse relation."""

    def objective_function(K):
        computed_delta = delta(option_type, S, K, T, r, sigma)
        return computed_delta - delta_value

    K_min = 0.01 * S
    K_max = 3.0 * S
    strike = brentq(objective_function, K_min, K_max)
    return strike


# Parameters
S0 = 575  # Initial SPY price
r = 0.05  # Risk-free rate (1%)
T_range = np.arange(1 / 252, 10 / 252, 1 / 252)  # Maturities from 1 to 10 days
delta_range = np.arange(0.30, 0.71, 0.01)  # Delta range from 30 to 70
sigma = 0.20  # Approximate volatility
option_type = 'c'  # 'c' for call options

# Initialize an empty volatility surface
vol_surface = np.zeros((len(T_range), len(delta_range)))

# Populate the volatility surface
for i, T in enumerate(T_range):
    for j, delta_value in enumerate(delta_range):
        # Find the corresponding strike for each delta
        K = delta_to_strike(S0, delta_value, T, r, sigma, option_type)

        # Calculate the option price using py_vollib
        market_price = black_scholes(option_type, S0, K, T, r, sigma)

        # Compute implied volatility using py_vollib
        iv = implied_volatility(market_price, S0, K, T, r, option_type)

        # Store the implied volatility in the surface
        vol_surface[i, j] = iv

# Plotting
T_grid, delta_grid = np.meshgrid(T_range * 252, delta_range)  # Convert T to days

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(T_grid, delta_grid, vol_surface.T, cmap='viridis')

ax.set_xlabel('Days to Maturity')
ax.set_ylabel('Delta')
ax.set_zlabel('Implied Volatility')
ax.set_title('Implied Volatility Surface (py_vollib)')

plt.show()
