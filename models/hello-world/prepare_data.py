from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from puzzle_utils import prepare_puzzle

from tqdm.auto import tqdm
tqdm.pandas()


def prepare():
    df = pd.read_csv("../../data/sudoku-3m.csv")
    puzzles = np.stack(df.puzzle.progress_apply(prepare_puzzle).values)
    prepared_df = pd.DataFrame(puzzles, columns=[f"digit_{x}"for x in range(puzzles.shape[1])])

    prepared_df.loc[:, ["clues", "difficulty"]] = df.loc[:, ["clues", "difficulty"]]

    train_df, test_df = train_test_split(prepared_df)
    train_df.to_csv("../../data/sudoku-3m-train.csv", index=False)
    test_df.to_csv("../../data/sudoku-3m-test.csv", index=False)


if __name__ == "__main__":
    prepare()
