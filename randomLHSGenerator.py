__author__ = 'Daniel Puschmann'
from random import Random
from pprint import pformat
from math import sqrt

from pyDOE import lhs

from centroid import Centroid
from utils import chooseRandomIndex
from arffWriter import write_data, write_header


class RandomLHSGenerator(object):

    def __init__(self, random_seed_generation=1, dimensions=10, centre_num=10,
                 sample_limit=None, class_num=2,
                 hyper_cube_length=500, variance=1, file_name=None,
                 stream_name='LHSData', criterion='maximin', distribution='gauss'):
        self.rand_generate = Random()
        self.rand_generate.seed(random_seed_generation)
        self.random_seed_generation = random_seed_generation
        self.class_num = class_num
        self.distributions = {'gauss': self.rand_generate.gauss, 'expovariate': self.rand_generate.expovariate,
                              'triangular': self.rand_generate.triangular, #'uniform': self.rand_generate.uniform,
                              } #'cauchy': self.rand_generate}
        self.supported_distributions = self.distributions.keys()
        self.number_of_distributions = len(self.supported_distributions)
        self.feature_distributions = [distribution for i in xrange(dimensions)]
        self.attributes = ['attribute%i' %i for i in xrange(dimensions)]
        self.attributes.append('class')
        self.centre_num = centre_num
        self.criterion = criterion
        self.dimensions = dimensions
        self.variance = variance
        self.sample_limit = sample_limit
        self.samples_produced = 0
        self.weights = []
        self.hyper_cube_length = hyper_cube_length
        self.features = ["attribute%i" % i for i in xrange(dimensions)]
        self.iteration = 0
        self.file_name = file_name
        if self.file_name is not None:
            write_header(stream_name, self.attributes, self.file_name)


    def __iter__(self):
        return self

    def restart(self):
        self.rand_generate = Random()
        self.rand_generate.seed(self.random_seed_generation)

    def generateCentroids(self):
        if self.dimensions<self.centre_num:
            centres = lhs(self.dimensions, samples=self.centre_num, criterion=self.criterion)
        else:
            centres = lhs(self.dimensions, criterion=self.criterion)
            centres = centres[:self.centre_num]
        for i, centre in enumerate(centres):
            centres[i] = map(lambda x: x*self.hyper_cube_length, centre)
        std = sqrt(self.variance)
        weight = 1
        self.weights = [1 for i in xrange(self.centre_num)]
        self.centroids = [Centroid(centre, i, std, weight) for i, centre in enumerate(centres)]

    def next(self):
        if self.sample_limit==None or self.samples_produced <= self.sample_limit:
            self.iteration += 1
            self.iteration %= 2010
            #this solves the problem of int overflow in case we want the data stream to go on infinite
            if self.sample_limit is not None:
                self.samples_produced += 1
            label = chooseRandomIndex(self.weights, self.rand_generate)
            centroid = self.centroids[label]
            point = {feature: self.draw_from_distribution(self.feature_distributions[dimension], centre, self.variance) / self.hyper_cube_length
                     for feature, dimension, centre in zip(self.features, range(self.dimensions),centroid.centre)}

            # points = zeros((self.centre_num, self.dimensions))
            # for i in xrange(self.dimensions):
            #     points[:, i] = self.draw_from_distribution(self.distribution, self.centroids[:, i], self.variance)
            # if self.file_name is None:
            #     for i, val in enumerate(points):
            #         write_data(val, i, self.file_name)
            if self.file_name is not None:
                write_data(point.values(), label, self.file_name)
            return {'label': label, 'point': point}
        else:
            raise StopIteration()


    def draw_from_distribution(self, distribution, mean, std):
        if distribution is 'gauss':
            return self.distributions[distribution](mean, std)
        if distribution is 'expovariate':
            return self.distributions[distribution](1/mean)
        if distribution is 'triangular':
            return self.distributions[distribution](mean-1.5*std, mean+1.5*std)
        raise Exception('Distribution %s is currently not supported. Supported distributions are: %s'
                        % (distribution, pformat(self.distributions)))




