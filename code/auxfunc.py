import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import vstack as csr_vstack
from collections import Counter
# from core import Model


def vstack(a, b):
    result = None
    if type(a) == np.ndarray:
        result = np.vstack([a, b])
    elif type(a) == csr_matrix:
        result = csr_vstack([a, b])
    else:
        raise TypeError("""Dataset X type not support, must be numpy.ndarray
                        or scipy.sparse.csr_matrix""")
    return result


# class CommitteeModel(Model):
#     def __init__(self, models):
#         self.models = models

#     def fit(self, X, y):
#         for model in self.models:
#             model.fit(X, y)

#     def predict(self, X):
#         predicts = []
#         for model in self.models:
#             predicts.append(model.predict(X))


#     def predict_proba(self, X):
#         predicts = []
#         for model in self.models:
#             predicts.append(model.predict_proba(X))

#         result = []
#         for j in range(len(predicts[0])):
#             proba = []
#             for i in range(len(predicts[0][0])):
#                 suma = 0
#                 for k in range(len(predicts)):
#                     suma += predicts[k][j][i]
#                 proba.append(suma / len(predicts))
#             result.append(proba)

#         return result

#     def score(self, X, y):
#         return

#     def predict_commitee(self, X):
#         pass

#     def predict_proba_committee(self, X):
#         result = []
#         for model in self.models:
#             result.append(model.predict_proba(X))

#         return result

#     @staticmethod
#     def reorder(predicts):
#         result = []
#         for j in range(len(predicts[0])):
#             elem = []
#             for i in range(len(predicts[0][0])):
#                 ci = []
#                 for k in range(len(predicts)):
#                     ci.append(predicts[k][j][i])
#                 elem.append(ci)
#             result.append(elem)

#         return result
