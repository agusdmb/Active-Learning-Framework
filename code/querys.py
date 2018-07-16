from heapq import nlargest, nsmallest
from math import log
from random import sample

from core import Selector


class UncertaintySelector(Selector):
    @staticmethod
    def select(model, data, n):
        probs = model.predict_proba(data)
        worst_probs = [(i, max(probs[i])) for i in range(len(probs))]
        worst_probs_sorted = sorted(worst_probs, key=lambda x: x[1])
        result = [i[0] for i in worst_probs_sorted][:n]
        return result


class CertaintySelector(Selector):
    @staticmethod
    def select(model, data, n):
        probs = model.predict_proba(data)
        worst_probs = [(i, max(probs[i])) for i in range(len(probs))]
        worst_probs_sorted = sorted(worst_probs, key=lambda x: x[1])
        result = [i[0] for i in worst_probs_sorted][-n:]
        return result


class MinDiffSelector(Selector):
    @staticmethod
    def select(model, data, n):
        probs = model.predict_proba(data)
        diffs = []
        for i, prob in enumerate(probs):
            fst, snd = nlargest(2, prob)
            diffs.append((i, fst - snd))
        result = nsmallest(n, diffs, key=lambda x: x[1])
        return [i[0] for i in result]


class EntropySelector(Selector):
    @staticmethod
    def select(model, data, n):
        probs = model.predict_proba(data)
        sums = []
        for i, prob in enumerate(probs):
            suma = 0
            for value in prob:
                # log of 0 it doesnt exist
                if value != 0:
                    suma -= value * log(value)
            sums.append((i, suma))
        result = nlargest(n, sums, key=lambda x: x[1])
        return [i[0] for i in result]


class RandomSelector(Selector):
    @staticmethod
    def select(model, data, n):
        return sample(range(data.shape[0]), n)
