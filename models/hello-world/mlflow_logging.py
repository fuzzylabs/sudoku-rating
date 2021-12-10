from mlflow import log_metric, log_param, start_run
from linearregression import linear_regression


def main():
    for alpha in range(10):
        with start_run(nested=True):
            log_param("alpha", alpha)
            _, accuracy = linear_regression("../../data/sudoku-3m.csv", alpha)
            log_metric("MAE", accuracy)


if __name__ == "__main__":
    main()
