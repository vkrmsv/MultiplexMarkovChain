"""
Test cases for testing if extract counts works as intended.

"""

from extract_counts import *



import unittest
import numpy as np

class TestExtractCounts(unittest.TestCase):

    def test_counts_with_out_nodes(self):
        """
        When there are no isolated nodes, there is no difference
        between the union and intersect method.
        """
        counts_obtained = compute_counts_from_file("test_input_edges.csv")
        counts_expected = {}
        counts_expected["0"] = np.array([0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1],int)
        counts_expected["1"] = np.array([0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0],int)
        for key in counts_expected:
            np.testing.assert_array_equal(counts_expected[key], counts_obtained[key])

        
    def test_counts_with_nodes_intersect(self):
        counts_obtained = compute_counts_from_file("test_input_edges.csv", "test_input_nodes.csv")
        counts_expected = {}
        counts_expected["0"] = np.array([0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1],int)
        counts_expected["1"] = np.array([3,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0],int)
        for key in counts_expected:
            np.testing.assert_array_equal(counts_expected[key], counts_obtained[key])


    def test_counts_with_nodes_union(self):
        counts_obtained = compute_counts_from_file("test_input_edges.csv", "test_input_nodes.csv", method="union")
        counts_expected = {}
        counts_expected["0"] = np.array([3,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1],int)
        counts_expected["1"] = np.array([3,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0],int)
        for key in counts_expected:
            np.testing.assert_array_equal(counts_expected[key], counts_obtained[key])


if __name__ == '__main__':
    unittest.main()
