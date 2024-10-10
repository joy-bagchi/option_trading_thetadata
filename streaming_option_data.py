import http.client

conn = http.client.HTTPConnection("127.0.0.1:25510")

headers = { 'Accept': "application/json" }

conn.request("GET", "/v2/hist/option/implied_volatility?root=SPY&exp=20240925&right=C&"
                    "strike=573000&start_date=20240901&end_date=20240923&ivl=900000", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))