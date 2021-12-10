import argparse
import os

import pandas as pd
from typing import Tuple
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.base import BaseEstimator
from sklearn.metrics import mean_absolute_error

tqdm.pandas()  # make pandas aware of tqdm


def load_data(path: str) -> pd.DataFrame:
    print("Load dataset")
    return pd.read_csv(path)


def get_category(char: str) -> int:
    if char == ".":
        return 0
    else:
        return int(char)


def prepare_puzzle(puzzle: str) -> np.ndarray:
    return np.array([get_category(char) for char in puzzle])


def prepare(dataset: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    print("Prepare dataset")
    prepared_puzzles = np.vstack(dataset.puzzle.progress_apply(prepare_puzzle).values)
    return prepared_puzzles, dataset.difficulty.values


def train(X: np.ndarray, y: np.ndarray, alpha: float = 1.0) -> BaseEstimator:
    print("Split data")
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model = Ridge(alpha=alpha)

    print("Fit model")
    model.fit(X_train, y_train)

    print("Evaluate model")
    y_pred = model.predict(X_test)

    accuracy = mean_absolute_error(y_test, y_pred)
    print("MAE:", accuracy)

    return model


def main(dataset_path: str, alpha: float):
    dataset = load_data(dataset_path).iloc[:10000]
    X, y = prepare(dataset)
    model = train(X, y, alpha)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train linear model')

    parser.add_argument("--alpha", type=float)

    args = parser.parse_args()

    main("data/sudoku-3m.csv", args.alpha)
