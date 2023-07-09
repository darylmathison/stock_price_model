import pickle

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
    return numerator/denominator * 100


def date_range():
    calendar = business_calendar.Calendar(workdays=[MO, TU, WE, TH, FR])
    end_day = datetime.datetime.today()
    day_delta = datetime.timedelta(days=1)

    while not calendar.isworkday(end_day):
        end_day = end_day - day_delta

    return (end_day - day_delta), end_day


def find_two_prior_closes(stock_symbol):
    ticker = yfinance.Ticker(stock_symbol)
    start_day, end_day = date_range()
    history = ticker.history(start=start_day, end=end_day)
    print(history.info)
    close = history.filter(["Close"])
    return close.to_numpy()


def test_model(stock_symbol):
    closes = find_two_prior_closes(stock_symbol)
    print(closes)

    predicted_close = get_predicted_value(closes[0])
    actual_close = float(closes[1])
    percent_diff = percent_difference(predicted_close, actual_close)
    logger.info("predicted close: %s; actual close: %s; percent difference %s",
                predicted_close, actual_close, percent_diff)


def get_predicted_value(input_value):
    with open('./stock_model.pickle', 'rb') as model_file:
        model = pickle.load(model_file)
    x_value = float(input_value)
    x = np.array([x_value])
    p = model.predict(x.reshape((1, 1)))
    p = "{:.2f}".format(p[0])
    return float(p)


def handle(event, context):

    if "yesterday_close" in event:
        close = get_predicted_value(event['yesterday_close'])
        logger.info("Today's predicted close is %s with yesterday's close", close, event['yesterday_close'])

        return {"close": close}
    else:
        test_model('CANE')
        return "OK"


if __name__ == '__main__':
    handle(dict(), None)
