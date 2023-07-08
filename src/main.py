import pickle
import numpy as np
import yfinance
import logging

logger = logging.getLogger(__name__)


def percent_difference(value1, value2):
    numerator = abs(value1 - value2)
    denominator = (value1 + value2)/2
    return numerator/denominator * 100


def test_model(stock_symbol):
    ticker = yfinance.Ticker(stock_symbol)
    predicted_close = get_predicted_value(ticker.info['previousClose'])
    actual_close = float(ticker.info['close'])
    percent_diff = percent_difference(predicted_close, actual_close)
    logger.info("predicted close: %s; actual close: %s; percent difference %s",
                predicted_close, ticker.info["close"], percent_diff)


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
