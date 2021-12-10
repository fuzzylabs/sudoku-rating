# Sudoku Rating Modelling

## Aims
We want to model sudoku solver rating and difficulty. We start with classic sudoku, with the intention of extending it to different sudoku variants.

## Requirements
* Python 3.7+
* [Pyenv](https://github.com/pyenv)
  * Pyenv can;t be installed using pip see the [installation docs](https://github.com/pyenv/pyenv#installation)
* [Pipenv](https://pypi.org/project/pipenv/)
* [dvc](https://dvc.org/doc/install/)

## Getting started
Set up python environment, and install dependencies
```
pipenv install
```

Pull data from DVC remote storage, DagsHub
```
dvc pull
```

If you want to push data to DagsHub, you need to set up authentication:
```
dvc remote modify origin --local auth basic
dvc remote modify origin --local user <DagsHub-user-name>
dvc remote modify origin --local password <Token>
```