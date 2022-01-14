import bentoml
import numpy as np
from bentoml import BentoService, api
from bentoml.adapters import JsonInput, JsonOutput
from bentoml.frameworks.sklearn import SklearnModelArtifact
from puzzle_utils import prepare_puzzle


@bentoml.env(infer_pip_packages=True)
@bentoml.artifacts([SklearnModelArtifact('linearregression')])
class SudokuRating(BentoService):

    @api(
        input=JsonInput(
            http_input_example="""
            [
              "1..5.37..6.3..8.9......98...1.......8761..........6...........7.8.9.76.47...6.312",
              "...81.....2........1.9..7...7..25.934.2............5...975.....563.....4......68."
            ]
            """
        ),
        output=JsonOutput(),
        api_doc="Takes string representations of sudoku and returns a difficulty score.",
    )
    def predict(self, cases):
        """
        Hello Heaven
        :param cases: World
        :return: Hi
        """
        prepared_cases = np.vstack([prepare_puzzle(case) for case in cases])
        print(prepared_cases)
        return self.artifacts.linearregression.predict(prepared_cases)
