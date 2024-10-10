import QuantLib as ql
from datetime import date
today = date.today()

option = ql.EuropeanOption(ql.PlainVanillaPayoff(ql.Option.Call, 578.0),
                           ql.EuropeanExercise(ql.Date(10, 10, 2024)))
u = ql.SimpleQuote(577.14)
r = ql.SimpleQuote(0.05)
sigma = ql.SimpleQuote(0.1653)
riskFreeCurve = ql.FlatForward(0, ql.NullCalendar(), ql.QuoteHandle(r), ql.Actual360())
volatility = ql.BlackConstantVol(0, ql.NullCalendar(), ql.QuoteHandle(sigma), ql.Actual360())
process = ql.BlackScholesProcess(ql.QuoteHandle(u), ql.YieldTermStructureHandle(riskFreeCurve),
                                 ql.BlackVolTermStructureHandle(volatility))
engine = ql.AnalyticEuropeanEngine(process)
option.setPricingEngine(engine)
print(option.NPV())
print(option.delta())
print(option.gamma())
print(option.theta())
print(option.vega())
