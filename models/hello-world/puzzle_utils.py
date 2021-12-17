import numpy as np


def get_category(char: str) -> int:
    if char == ".":
        return 0
    else:
        return int(char)


def prepare_puzzle(puzzle: str) -> np.ndarray:
    return np.array([get_category(char) for char in puzzle])