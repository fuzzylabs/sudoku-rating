import argparse

import pandas as pd
from typing import Tuple
import numpy as np
from tqdm import tqdm
from sklearn.linear_model import Ridge
from sklearn.base import BaseEstimator
from sklearn.metrics import mean_absolute_error
from joblib import dump

tqdm.pandas()  # make pandas aware of tqdm


def load_data(path: str) -> pd.DataFrame:
    print("Load dataset")
    return pd.read_csv(path)


def prepare(dataset: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    print("Prepare dataset")
    feature_cols = [f"digit_{x}"for x in range(81)]
    return dataset.loc[:, feature_cols].values, dataset.difficulty.values


def train(X: np.ndarray, y: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, alpha: float = 1.0) -> BaseEstimator:
    print("Fit model")
    model = Ridge(alpha=alpha)
    model.fit(X, y)

    print("Evaluate model")
    y_pred = model.predict(X_test)

    accuracy = mean_absolute_error(y_test, y_pred)
    print("MAE:", accuracy)

    return model


def persist_model(model: BaseEstimator, path: str):
    print("Persisting the model")
    dump(model, path)


def main(dataset_path: str, test_dataset_path: str, alpha: float):
    dataset = load_data(dataset_path)
    test_dataset = load_data(dataset_path)
    X, y = prepare(dataset)
    X_test, y_test = prepare(test_dataset)
    model = train(X, y, X_test, y_test, alpha)
    persist_model(model, "artifact/linearregression.joblib")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train linear model')

    parser.add_argument("--alpha", type=float)

    args = parser.parse_args()

    main("data/sudoku-3m-train.csv", "data/sudoku-3m-test.csv", args.alpha)
