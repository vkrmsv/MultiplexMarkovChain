.. image:: https://travis-ci.org/vkrmsv/MultiplexMarkovChain.svg?branch=master
    :target: https://travis-ci.org/vkrmsv/MultiplexMarkovChain
.. image:: https://landscape.io/github/vkrmsv/MultiplexMarkovChain/master/landscape.svg?style=flat
   :target: https://landscape.io/github/vkrmsv/MultiplexMarkovChain/master
   :alt: Code Health

``MultiplexMarkovChain`` is a Python package that helps discern
"dynamical spillover" in multiplex networks.

The package helps discover correlations present in the edge
dynamics of multiplex networks. Please see the following paper for
information on "dynamical spillover".
http://arxiv.org/abs/1505.04766



Requirements
------------

- Numpy

- Networkx

- IPython notebook (for the example)



Main Files
-----------

- extract_counts.py : This file contains functions that can extract
  counts that can be used to construct a Markov chain from
  longitudinal data on Multiplex networks.

- MultiplexMarkovChain.py : This file contains the class
  MultiplexMarkovChain. This class helps in building a Markov chain
  that represents edge dynamics of a multiplex network. The class also
  has methods to construct the corresponding null model that can
  determine the existence of dynamical spillover.

- example.ipynb : An example (in IPython notebook format) that steps
  through how this package can be used to detect dynamical spillover
  in a real world multiplex network. You can see the example by typing
  `ipython notebook` in the command line from the folder in which you
  cloned the ``MultiplexMarkovChain`` repository, then clicking
  `example.ipynb` in the browser window that opens.

- alliance_trade_nodes.csv : Contains the data on the presence of
  nodes (i.e. nation-states) in each year from 1950 to 2003. The
  format is: year,nation. 

- alliance_trade_edges.csv : Contains the data on the presence of
  alliance and trade edges between a pair of nodes
  (i.e. nation-states) in each year from 1950 to 2003. The format is:
  year,nation1,nation2,alliance,trade. `alliance`, `trade` are binary
  entries with 0 indicating absence and 1 indicating presence of that
  particular type of link between `nation1` and `nation2`.



Unittest files
----------------

- test_MultiplexMarkovChain.py : unittests for the classes in the
  file MultiplexMarkovChain.py.

- test_extract_counts.py : unittests for functions in the file
  extract_counts.py.

- test_input_edges.csv : Edge list of an example network used as input
  in unittests.

- test_input_nodes.csv : Node list of an example network used as input
  in unittests.



Data Sources
--------------

The files `alliance_trade_nodes.csv` and `alliance_trade_edges.csv`
together describe the multiplex network of alliance and trade between
countries. The data on international alliances is derived from the
ATOP project [B. A. Leeds, Rice University, Department of Political
Science, Houston (2005)]. The trade networks are derived from a
combination of two datasets on international trade: the Correlates of
War (COW) bilateral trade dataset [K. Barbieri, O. M. Keshk,
and B. M. Pollins, Conflict Management and Peace Science 26, 471
(2009)], and the Gledistch trade dataset [K. S. Gleditsch, Journal of
Conflict Resolution 46, 712 (2002)]. The trade data is binarized such
that an edge exists if the value of trade between two countries is
greater than 0.001 of the exporter’s GDP. Note the above threshold is
not symmetric between the two countries involved in trade, and hence
gives us a directed network of trade between nations. Neglecting the
edge directionality, i.e., ensuring there is at least one-way trade
yields the data provided here.




Acknowledgments
-----------------
``MultiplexMarkovChain`` thanks Ryan James and Pierre-Andre Noel for helpful
pointers. 


``MultiplexMarkovChain`` gratefully acknowledges support from the following:

- US Army Research Laboratory and the US Army Research Office under MURI award W911NF-13-1-0340, and Cooperative Agreement W911NF-09-2-0053 

- The Defense Threat Reduction Agency Basic Research Grant No. HDTRA1-10-1-0088 

- NSF Grant No. ICES-1216048
