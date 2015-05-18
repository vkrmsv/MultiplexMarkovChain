"""
Test cases for testing the class MultiplexMarkovChain and the class
MarkovChain.

"""

import MultiplexMarkovChain

import unittest
import time
import numpy as np

class TestMarkovChain(unittest.TestCase):
    
    def get_counts(self):
        counts = [10, 10, 20, 20]
        return counts

    def setUp(self):
        counts = self.get_counts()
        self.MC = MultiplexMarkovChain.MarkovChain(counts)


    def test_markov_chain_state_totals(self):
        totals_expected = [20, 40]
        totals_obtained = self.MC.get_state_totals()
        self.assertTrue(np.allclose(totals_expected, totals_obtained))


    def test_markov_chain_parameters(self):
        parameters_expected = np.array([0.5, 0.5, 0.5, 0.5])
        parameters = self.MC.get_parameters()
        self.assertTrue(np.allclose(parameters_expected, parameters))


    def test_markov_chain_std_dev(self):
        sigma_expected = np.array([0.104257207028537, 0.104257207028537,  0.076249285166302,  0.076249285166302])
        sigma_obtained = self.MC.get_std_dev()
        self.assertTrue(np.allclose(sigma_expected, sigma_obtained))


class TestMultiplexMarkovChain(unittest.TestCase):

    def get_counts_for_exception(self):
        counts = [10, 6, 3]
        return counts

    def get_counts(self):
        # numbers from the network of nations data.
        counts = [319388, 485, 19285, 50, 108, 11964, 3, 1552, 17205, 53, 165360, 707, 10, 1311, 196, 25513]
        return counts

    def setUp(self):
        counts = self.get_counts()
        self.MC = MultiplexMarkovChain.MultiplexMarkovChain(counts)

    def test_exception_raised_with_bad_input_for_count(self):
        counts = self.get_counts_for_exception()
        with self.assertRaises(AssertionError):
            MultiplexMarkovChain.MultiplexMarkovChain(counts)

    def test_counts_null_components(self):
        self.MC.compute_null_components()
        null_components = self.MC.null_components
        #assert that the null_components as elements corresponding to two layers
        self.assertTrue(len(null_components),2)
        # check if the outputs match
        expected_output = [[521238, 1295, 317, 40340], [331945, 20890, 18579, 191776]]
        for i,layer in enumerate(null_components):
            self.assertTrue(np.allclose(layer["counts"],expected_output[i]))

    def test_prob_null_components(self):
        self.MC.compute_null_components()
        null_components = self.MC.null_components
        prob_expected = [[0.99751978336379377, 0.0024802166362061871, 0.007821146609606729, 0.99217885339039324],
                          [0.94079135691551619, 0.059208643084483772, 0.088326036214625619, 0.91167396378537435]]
                         
        for i,layer in enumerate(null_components):
            self.assertTrue(np.allclose(layer["MC"].get_parameters(),prob_expected[i]))


    def test_prob_null(self):
        pnull_expected = [0.93845799054089529, 0.002333366374620856, 0.059061792822898439, 0.00014685026158533105, 0.0073580671314871036, 0.93343328978402906, 0.00046307947811962514, 0.058745563606364147, 0.088106968510195949, 0.00021906770442966462, 0.90941281485359782, 0.0022611489317765224, 0.00069081087868002027, 0.087635225335945602, 0.0071303357309267087, 0.90454362805444766]
        pnull_obtained = self.MC.get_null_prob()
        self.assertTrue(np.allclose(pnull_obtained, pnull_expected))
        


if __name__ == '__main__':
    unittest.main()


