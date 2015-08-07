__author__ = 'Daniel Puschmann'


def chooseRandomIndex(weights, random):
    sumProb = sum(weights)
    val = random.random() * sumProb
    idx = 0
    summation = 0.0
    while summation <= val and idx < len(weights):
        summation += weights[idx]
        idx += 1
    return idx - 1
