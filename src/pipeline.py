from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import numpy as np
from pandas import DataFrame


def globbing_prices(data: DataFrame, history=1, num_outputs=1):
    x = []
    y = []
    for i in range(history, len(data) - num_outputs):
        x.append(data[i - history:i].values)
        ends = data[i: (i + num_outputs)].values
        y.append(ends[0])

    x_np = np.array(x)
    y_np = np.array(y)
    return x_np.reshape((x_np.shape[0], x_np.shape[1])), y_np.reshape((y_np.shape[0], y_np.shape[1]))


def create_pipeline(column_name):
    def filter_out_columns(dataframe):
        return dataframe.filter([column_name])

    return Pipeline([
        ('filtering', FunctionTransformer(filter_out_columns)),
        ('globbing_data', FunctionTransformer(globbing_prices))
    ])
