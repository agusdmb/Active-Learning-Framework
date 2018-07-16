import unittest

import numpy as np

from core import Dataset
import querys


class TestDataset(unittest.TestCase):
    def setUp(self):
        X = np.arange(12).reshape(4, 3)
        y = np.array([0, 1, 2, 3])
        X_unlabeled = np.arange(12, 24).reshape(4, 3)
        self.dataset = Dataset(X, y, X_unlabeled)

    def test_tag_elements(self):
        X1 = self.dataset.get_X()
        y1 = self.dataset.get_y()
        unlabeled1 = self.dataset.get_unlabeled()

        self.dataset.tag_elements([0], [4])

        X2 = self.dataset.get_X()
        y2 = self.dataset.get_y()
        unlabeled2 = self.dataset.get_unlabeled()

        self.assertEqual(X1.shape[0] + 1, X2.shape[0])
        self.assertEqual(y1.shape[0] + 1, y2.shape[0])
        self.assertEqual(unlabeled1.shape[0], unlabeled2.shape[0] + 1)

        self.assertNotIn(unlabeled1[0], X1)
        self.assertIn(unlabeled1[0], X2)


class Model:
    def predict_proba(self, data):
        return data


class TestSelectors(unittest.TestCase):
    def setUp(self):
        self.data = [
            [1., 0., 0.],
            [0.3, 0.3, 0.4],
            [0., 0., 1.],
            [0.32, 0.32, 0.36],
            [0.5, 0.5, 0]
        ]
        self.m = Model()

    def test_uncertity(self):
        un = querys.UncertaintySelector()
        selected = un.select(self.m, self.data, 2)
        self.assertEqual(selected, [3, 1])

    def test_certity(self):
        ce = querys.CertaintySelector()
        selected = ce.select(self.m, self.data, 2)
        self.assertEqual(selected, [0, 2])

    def test_mindiff(self):
        mi = querys.MinDiffSelector()
        selected = mi.select(self.m, self.data, 2)
        self.assertEqual(selected, [4, 3])

    def test_entropy(self):
        en = querys.EntropySelector()
        selected = en.select(self.m, self.data, 2)
        self.assertEqual(selected, [3, 1])


if __name__ == '__main__':
    unittest.main()
