import pandas as pd
from datetime import date, datetime
from thetadata import ThetaClient, DateRange, StockReqType, OptionReqType, OptionRight


def end_of_day() -> pd.DataFrame:
    # client = ThetaClient(username="joy.bagchi@gmail.com", passwd="Me!2cedesclk320")  # No credentials required for free access
    client = ThetaClient(launch=False)  # No credentials required for free access
    # Make any requests for data inside this block. Requests made outside this block won't run.
    with client.connect():
        # out = client.get_hist_stock(
        #     req=StockReqType.EOD,  # End of day data
        #     root="SPY",
        #     date_range=DateRange(date(2024, 1, 1), date(2024, 1, 30)),
        # )
        snap = client.get_hist_option(
            req=OptionReqType.IMPLIED_VOLATILITY,  # Snapshot data
            root="SPY",
            exp=datetime(2024, 9, 25),
            right=OptionRight.CALL,
            strike=573,
            date_range=DateRange(date(2024, 9, 1), date(2024, 9, 23)),
        )

    # We are out of the client.connect() block, so we can no longer make requests.
    return snap

if __name__ == "__main__":
    data = end_of_day()
    print(data.to_string())
