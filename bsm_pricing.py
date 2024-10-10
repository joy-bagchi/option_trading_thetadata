import math
import numpy as np
import pandas as pd
from scipy.stats import norm

#Black-Scholes price and Greeks
class EuropeanOptionBS:

    def __init__(self, S, K, T, r, dividend, sigma, Type):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.dividend = dividend
        self.sigma = sigma
        self.Type = Type
        self.d1 = self.d1()
        self.d2 = self.d2()
        self.price = self.price()
        self.delta = self.delta()
        self.theta = self.theta()
        self.vega = self.vega()
        self.gamma = self.gamma()
        self.volga = self.volga()
        self.vanna = self.vanna()

    def d1(self):
        d1 = (math.log(self.S / self.K) \
              + (self.r - self.dividend + .5 * (self.sigma ** 2)) * self.T) \
             / (self.sigma * self.T ** .5)
        return d1

    def d2(self):
        d2 = self.d1 - self.sigma * self.T ** .5
        return d2

    def price(self):
        price = 0
        if self.Type == "Call":
            price = self.S * math.exp(-self.dividend * self.T) * norm.cdf(self.d1) \
                    - self.K * math.exp(-self.r * self.T) * norm.cdf(self.d2)
        if self.Type == "Put":
            price = self.K * math.exp(-self.r * self.T) * norm.cdf(-self.d2) \
                    - self.S * math.exp(-self.dividend * self.T) * norm.cdf(-self.d1)
        return price

    def delta(self):
        delta = 0
        if self.Type == "Call":
            delta = math.exp(-self.dividend * self.T) * norm.cdf(self.d1)
        if self.Type == "Put":
            delta = -math.exp(-self.dividend * self.T) * norm.cdf(-self.d1)
        return delta

    def theta(self):
        theta = 0
        if self.Type == "Call":
            theta1 = -math.exp(-self.dividend * self.T) * \
                     (self.S * norm.pdf(self.d1) * self.sigma) / (2 * self.T ** .5)
            theta2 = self.dividend * self.S * math.exp(-self.dividend * self.T) * norm.cdf(self.d1)
            theta3 = -self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(self.d2)
            theta = theta1 + theta2 + theta3
        if self.Type == "Put":
            theta1 = -math.exp(-self.dividend * self.T) * \
                     (self.S * norm.pdf(self.d1) * self.sigma) / (2 * self.T ** .5)
            theta2 = -self.dividend * self.S * math.exp(-self.dividend * self.T) * norm.cdf(-self.d1)
            theta3 = self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(-self.d2)
            theta =  theta1 + theta2 + theta3
        return theta

    def vega(self):
        vega = self.S * math.exp(-self.dividend * self.T) * self.T ** .5 * norm.pdf(self.d1)
        return vega

    def gamma(self):
        gamma = math.exp(-self.dividend * self.T) * norm.pdf(self.d1) / (self.S * self.sigma * self.T ** .5)
        return gamma

    def volga(self):
        volga = self.vega / self.sigma * self.d1 * self.d2
        return volga

    def vanna(self):
        vanna = -self.vega / (self.S * self.sigma * self.T** .5) * self.d2
        return vanna
