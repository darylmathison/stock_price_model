import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from pipeline import create_pipeline
import pickle

plt.style.use('fivethirtyeight')


def evaluate_models(x, y, model):
    params = {
        "max_depth": [i for i in range(7, 15)],
        "criterion": ["squared_error", "friedman_mse", "absolute_error", "poisson"],
        "splitter": ["best", "random"],
        "max_features": ["sqrt", "log2"],
        "min_samples_split": [i for i in range(2, 5)]
    }

    gs = GridSearchCV(model, params, cv=3)

    gs.fit(x, y)
    print(gs.best_score_, gs.best_params_)
    return gs.best_estimator_


def main():
    cane = pd.read_csv('../data/CANE.csv', index_col=0)
    pipeline = create_pipeline("Close")
    x, y = pipeline.fit_transform(cane)

    x_training_data, x_verify, y_training_data, y_verify = train_test_split(x, y, train_size=0.8, shuffle=False)
    x_train, x_test, y_train, y_test = train_test_split(x_training_data, y_training_data, train_size=0.9, shuffle=False)

    best_model = evaluate_models(x_train, y_train, DecisionTreeRegressor())
    print(best_model.score(x_test, y_test))
    print(best_model.score(x_verify, y_verify))

    with open('../data/stock_model.pickle', 'wb') as model_file:
        pickle.dump(best_model, model_file)


if __name__ == '__main__':
    main()
