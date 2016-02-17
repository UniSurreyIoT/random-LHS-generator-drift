__author__ = 'Daniel Puschmann'


from randomLHSGenerator import RandomLHSGenerator
from random import Random

class RandomLHSGeneratorDrift(RandomLHSGenerator):

    def __init__(self, speed=1, random_seed_generation=1, dimensions=10, center_num=10,
                 sample_limit=None, class_num=2,
                 hyper_cube_length=500, variance=60, file_name = None,
                 stream_name='LHSData', criterion='maximin', distribution='gauss'):
        super(RandomLHSGeneratorDrift, self).__init__(random_seed_generation, dimensions,
                                                 center_num, sample_limit, class_num,
                                                 hyper_cube_length, variance, file_name,
                                                 stream_name, criterion, distribution)
        self.speed = speed
        self.generateCentroids()
        self.rand_model = Random()
        self.drift_times = [self.rand_model.randint(50, 2000) for i in xrange(dimensions)]



    def change_distribution(self, distribution):
        self.feature_distributions = distribution


    def shift_centroid(self):
        for centre_num, centre in enumerate(self.centroids.centres):
            for dimension, value in enumerate(centre):
                if self.iteration > self.drift_times[dimension]:
                    if self.rand_model.randint(0, 1) is 1:
                        #shift centre of feature
                        self.centroids.centres[centre_num] = self.rand_model.random() * self.hyper_cube_length

                    if self.rand_model.randint(0, 1) is 1:
                        #shift distribution
                        self.feature_distributions[dimension] = self.supported_distributions[self.rand_model.randrange(0, self.number_of_distributions)]



if __name__ == '__main__':
    features = [2,3,4,5]
    file_names = ["LHSGeneratedK100F%i" % f for f in features]
    limit = 100000
    for f, fname in zip(features, file_names):
        stream = RandomLHSGeneratorDrift(file_name=fname, sample_limit=limit, center_num=100, dimensions=f)
        for i, instance in enumerate(stream):
            if i % 10000 == 0:
                print "Instance: %i" % i
