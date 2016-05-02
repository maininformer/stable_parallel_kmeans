from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import pathos.multiprocessing as mp
import copy
import time

class SKMeans(object):

    def __init__(self, data, k_max, percent_subsampling, number_of_subsamples):
        self.data = data
        self.k_max = k_max
        self.percent_subsampling = percent_subsampling
        self.number_of_subsamples = number_of_subsamples
        self.scores = scores = dict((k,copy.deepcopy([])) for k in range(2,k_max))

    def fit(self, n_jobs = 1, verbose = True):
        pool = mp.ProcessingPool(processes=n_jobs)
        for k in range(2,self.k_max):
            t = time.time()
            for iteration in range(max(int(self.number_of_subsamples/n_jobs), 1)):
                # max becasuse if number of subsamples is smaller than jobs all will be 0
                #the fact that not everyprocess is entering its own score might be a bottle neck

                self.scores[k].extend(pool.map(self._loop,[k for i in range(n_jobs)]))

            if verbose:
                print "K={0} done in {1:.2f} seconds \n".format(k,time.time()-t)


    def _loop(self,k):
        subsample_1 = self.subsample()
        subsample_2 = self.subsample()

        C = self.intersect(subsample_1,subsample_2)

        labels_1 = self.cluster(subsample_1, k)
        labels_2 = self.cluster(subsample_2, k)

        common_labels_1, common_labels_2 = self.find_common_elements(C, labels_1, labels_2)

        labels_score_1 = self.intersect_labels(common_labels_1)
        labels_score_2 = self.intersect_labels(common_labels_2)

        score = self.do_cosine(labels_score_1, labels_score_2)

        #self.scores[k].append(score)
        return score


    def subsample(self):
        """First call this, Input: data and percent to subsample, returns random subsample"""
        random_indices = np.random.randint(0,len(self.data), int(self.percent_subsampling*len(self.data)))
        return self.data[random_indices]


    def cluster(self, X, k):
        """Second run this, Clusters X into K clusters and returns their labels"""
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        return kmeans.labels_


    #Tested works
    def intersect(self, subsample_1 , subsample_2):
        """Second you can also run this, finds the interesction of two subsamples, tested and works.
           Input: Intersections, returns, a binary matrix, one where the element with index of subsample_1 on each row is the same
           as the element with index of subsample_2 on each column"""

        assert np.shape(subsample_1)==np.shape(subsample_2), 'subsamples have different shapes'
        C = np.zeros(shape=(np.shape(subsample_1)[0],np.shape(subsample_1)[0]))
        for i,s1 in enumerate(subsample_1):
            for j,s2 in enumerate(subsample_2):
                if np.sum(np.equal(s1,s2))==np.shape(subsample_1)[1]: #This will happen if all the columns are 1 i.e. [True, True, True]
                    C[i][j] = 1
        return C



    def find_common_elements(self, C, labels_1, labels_2):
        """Third: computes two 1-d arrays, each array has indices that will yield the same element, if used to query the
        parent subsample, in other words the locations where that element is repeated. Once that is calculated, it will
        return the labels corresponding to each of those elements."""
        #will return rows and columns where C is one, i.e which elements in the parent matrices were together
        here = np.where(C==1)
        #The clustered points will be in the same order because of the here_matrix
        labels_1_ = labels_1[here[0]]
        labeld_2_ = labels_2[here[1]]
        return labels_1_, labeld_2_


    #make a clustered with itself on cluster_1 and cluster_2 and then compute the similarities
    def intersect_labels(self, labels):
        """Fourth: use the labels from find_common_elements here to see who are clustered together"""
        label_score = np.zeros(shape=(len(labels),len(labels)))
        for i, label_i in enumerate(labels):
            for j, label_j in enumerate(labels):
                if label_i == label_j:
                    if i!=j:
                        label_score[i][j] = 1
        return label_score



    def do_cosine(self, intersect_labels_1, intersect_labels_2):
        numerator = np.sum(np.multiply(intersect_labels_1, intersect_labels_2))
        denominator = np.sum(np.multiply(
                                         intersect_labels_1,
                                         intersect_labels_1))*np.sum(np.multiply(intersect_labels_2,
                                                                                 intersect_labels_2))
        return numerator/(denominator)**0.5
