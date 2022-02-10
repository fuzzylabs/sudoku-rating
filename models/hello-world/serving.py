import numpy as np
import bentoml
from bentoml.io import JSON
from puzzle_utils import prepare_puzzle

linear_regression_runner = bentoml.sklearn.load_runner("linear_regression:latest")

svc = bentoml.Service("linear_regression", runners=[linear_regression_runner])


@svc.api(
    input=JSON(),
    output=JSON(),
    doc="Takes string representations of sudoku and returns a difficulty score.",
)
def predict(cases):
    """
    Hello Heaven
    :param cases: World
    :return: Hi
    """
    prepared_cases = np.vstack([prepare_puzzle(case) for case in cases])
    print(prepared_cases)

    return [linear_regression_runner.run(case) for case in prepared_cases]
