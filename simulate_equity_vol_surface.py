import numpy as np
import matplotlib.pyplot as plt

from pysabr import Hagan2002LognormalSABR
from sabr_model import delta_to_strike


# Simulate Equity Volatility Surface using SABR
def simulate_equity_vol_surface(calibrated_sabr_model, S, r, T_range, delta_range, atm_iv, option_type='c'  , M=1000):
    """Simulate an equity volatility surface using the SABR model.
    asset_prices: Array of simulated asset prices
    r: Risk-free rate
    T_range: Array of time to maturity values
    delta_range: Array of delta values
    atm_vols: Array of ATM volatilities
    option_type: 'c' for call options and 'p' for put options
    M: Number of simulations
    """

    # Calibrate SABR model to the ATM vol

    # Initialize an empty volatility surface
    vol_surfaces = np.zeros((len(T_range), len(delta_range)))
    beta = 0.5 # Assume beta = 0.5 for simplicity
    # SABR Model for Smile/Skew Adjustment
    for i, T in enumerate(T_range):
        F = S  # Assume ATM forward price is S0 (adjust this as needed)
        for j, delta_value in enumerate(delta_range):
            # Use delta-to-strike conversion (this remains the same)
            K = delta_to_strike(S, delta_value, T, r, atm_iv, option_type)

            # Calculate implied vol for each strike using the SABR model
            sabr_iv = calibrated_sabr_model.lognormal_vol(K)

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
