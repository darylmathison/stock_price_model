import unittest
from unittest.mock import patch, MagicMock
import main


class TestMain(unittest.TestCase):
    def test_percent_diff(self):
        actual = main.percent_difference(1, 2)
        self.assertEqual(50, actual)  # add assertion here

    def test_get_predicted_value(self):
        actual = main.get_predicted_value("50.0")
        self.assertIsNotNone(actual)

    @patch("main.find_two_prior_closes")
    def test_test_model(self, two_closes):
        two_closes.__call__ = MagicMock(return_value=[12.0, 20.0])
        main.test_model("CANE")

    @patch("main.yfinance.Ticker")
    def test_handle_signal_test_model(self, ticker):
        ticker().info = {'previousClose': 21.0}
        actual = main.handle(dict(), None)
        self.assertEqual("OK", actual)

    @patch("main.yfinance.Ticker")
    def test_handle_signal_normal(self, ticker):
        ticker().info = {"close": 20.0, 'previousClose': 21.0}
        actual = main.handle({'yesterday_close': 15.0}, None)
        self.assertNotEqual("OK", actual)

    def test_date_range(self):
        _range = main.date_range()
        self.assertEqual(2, len(_range))


if __name__ == '__main__':
    unittest.main()
