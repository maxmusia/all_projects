import random
import pandas as pd
import numpy as np


class MyLogReg:
    def __init__(self, weights=np.array([]), n_iter=14, learning_rate=0.1 ):
        self.n_iter = n_iter
        self.learning_rate = learning_rate
        self.weights = weights

    def __str__(self):
        return f"{self.__class__.__name__} class: n_iter={self.n_iter}, learning_rate={self.learning_rate}"

    def fit(self, X, y, verbose=False):
        self.y = y
        self.X = X
        self.verbose = verbose
        rows, col = self.X.shape
        self.X.insert(0, None, np.ones(rows))
        self.weights = np.ones(self.X.shape[1])

        for i in range(1, self.n_iter + 1):
            y_ = 1/(1+np.exp(-self.X@self.weights))
            grad = self.X.T@(y_ - y)/rows
            self.weights -= self.learning_rate * grad

        self.mean_weight = self.weights.to_numpy()[1:].mean()


    def predict_proba(self, X):


        y_ = 1 / (1 + np.exp(-X @ self.weights))
        self.mean_y_ = y_.mean()
        return self.mean_y_

    def predict(self, X):


        y_ = 1 / (1 + np.exp(-X @ self.weights))
        self.sum_y_ = int(sum(y_))
        return self.sum_y_






    def get_coef(self):
        return self.mean_weight


from sklearn.datasets import make_regression

X, y = make_regression(n_samples=400, n_features=14, n_informative=5, noise=15, random_state=42)
X = pd.DataFrame(X)
y = pd.Series(y)
X.columns = [f'col_{col}' for col in X.columns]


g = MyLogReg()
#print(g.__str__())
g.fit(X, y)
#print(g.get_coef())
print(g.predict(X))
print(g.predict_proba(X))
