from abc import ABC, abstractmethod

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split

import auxfunc


class Oracle(ABC):
    @property
    @abstractmethod
    def target_names(self):
        """ List of target names """
        return

    def ask(self, readable_X, recoms):
        assert len(readable_X) == len(recoms), \
            "readable_X and recoms must have same size"
        result = []
        for i, elem in enumerate(readable_X):
            answer = self.ask_for_element(elem, recoms[i])
            result.append(answer)
        return result

    def show_element(self, x, recom):
        print("Instance\n========\n")
        print(x)
        print("\nLabel predicted\n===============")
        print(recom, '-', self.target_names[recom])

    def show_options(self):
        print("\nOptions\n=======")
        for i in range(len(self.target_names)):
            print(i, '-', self.target_names[i])

    def ask_for_element(self, x, recom):
        self.show_element(x, recom)
        self.show_options()
        answer = None
        while not (answer in range(len(self.target_names)) or answer == -2):
            if answer is not None:
                print("Invalid answer")
            answer = self.validate_answer(input("Your answer: "))
        return answer

    @staticmethod
    def validate_answer(answer):
        try:
            answer = int(answer)
        except ValueError:
            answer = -1
        return answer


class Dataset:
    def __init__(self, X, y, X_unlabeled, test_size=0.2, random_state=7):
        """
        X: Can be an numpy.ndarray or a scipy.sparse.csr_matrix
        y: Must be a numpy.ndarray
        X_unlabeled: Same type as X
        """
        assert isinstance(X, (np.ndarray, csr_matrix)), \
            "X must be numpy.ndarray or a sparse"
        assert type(X) == type(X_unlabeled),  \
            "X and X_unlabeled must be same type"
        assert isinstance(y, np.ndarray), "'y' type must be numpy.ndarray"

        # leave some tagged data for testing
        X_train, self.X_test, y_train, self.y_test = self._split_X(
            X, y, test_size, random_state)

        self.X = auxfunc.vstack(X_train, X_unlabeled)

        self.lenX = len(y_train)
        y_unlabeled = np.array([-1] * X_unlabeled.shape[0])
        self.y = np.hstack([y_train, y_unlabeled])

    @staticmethod
    def _split_X(X, y, test_size, random_state):
        splited_data = train_test_split(X, y, test_size=test_size,
                                        random_state=random_state)
        return splited_data

    def tag_elements(self, indices, tags):
        assert len(indices) == len(tags), \
            "Not the same numbers of indices and tags"
        r_indices = self._get_unlabeled_indices()
        for i, elem in enumerate(indices):
            r_i = r_indices[elem]
            self.y[r_i] = tags[i]

    def _get_unlabeled_readable(self, i):
        indices = self._get_unlabeled_indices()
        index = indices[i]
        index_unlabeled = index - self.lenX
        return self.get_unlabeled_readable(index_unlabeled)

    def get_unlabeled_readable(self, i):
        """ The output of this method is passed to the Oracle. """
        return self.get_X_unlabeled()[i]

    def get_X(self):
        return self.X[self._get_train_indices()]

    def get_y(self):
        return self.y[self._get_train_indices()]

    def get_X_unlabeled(self):
        return self.X[self.lenX:]

    def get_unlabeled(self):
        return self.X[self._get_unlabeled_indices()]

    def _get_train_indices(self):
        return np.where(self.y >= 0)[0]

    def _get_unlabeled_indices(self):
        return np.where(self.y == -1)[0]


class Model(ABC):
    @abstractmethod
    def fit(self, X, y):
        return

    @abstractmethod
    def predict(self, X):
        return

    @abstractmethod
    def predict_proba(self, X):
        return

    @abstractmethod
    def score(self, X, y):
        return


class Selector(ABC):
    @abstractmethod
    def select(self, model, data, n, *args, **kwargs):
        return


class ActiveLearner:
    def __init__(self, model, dataset, selector, oracle):
        self.model = model
        self.selector = selector
        self.dataset = dataset
        self.oracle = oracle
        self.scores = []

    def fit(self):
        self.model.fit(self.dataset.get_X(), self.dataset.get_y())
        self._test()

    def select(self, n):
        X_unlabeled = self.dataset.get_unlabeled()
        if X_unlabeled.shape[0] < n:
            n = X_unlabeled.shape[0]
        if n == 0: return []
        selected = self.selector.select(self.model, X_unlabeled, n)
        return selected

    def ask(self, indices):
        if len(indices) == 0: return []
        recoms = self.model.predict(self.dataset.get_unlabeled()[indices])
        readable_X = [self.dataset._get_unlabeled_readable(i) for i in indices]
        result = self.oracle.ask(readable_X, recoms)
        return result

    def tag_elements(self, indices, y):
        """ Keyword arguments:
        indices -- is a list of index of unlabeled.X
        y -- is the target of each of those X
        """

        self.dataset.tag_elements(indices, y)

    def _test(self):
        result = self.model.score(self.dataset.X_test, self.dataset.y_test)
        self.scores.append(result)
        return result

    def get_scores(self):
        return self.scores

    def change_selector(self, selector):
        self.selector = selector
