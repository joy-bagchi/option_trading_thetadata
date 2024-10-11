import numpy as np
import matplotlib.pyplot as plt
from py_vollib.black_scholes import black_scholes
from py_vollib.black_scholes.greeks.numerical import delta
from py_vollib.black_scholes.implied_volatility import implied_volatility
from scipy.optimize import brentq
from sabr_model import sabr_volatility, fit_sabr

def delta_to_strike(S, delta_value, T, r, sigma, option_type='call'):
    """Convert delta to strike using an inverse relation."""

    def objective_function(K):
        computed_delta = delta(option_type, S, K, T, r, sigma)
        return computed_delta - delta_value

    K_min = 0.01 * S
    K_max = 3.0 * S
    strike = brentq(objective_function, K_min, K_max)
    return strike

# Simulate Equity Volatility Surface using SABR
def simulate_equity_vol_surface(S0, r, T_range, delta_range, atm_vol, option_type):
    # Initialize an empty volatility surface
    vol_surface = np.zeros((len(T_range), len(delta_range)))

    # SABR Model for Smile/Skew Adjustment
    for i, T in enumerate(T_range):
        F = S0  # Assume ATM forward price is S0 (adjust this as needed)

        # Fit SABR to the ATM vol to introduce skew
        strikes = np.linspace(0.8 * S0, 1.2 * S0, 50)  # Example strikes
        atm_vols = np.full_like(strikes, atm_vol)  # Use ATM vol as proxy for initial guess

        # Fit SABR model to ATM volatility to introduce skew
        alpha, beta, rho, nu = fit_sabr(strikes, atm_vols, F, T)

        for j, delta_value in enumerate(delta_range):
            # Use delta-to-strike conversion (this remains the same)
            K = delta_to_strike(S0, delta_value, T, r, atm_vol, option_type)

            # Calculate implied vol for each strike using the SABR model
            sabr_iv = sabr_volatility(K, F, T, alpha, beta, rho, nu)

            # Store the SABR-implied vol in the surface
            vol_surface[i, j] = sabr_iv
    return vol_surface

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
