# This is a sample Python script.
from py_vollib import black_scholes as bs
from py_vollib.black_scholes.greeks import analytical as greeks_a
from py_vollib.black_scholes.greeks import numerical as greeks_n
from py_vollib.black_scholes import implied_volatility as iv



option_price = bs.black_scholes('c', 577.14, 578, 1/365,0.05, 0.176)
print(option_price )   # Call option price
delta = greeks_n.delta('c', 577.14, 578, 1/365, 0.05, 0.1653)  # Call option delta
print('Delta: '+str(delta))
gamma = greeks_n.gamma('c', 577.14, 578, 1/365, 0.05, 0.1653)  # Call option gamma
print('Gamma: '+str(gamma))
theta = greeks_n.theta('c', 577.14, 578, 1/365, 0.05, 0.1653)  # Call option theta
print('Theta: '+str(theta))
option_price = 1.75
imp_vol = iv.implied_volatility(option_price, 577.14, 578, 1/365, 0.05, 'c')  # Call option gamma('c', 552.08, 555, 3/365, 0.02, 0.2114)  # Call option gamma
print(imp_vol)




