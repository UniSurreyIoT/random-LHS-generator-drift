# random-LHS-generator-drift

We introduce a novel way of generating data streams with data drift. The drift is introduced both by shifting 
the centroids in randomised intervals and by changing the data distribution function used to randomly draw the
data from the centroids. Here we can scale up the dimensionality of the generated data, with each feature having
its own distribution to draw the data from.
The centroids are selected through Latin Hypercube Sampling (LHS) [1]. The number of clusters and dimensions
are fixed beforehand. Similar to the method be- fore, each centroid is assigned with a standard deviation and
weight. Furthermore, each dimension is given a distribution function, which later is used to generate the data
samples.
Considering that each dimension represents a feature of a data stream, this models the fact that in IoT
applications we are dealing with largely heterogeneous data streams in which the features do not follow the same
data distribution. Our current implementation supports triangular, Gaussian, exponential, and Cauchy
distributions. The implementation is easily expandable and can support other common or custom distributions.

[1] McKay, M. D., Beckman, R. J., Conover, W. J. ”Comparison of three methods for selecting values of input variables in the analysis of output from a computer code.” Technometrics vol. 21, no. 2, pp. 239-245, 1979.