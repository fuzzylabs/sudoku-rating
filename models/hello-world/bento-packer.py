from joblib import load
from bentoml import sklearn, models

model = load("linearregression.joblib")

tag = sklearn.save("linear_regression", model)

print(f"Saved with metadata: {models.get(tag)}")
