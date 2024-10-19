import numpy as np
from sqlalchemy.testing.plugin.plugin_base import logging
from timeit_decorator import timeit
from simulate_equity_vol_surface import simulate_equity_vol_surface, plot_vol_surface
from simulate_equity_price_with_stochastic_vol import simulate_equity_price_with_stochastic_vol
from sabr_model import calibrate_sabr_model
# Seed for reproducibility
np.random.seed(42)
import logging
logging.basicConfig(level=logging.INFO)

#Parameters:
M = 1  # Number of simulations

# Time parameters
T = 1.0        # Total simulation time in years
N = 252        # Number of time steps (daily)

# Heston model parameters
mu = 0.07           # Drift
kappa = 2.0         # Speed of mean reversion for variance
theta = 0.04        # Long-term variance
sigma_v = 0.3       # Volatility of variance
rho = -0.7          # Correlation between asset and variance
V0 = 0.04           # Initial variance
S0 = 576            # Initial SPY price

# Vol Surface parameters for SABR
r = 0.05  # Risk-free rate
T_range = np.arange(1/252, 10/252, 1/252)  # Maturities from 1 to 10 days
delta_range = np.arange(0.30, 0.51, 0.05)  # Delta range from 30 to 70
_vols = np.array([0.1472, 0.1537, 0.1609, 0.1706, 0.1796])  # Implied volatilities
print(delta_range, _vols)

option_type = 'c'  # 'c' for call options and 'p' for put options

@timeit(log_level=logging.DEBUG)
def run_sim():
    sabr = calibrate_sabr_model(S0, r, T, delta_range, _vols, 0.25, option_type)
    S, V = simulate_equity_price_with_stochastic_vol(mu, kappa, theta, sigma_v, rho, V0, S0, T, N, M)
    VS = np.zeros((M, N+1, len(T_range), len(delta_range)))
    for i in range(M):
        for j in range(N):
            VS[i,j] = simulate_equity_vol_surface(sabr, S[i,j], r, T_range, delta_range, V[i,j], option_type)
    # plot_vol_surface(T_range, delta_range, VS[0,0])
    return S, V, VS

if __name__ == '__main__':
    # print(timeit.timeit(run_sim, number=1))
    s, v, vs = run_sim()
    print(s.shape, v.shape, vs.shape)