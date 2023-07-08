import unittest
from unittest.mock import patch, MagicMock
import main


class TestMain(unittest.TestCase):
    def test_percent_diff(self):
        actual = main.percent_difference(1, 3)
        self.assertEqual(100, actual)  # add assertion here

    def test_get_predicted_value(self):
        actual = main.get_predicted_value("50.0")
        self.assertIsNotNone(actual)

    @patch("main.yfinance.Ticker")
    def test_test_model(self, ticker):
        ticker().info = {"close": 20.0, 'previousClose': 21.0}
        main.test_model("CANE")

    @patch("main.yfinance.Ticker")
    def test_handle_signal_test_model(self, ticker):
        ticker().info = {"close": 20.0, 'previousClose': 21.0}
        actual = main.handle(dict(), None)
        self.assertEqual("OK", actual)

    @patch("main.yfinance.Ticker")
    def test_handle_signal_normal(self, ticker):
        ticker().info = {"close": 20.0, 'previousClose': 21.0}
        actual = main.handle({'yesterday_close': 15.0}, None)
        self.assertNotEqual("OK", actual)


if __name__ == '__main__':
    unittest.main()
