# coding: utf-8
# Author: Kevin Zhou
# Mail  : evilpsycho42@gmail.com
# Time  : 10/18/18

import numpy as np
from sklearn.metrics import pairwise
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


__all__ = ["KernelKMeans", "KMeans"]


class KernelKMeans(object):

    def __init__(self,
                 n_clusters=8,
                 max_iter=300,
                 kernel=pairwise.linear_kernel):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.kernel = kernel

    def _initialize_cluster(self, X):
        self.N = np.shape(X)[0]
        self.y = np.random.randint(low=0, high=self.n_clusters, size=self.N)
        self.K = self.kernel(X)

    def fit_predict(self, X):
        self._initialize_cluster(X)
        for _ in range(self.max_iter):
            obj = np.tile(np.diag(self.K).reshape((-1, 1)), self.n_clusters)
            N_c = np.bincount(self.y)
            for c in range(self.n_clusters):
                obj[:, c] -= 2 * \
                    np.sum((self.K)[:, self.y == c], axis=1) / N_c[c]
                obj[:, c] += np.sum((self.K)[self.y == c][:, self.y == c]) / \
                    (N_c[c] ** 2)
            self.y = np.argmin(obj, axis=1)
        return self.y