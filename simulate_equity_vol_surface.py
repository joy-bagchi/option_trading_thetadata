import numpy as np
import matplotlib.pyplot as plt

from py_vollib.black_scholes.greeks.numerical import delta
from py_vollib.black_scholes.implied_volatility import implied_volatility
from scipy.optimize import brentq
from sabr_model import sabr_volatility, fit_sabr


def delta_to_strike(S, delta_value, T, r, sigma, option_type='call'):
    """Convert delta to strike using an inverse relationship.
    S: Current asset price
    delta_value: Delta value
    T: Time to maturity
    r: Risk-free rate
    sigma: Implied volatility
    option_type: 'call' or 'put'
    """

    def objective_function(K):
        computed_delta = delta(option_type, S, K, T, r, sigma)
        return computed_delta - delta_value

    K_min = 0.01 * S
    K_max = 3.0 * S
    strike = brentq(objective_function, K_min, K_max)
    return strike

# Simulate Equity Volatility Surface using SABR
def simulate_equity_vol_surface(S, r, T_range, delta_range, V, option_type='c'  , M=1000):
    """Simulate an equity volatility surface using the SABR model.
    asset_prices: Array of simulated asset prices
    r: Risk-free rate
    T_range: Array of time to maturity values
    delta_range: Array of delta values
    atm_vols: Array of ATM volatilities
    option_type: 'c' for call options and 'p' for put options
    M: Number of simulations
    """

    # Initialize an empty volatility surface
    vol_surfaces = np.zeros((len(T_range), len(delta_range)))

    # SABR Model for Smile/Skew Adjustment
    for i, T in enumerate(T_range):
        F = S  # Assume ATM forward price is S0 (adjust this as needed)
        # Fit SABR to the ATM vol to introduce skew
        strikes = np.linspace(0.8 * S, 1.2 * S, 50)  # Example strikes

        # Fit SABR model to ATM volatility to introduce skew
        alpha, beta, rho, nu = fit_sabr(strikes, V, F, T)
        for j, delta_value in enumerate(delta_range):
            # Use delta-to-strike conversion (this remains the same)
            K = delta_to_strike(S, delta_value, T, r, V, option_type)

            # Calculate implied vol for each strike using the SABR model
            sabr_iv = sabr_volatility(K, F, T, alpha, beta, rho, nu)

            # Store the SABR-implied vol in the surface
            vol_surfaces[i, j] = sabr_iv
    return vol_surfaces

# Plotting
def plot_vol_surface(T_range, delta_range, vol_surface):
    T_grid, delta_grid = np.meshgrid(T_range * 252, delta_range)  # Convert T to days

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(T_grid, delta_grid, vol_surface.T, cmap='viridis')

    ax.set_xlabel('Days to Maturity')
    ax.set_ylabel('Delta')
    ax.set_zlabel('Implied Volatility')
    ax.set_title('Implied Volatility Surface (py_vollib)')

    plt.show()
