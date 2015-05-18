#!/usr/bin/env python
"""

Class that constructs a MultiplexMarkovchain given the counts. Also
has methods to get the null model and the parameters of the
probability distribution associated with the Markov chain. Currently
handles only 4-state Markov chains (i.e. two layer networks).

"""
from __future__ import division
import numpy as np
from warnings import warn


class MarkovChain(object):
    """
    A class that computes properties of a Markov chain such as the
    transition parameters and standard deviation. The class assumes a
    uniform prior for the distribution of transition parameters.

    Each state of the Markov chain has a Dirichlet (multivariate beta)
    distribution whose variates are the transition parameters. The
    transition parameters are estimated as the mean of the
    corresponding Dirichlet distribution.

    Parameters
    ----------

    counts : Counts for each transition of the Markov chain. Numpy
    array or list with number of entries matching the number of transitions.

    num_transitions : The number of transitions in the Markov
    chain. The number of states of the Markov chain is sqrt(num_transitions).

    state_totals : The total of counts leaving from the particular
    state of the Markov chain. len(state_totals) is equal to the
    number of states of the Markov chain. Can be accessed using the
    method `get_state_totals`.

    params : The average value of the probability of the transitions
    assuming a uniform prior. The `i`th entry is interpreted as the
    probability of the `i`th transition. Can be accessed using the
    method `get_parameters`.

    std : The standard deviations of the variates of the Dirichlet
    distributions associated with the Markov chain. The `i`th entry is
    the standard deviation associated with the `i`th transition
    parameter. Can be accessed using the method `get_std_dev`.

    """

    def __init__(self, counts):
        counts = np.array(counts)
        self.counts = counts
        self.params = None # probability of transitions
        self.std = None # std. associated with the transitions
        self.state_totals = None #total number of transitions leaving a state
        self.num_transitions = len(counts)

    def compute_prob_params(self,counts):
        """
        Given counts returns the mean, std. dev. for every transition
        and normalization constant for each state.
        """
        num_transitions  = self.num_transitions
        l = int(np.sqrt(num_transitions)) # number of states in the MC
        totals = np.zeros(l)
        mu = np.zeros(num_transitions)
        sigma = np.zeros(num_transitions)
        for c1 in range(l):
            tot = np.sum(counts[list(range(c1*l, (c1+1)*l ))]) # total counts leaving this state
            totals[c1] = tot
            if tot > 0:
                for c2 in range(l):
                    index = c1*l + c2
                    # mean and std. dev of the corresponding beta distribution
                    p = (counts[index]+1)/(tot+l)
                    mu[index] = p
                    sigma[index] = np.sqrt(p*(1-p)/(tot+ (l+1)))

        self.params = mu
        self.std = sigma
        self.state_totals = totals


    def get_parameters(self):
        if self.params is None:
            self.compute_prob_params(self.counts)
        return self.params

    def get_std_dev(self):
        if self.std is None:
            self.compute_prob_params(self.counts)
        return self.std

    def get_state_totals(self):
        if self.state_totals is None:
            self.compute_prob_params(self.counts)
        return self.state_totals



def _is_power_of_2(x):
    return (x & (x-1) == 0 and x != 0)


class MultiplexMarkovChain(MarkovChain):
    """
    Class inherits from MarkovChain. In addition, the class builds a
    null model for detecting `dynamical spillover` (Insert ref. to
    paper).

    Parameters
    ----------

    null_components : a list with a dictionary for each layer of the
    multiplex network. The dictionary has two items:

        counts : the total counts associated with a Markov chain
        describing the edge dynamics on a particular layer

        MC : the MarkovChain initialized with the above counts.


    null_prob : transition parameters for the null model.

    null_std : standard deviation associated with the transition
    parameters of the null model.

    See Also
    ---------
    MarkovChain

    """


    def __init__(self, counts):
        num_transitions = len(counts)
        #check if the num_transitions is a power of 2.
        if not _is_power_of_2(num_transitions):
            raise AssertionError("Length of counts is not a power of 2.")

        MarkovChain.__init__(self, counts)
        self.null_components = None
        self.null_prob = None
        self.null_std = None


    def _compute_null_counts(self, counts):
        """
        This function computes the counts for the null model. Currently
        hard coded for 4 states.
        """
        counts_layer1 = np.zeros(4)
        counts_layer2 = np.zeros(4)
        counts_layer1[0] = counts[0] + counts[2] + counts[8] + counts[10]
        counts_layer1[1] = counts[1] + counts[3] + counts[9] + counts[11]
        counts_layer1[2] = counts[4] + counts[6] + counts[12] + counts[14]
        counts_layer1[3] = counts[5] + counts[7] + counts[13] + counts[15]
        counts_layer2[0] = counts[0] + counts[1] + counts[4] + counts[5]
        counts_layer2[1] = counts[2] + counts[3] + counts[6] + counts[7]
        counts_layer2[2] = counts[8] + counts[9] + counts[12] + counts[13]
        counts_layer2[3] = counts[10] + counts[11] + counts[14] + counts[15]
        self.null_components = [{"counts":counts_layer1}, {"counts":counts_layer2}]

    def compute_prob_null_components(self):
        """
        Initializes a MarkovChain for each layer of the multiplex that
        describes the evolution of edges on that layer independent of
        the other layers.
        """
        for component in self.null_components:
            component["MC"] = MarkovChain(component["counts"])


    def compute_null_components(self):
        """
        Computes the components of the null model. For a 4-state MC,
        they are two 2-state MCs.
        """
        self._compute_null_counts(self.counts)
        self.compute_prob_null_components()

    def get_index_for_null(self, i):
        if (i == 0):
            return [0, 0]
        elif (i == 1):
            return [1, 0]
        elif (i == 2):
            return [0, 1]
        elif (i == 3):
            return [1, 1]
        elif (i == 4):
            return [2, 0]
        elif (i == 5):
            return [3, 0]
        elif (i == 6):
            return [2, 1]
        elif (i == 7):
            return [3, 1]
        elif (i == 8):
            return [0, 2]
        elif (i == 9):
            return [1, 2]
        elif (i == 10):
            return [0, 3]
        elif (i == 11):
            return [1, 3]
        elif (i == 12):
            return [2, 2]
        elif (i == 13):
            return [3, 2]
        elif (i == 14):
            return [2, 3]
        else:
            return [3, 3]


    def compute_null_prob_std(self):
        """
        Computes the null probability using the null components. When
        computing the standard deviation the method approximates the
        beta distributions as a Gaussian distributions.
        """
        num_transitions = self.num_transitions
        pnull = np.ones(num_transitions)
        std_null = np.zeros(num_transitions)
        #If the Gaussian approximation is not justified warn the user
        state_totals = self.get_state_totals()
        if (np.any(state_totals < 100)):
            warn("Some of the state totals are less than 100. Gaussian approximation may not be justified.")
        for i in range(num_transitions):
            indices = self.get_index_for_null(i)
            for j,q in enumerate(indices):
                null_component = self.null_components[j]
                prob = null_component["MC"].get_parameters()[q]
                sigma = null_component["MC"].get_std_dev()[q]
                pnull[i] *= prob
                std_null[i] +=  (sigma/prob)**2
        std_null = np.sqrt(std_null)
        std_null = pnull*std_null
        self.null_prob = pnull
        self.null_std = std_null


    def get_null_prob(self):
        """
        Return the probability for each transition
        of the null model. Computes the null model the first time this
        function is called.
        """
        if self.null_prob is None:
            if self.null_components is None:
                self.compute_null_components()

            self.compute_null_prob_std()
        return self.null_prob


    def get_null_std_dev(self):
        """
        Returns the std dev. associated with the probability
        distribution of the transition parameters of the null model.
        """
        if self.null_std is None:
            if self.null_components is None:
                self.compute_null_components()
            self.compute_null_prob_std()
        return self.null_std
