import pickle
import numpy as np
import json


def handle(event, context):
    with open('./stock_model.pickle', 'rb') as model_file:
        model = pickle.load(model_file)

    print("I am here")
    yesterday_close = float(event['yesterday_close'])
    x = np.array([yesterday_close])

    p = model.predict(x.reshape((1, 1)))
    p = "{:.2f}".format(p[0])
    return {"close": float(p)}


if __name__ == '__main__':
    handle({"yesterday_close": "13.48"}, None)
