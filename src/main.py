from fastapi import FastAPI
import pickle
import numpy as np

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/predict/{yesterday_close}")
async def prediction(yesterday_close: float):
    with open('data/stock_model.pickle', 'rb') as model_file:
        model = pickle.load(model_file)

    x = np.array([yesterday_close])
    p = str(model.predict(x.reshape((1, 1))))
    return {"close": p}


