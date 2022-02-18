# Sudoku Rating Modelling

## Aims
We want to model sudoku solver rating and difficulty. We start with classic sudoku, with the intention of extending it to different sudoku variants.

## Requirements
* Python 3.7+
* [Pyenv](https://github.com/pyenv)
  * Pyenv can't be installed using pip see the [installation docs](https://github.com/pyenv/pyenv#installation)
* [Pipenv](https://pypi.org/project/pipenv/)
* [dvc](https://dvc.org/doc/install/)
* [Guild.AI](https://my.guild.ai/t/get-started-with-guild-ai/35)
* [kubectl](https://kubernetes.io/docs/tasks/tools/)
* [helm](https://helm.sh/docs/intro/install/)
* Kubernetes cluster with [Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/nav/installation.html) installed; instructions for setting up locally are provided below

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

## Deployment
### Setting up Seldon Core locally (optional)
Note: for other ways of installing Seldon Core look at [the installation documentation](https://docs.seldon.io/projects/seldon-core/en/latest/nav/installation.html).

Firstly, install [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation) and create a cluster:
```
cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
EOF
```

We also need install [Ambassador](https://www.getambassador.io/docs/edge-stack/latest/tutorials/getting-started/) to be used as an Ingress Controller:
```
kubectl apply -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-crds.yaml

kubectl apply -n ambassador -f https://github.com/datawire/ambassador-operator/releases/latest/download/ambassador-operator-kind.yaml
kubectl wait --timeout=180s -n ambassador --for=condition=deployed ambassadorinstallations/ambassador
```

We can now install Seldon Core:
```
kubectl create namespace seldon-system

helm install seldon-core seldon-core-operator \
    --repo https://storage.googleapis.com/seldon-charts \
    --set usageMetrics.enabled=true \
    --set ambassador.enabled=true \
    --namespace seldon-system
	
kubectl get pods -n seldon-system

kubectl port-forward -n ambassador svc/ambassador 8080:80
```

### Model deployment

First, we need to upload the model artifact `models/hello-world/linearregression.joblib` to a compatible remote storage (e.g. Google Storage or S3). Filename in the remote storage must be `model.joblib`.

Next, we need to replace the `modelUri` in `models/hello-world/seldon/model.yaml` with a path to the directory containing the model artifact. The file in the repository already, points to a public bucket containing a pre-trained model, that you can use.

Finally, we can deploy the model by running this command in `models/hello-world` directory:
```
kubectl apply -f seldon/model.yaml
```

Swagger UI should now be available here: [http://localhost/seldon/seldon/sudoku-model/api/v1.0/doc/](http://localhost/seldon/seldon/sudoku-model/api/v1.0/doc/)

An inference request can be made as follows:
```
curl -X POST http://localhost/seldon/seldon/sudoku-model/api/v1.0/predictions \
    -H 'Content-Type: application/json' \
    -d '{ "data": { "ndarray": [[0,0,0,5,0,0,0,1,0,6,0,0,0,0,9,0,0,2,0,0,0,3,0,0,4,0,0,5,0,0,0,0,0,2,0,7,2,0,0,9,0,0,0,4,1,0,0,4,0,0,3,8,0,0,9,0,0,0,0,1,0,0,5,0,0,0,7,0,0,0,0,0,3,1,0,0,6,5,0,9,0]] } }'
```

### Server monitoring
To add service monitoring with Promethius and Grafana, such as request and error rates:
```
helm install seldon-core-analytics seldon-core-analytics \
   --repo https://storage.googleapis.com/seldon-charts \
   --namespace seldon-system
```

Add port-forwarding as follows:
```
kubectl port-forward svc/seldon-core-analytics-grafana 3000:80 -n seldon-system
```

The Grafana dashboard will be available at [http://localhost:3000/dashboard/db/prediction-analytics](http://localhost:3000/dashboard/db/prediction-analytics).
