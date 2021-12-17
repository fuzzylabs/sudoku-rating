import bentoml
import numpy as np
from bentoml import BentoService, api
from bentoml.adapters import JsonInput, JsonOutput
from bentoml.frameworks.sklearn import SklearnModelArtifact
from puzzle_utils import prepare_puzzle


@bentoml.env(infer_pip_packages=True)
@bentoml.artifacts([SklearnModelArtifact('linearregression')])
class SudokuRating(BentoService):

    # TODO a schemata
    @api(input=JsonInput(), output=JsonOutput())
    def predict(self, cases):
        prepared_cases = np.vstack([prepare_puzzle(case) for case in cases])
        print(prepared_cases)
        return self.artifacts.linearregression.predict(prepared_cases)
