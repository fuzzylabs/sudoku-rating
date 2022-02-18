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

## Experiment tracking
You can view experiments by running (it will open the browser window):
```
guild view
```

You can pull runs performed on other machines from S3:
```
guild pull REMOTE_NAME
```

You can push runs performed on your machine to the remote, so they are available to your collaborators:
```
guild push REMOTE_NAME
```

## GuildAI remote configuration
To push to and pull from the remote storage (AWS S3) you need to configure guild with the S3 remote. The example configuration is as follows:
```
remotes:
  sudoku-s3:
    type: s3
    bucket: sudoku-rating-guildai
    root: runs
    region: eu-west-2
```

Adjust the configuration to reflect your environment. For more details see [GuildAI docs](https://my.guild.ai/t/remotes/171)

## Serving
The model is served with BentoML docker container.

To pack the model artifact for bento:
```
python bento-packer.py
```

To serve the model with BentoML:
```shell
bentoml serve ./serving.py:svc --reload
```

To turn the bento into a docker image:
```shell
bentoml containerize linear_regression:latest
```

To run that docker image:
```shell
docker run -p 127.0.0.1:5000:5000 --rm linear_regression:<Image ID>
```

This is an example cURL command that will query the model for the given sudoku values
```shell
curl --request POST \
  --url "localhost:5000/predict" \
  --header 'content-type: application/json' \
  --data '[
  "1..5.37..6.3..8.9......98...1.......8761..........6...........7.8.9.76.47...6.312",
  "...81.....2........1.9..7...7..25.934.2............5...975.....563.....4......68."
]'
```

To run the Web UI (built with `streamlit`):
```
streamlit run ui.py
```