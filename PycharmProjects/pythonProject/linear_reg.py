import random
import pandas as pd
import numpy as np

class MyLineReg:
    def __init__(self, weights=np.array([]), metric=None, reg=None, l1_coef=(0, float), l2_coef=(0, float), n_iter=100, learning_rate=lambda iter: 0.5 * (0.85 ** iter), sgd_sample=0.1, random_state=42):
        self.metric = metric
        self.reg = reg
        self.l1_coef = l1_coef
        self.l2_coef = l2_coef
        self.n_iter = n_iter
        self.learning_rate = learning_rate
        self.weights = weights
        self.random_state = random_state
        self.sgd_sample = sgd_sample
    def __str__(self):
        return f"{self.__class__.__name__} class: n_iter={self.n_iter}, learning_rate={self.learning_rate}"

    def fit(self, X, y, verbose = False):
        self.y = y
        self.X = X
        self.verbose = verbose
        rows, col = X.shape
        X.insert(0, None,  np.ones(rows))
        self.weights = np.ones(X.shape[1])

        random.seed(self.random_state)

        for i in range(1, self.n_iter+1):
            l1_loss = self.l1_coef * sum(abs(self.weights))
            l1_grad = self.l1_coef * np.sign(self.weights)
            l2_loss = self.l2_coef * sum(self.weights ** 2)
            l2_grad = 2 * self.l2_coef * self.weights
            reg_var = {'l1': (l1_loss, l1_grad), 'l2': (l2_loss, l2_grad),
                       'elasticnet': (l1_loss + l2_loss, l1_grad + l2_grad)}
            if self.reg is not None:
                self.l_loss = reg_var[self.reg][0]
                self.l_grad = reg_var[self.reg][1]
            else:
                self.l_loss, self.l_grad = 0, 0

            if self.sgd_sample is None:

                y_ = X@self.weights
                grad = 2*(X.T@(y_ - y))/rows + self.l_grad
            else:
                if type(self.sgd_sample) != int:
                    self.sgd_sample = round(X.shape[0] * self.sgd_sample)
                self.sample_rows_idx = random.sample(range(X.shape[0]), self.sgd_sample)
                self.Sample = X.iloc[self.sample_rows_idx, :]
                self.vector = self.y.iloc[self.sample_rows_idx]
                y_ = self.Sample@self.weights
                grad = 2 * (self.Sample.T@(y_ - self.vector)) / self.sgd_sample + self.l_grad

            if callable(self.learning_rate):
                LR = self.learning_rate(i)
                self.weights -= LR * grad
            else:
                self.weights -= self.learning_rate*grad

        y_ = X @ self.weights
        self.mse = sum((y - y_) ** 2 / rows)
        self.mae = sum(abs(y - y_) / rows)
        self.rmse = self.mse**0.5
        self.mape = sum(abs((y - y_) / y) * 100 / rows)
        self.r2 = 1 - sum((y - y_) ** 2)/sum((y - y.mean()) ** 2)
        self.wsum = sum(self.weights.to_numpy()[1:])
        self.mean = self.weights.to_numpy()[1:].mean()



    def get_coef(self):
        return self.mean


    def predict(self, X):
        #X.insert(0, None, np.ones(X.shape[0]))
        y_ = X@self.weights
        return sum(y_)

    def get_best_score(self):
        return self.__getattribute__(self.metric)


from sklearn.datasets import make_regression

X, y = make_regression(n_samples=1000, n_features=14, n_informative=10, noise=15, random_state=42)
X = pd.DataFrame(X)
y = pd.Series(y)
X.columns = [f'col_{col}' for col in X.columns]


g = MyLineReg(metric = 'mse', reg = None, l1_coef= 0.8 , l2_coef = 0.7 )
g.fit(X, y)
print(g.get_coef())
print(g.predict(X))
#print(g.__str__())
print(g.get_best_score())
