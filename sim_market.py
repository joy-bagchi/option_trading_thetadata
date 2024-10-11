import numpy as np
from simulate_equity_vol_surface import simulate_equity_vol_surface, plot_vol_surface

#Parameters:
S0 = 557  # Initial SPY price
r = 0.05  # Risk-free rate
T_range = np.arange(1/252, 10/252, 1/252)  # Maturities from 1 to 10 days
delta_range = np.arange(0.30, 0.71, 0.05)  # Delta range from 30 to 70
atm_vol = 0.20  # Approximate volatility (from Heston or simulation)
option_type = 'c'  # 'c' for call options

vol_surf = simulate_equity_vol_surface(S0, r, T_range, delta_range, atm_vol, option_type)
plot_vol_surface(T_range, delta_range, vol_surf)