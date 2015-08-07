__author__ = 'Daniel Puschmann'


class Centroid(object):

    def __init__(self, centre, label, std, weight):
        self.centre = centre
        self.label = label
        self.std = std
        self.weight = weight