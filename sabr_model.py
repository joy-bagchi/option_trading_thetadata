import numpy as np
from pysabr import Hagan2002LognormalSABR
from scipy.optimize import brentq
from py_vollib.black_scholes.greeks.numerical import delta


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


def calibrate_sabr_model(S, r, T, delta_range, market_vols, atm_iv, option_type='c'):
    """Calibrate the SABR model to the ATM volatility.
    S: Current asset price
    r: Risk-free rate
    T: Time to maturity
    delta: Delta value
    atm_iv: ATM implied volatility
    option_type: 'c' for call options and 'p' for put options
    """
    assert len(delta_range) == len(market_vols), "Mismatch between delta_range and market_vols length"

    # Initial guess for beta
    _beta = 0.5

    # SABR Model for Smile/Skew Adjustment
    _sabr = Hagan2002LognormalSABR(S, S, T, atm_iv, _beta, rho=-0.25, volvol=0.3)
    strikes = [delta_to_strike(S, delta_value, T, r, atm_iv, option_type) for delta_value in delta_range]
    # Fit SABR to the ATM vol to introduce skew
    _alpha, _rho, _nu = _sabr.fit(strikes, market_vols)

    return Hagan2002LognormalSABR(S, S, T, atm_iv, _beta, rho=_rho, volvol=_nu)