import pickle
import os
import business_calendar
import numpy as np
import yfinance
import logging
from business_calendar import MO, TU, WE, TH, FR
import datetime

logger = logging.getLogger(__name__)


def percent_difference(value1, value2):
    numerator = abs(value1 - value2)
    denominator = value2
    return float("{:.2f}".format(numerator / denominator * 100))


def date_range():
    day_delta = datetime.timedelta(days=1)

    def find_first_prior_market_day(base_date: datetime.datetime):
        market_day = datetime.datetime(year=base_date.year, month=base_date.month, day=base_date.day)

        while not calendar.isworkday(market_day):
            market_day = market_day - day_delta
        return market_day

    calendar = business_calendar.Calendar(workdays=[MO, TU, WE, TH, FR])
    end_day = find_first_prior_market_day(datetime.datetime.today())
    start_day = find_first_prior_market_day(end_day - day_delta)
    return start_day, end_day


def find_two_prior_closes(stock_symbol):
    ticker = yfinance.Ticker(stock_symbol)
    start_day, end_day = date_range()
    history = ticker.history(start=start_day, end=end_day)
    close = history.filter(["Close"])
    return list(float("{:.2f}".format(p[0])) for p in close.to_numpy().tolist())


def test_model(stock_symbol):
    closes = find_two_prior_closes(stock_symbol)

    predicted_close = get_predicted_value(closes[0])
    actual_close = closes[1]
    percent_diff = percent_difference(predicted_close, actual_close)
    logger.info("predicted close: %s; actual close: %s; percent difference: %s",
                predicted_close, actual_close, percent_diff)
    return {"predicted_close": predicted_close,
            "actual_close": actual_close,
            "percent_diff": percent_diff}


def get_predicted_value(input_value):
    with open('./stock_model.pickle', 'rb') as model_file:
        model = pickle.load(model_file)
    x_value = float(input_value)
    x = np.array([x_value])
    p = model.predict(x.reshape((1, 1)))
    p = "{:.2f}".format(p[0])
    return float(p)


log_levels = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET
}

try:
    LOGGING_LEVEL = os.environ['LOGGING_LEVEL']
except KeyError as ke:
    LOGGING_LEVEL = "INFO"


def handle(event, context):
    logging.getLogger().setLevel(log_levels[LOGGING_LEVEL])

    if "yesterday_close" in event:
        close = get_predicted_value(event['yesterday_close'])
        logger.info("Today's predicted close is %s with yesterday's close %s", close, event['yesterday_close'])

        return {"close": close}
    else:
        return test_model('CANE')


if __name__ == '__main__':
    handle(dict(), None)
