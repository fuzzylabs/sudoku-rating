# Sudoku Rating Modelling

## Aims
We want to model sudoku solver rating and difficulty. We start with classic sudoku, with the intention of extending it to different sudoku variants.

## Requirements
* Python 3.7+
* [Pyenv](https://github.com/pyenv)
  * Pyenv can;t be installed using pip see the [installation docs](https://github.com/pyenv/pyenv#installation)
* [Pipenv](https://pypi.org/project/pipenv/)
* [dvc](https://dvc.org/doc/install/)
* [Guild.AI](https://my.guild.ai/t/get-started-with-guild-ai/35)

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

## Training Linear model
There's a linear model training code in `models/hello-world`. The code can be run with Guild.AI to track the experiment:
```
guild run train
```

If you want to override hyperparameters (i.e. alpha), you can specify them as command line arguments:
```
guild run train alpha=0.1
```

For more details on hyperparameter optimision with Guild.AI, see [the documentation](https://my.guild.ai/t/get-started-optimize-a-model/41)