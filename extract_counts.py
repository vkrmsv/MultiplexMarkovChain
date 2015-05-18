#!/usr/bin/env python
"""
File contains functions to compute counts for constructing Markov
chains for the dynamics of edges on a two-layer multiplex network.
"""


import numpy as np
import networkx as nx
import logging

#set up logs
logger = logging.getLogger("multiplex_markov_chain")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)



def get_node_set(g1,g2,method="union"):
    """
    Returns the set of nodes that have to be considered in counting
    transitions of the Markov chains.  The input for the keyword
    argument `method` controls the method used.
    """
    if (method=="intersection"):
        nodes = list(set(g1.nodes()) & set(g2.nodes()))
    else:
        nodes = list(set(g1.nodes()) | set(g2.nodes()))
    return nodes
    

def get_counts(g1, g2, method):
    """
    Computes the counts for each transition from time (t) step to time
    (t+1) given networkx graph instances for the two time steps.

    Parameters
    -----------
    g1 : nx graph object representing the multiplex at time t
    g2 : nx graph object representing the multiplex at time (t+1)

    Each edge of the graph must have an attribute `state` that is set
    when the graph is constructed.  The output is an array of size 16
    that has the counts for (t) to (t+1).

    method : When the set of nodes in g1 is not the same as g2, the
    `method` to be used to find a common set of nodes. Accepts two
    values union or intersect.
    
    Returns
    -------
    counts : np.array of counts for the transitions
    
    """
    # get the set of nodes to iterate over
    nodes = get_node_set(g1, g2, method)
    # Now count the numbers for each transition
    counts = np.zeros(16, int)
    for i,n in enumerate(nodes):
        for m in nodes[i+1:]:
            if (g1.has_edge(n,m)):
                #An edge is present, check what is the state
                prev_state = g1.edge[n][m]["state"]
            else:
                prev_state = 0
            if (g2.has_edge(n,m)):
                current_state = g2.edge[n][m]["state"]
            else:
                current_state = 0
            transition = prev_state*4 + current_state
            counts[transition] += 1
    return counts


def compute_counts_from_file(fname_edges, fname_nodes=None, method=None):
    """
    Get as inputs file path for edges of the graph. Returns a
    dictionary with counts indexed by the time steps

    Parameters
    -----------
    fname_edges : path to a csv file of edge information in the
    following format.
    Time,Node1,Node2,Edge-Type1,Edge-Type2

    Time: Integer indicating the time the pair of nodes
    
    Edge-Type1 : Binary value. 0 (1) indicates absence (presence) of
    an edge of type 1

    Edge-Type2 : Binary value. 0 (1) indicates absence (presence) of
    an edge of type 2

    The file could be an edge-list, i.e., a list of only the edges
    present in the network or a list of all possible node-pairs with
    information of edges that are absent.

    fname_nodes : optional, path to a csv file with node information
    with the following format.  Time,Node

    Assumptions:
    - The values for Time above is non-decreasing.
    - When there is a change, time increases by 1.

    method : method to use when the set of nodes between two time
    steps are not the same. The variable accepts the strings `union`
    or `intersection`.

    Returns
    --------
    counts : dictionary with time steps as key and the np.array of
    counts for the transitions as the value.
    
    """
    fEdges = open(fname_edges,"r")
    fEdges.readline()
    counts = {}
    prevTimeStep = None
    timeStepToProcess = None

    # When method is not specified, if node file is given use the
    # intersection between two time steps, else use the union.
    if method is None:
        if fname_nodes is None:
            method = "union"
        else:
            method = "intersection"
    

    if (fname_nodes is not None):
        fNodes = open(fname_nodes,"r")
        fNodes.readline()
        nodeLine = fNodes.readline()
        nodeLine = nodeLine.rstrip()
        if (nodeLine):
            timeStep_nodes, node = nodeLine.split(",")
        else:
            nodeLine = None    
    for line in fEdges:
        line = line.rstrip()
        edge = line.split(",")
        if (len(edge) != 5):
            logger.warning("Line not in proper format. Ignoring %s",line)
            continue
        timeStep, n1, n2, eA, eB = edge
        if (timeStep != prevTimeStep):
            if prevTimeStep is not None:
                if (timeStepToProcess is None):
                    timeStepToProcess = prevTimeStep
                else:
                    # There are two graphs that are built. Get counts for them.
                    logger.info("Getting counts for %s-->%s",g_old.graph['time'],g_new.graph['time'])
                    c = get_counts(g_old, g_new, method = method)
                    counts[timeStepToProcess] = c
                    timeStepToProcess = prevTimeStep
                #New time step has started. Assign old graphs to the new ones.
                g_old = g_new
                # Start building a new graph for the current time.
            g_new = nx.Graph(time=timeStep)
            #add nodes for this timeStep
            if fname_nodes is not None:
                while (nodeLine and timeStep_nodes == timeStep):
                    g_new.add_node(node)
                    nodeLine = fNodes.readline()
                    nodeLine = nodeLine.rstrip()
                    if (nodeLine):
                        timeStep_nodes, node = nodeLine.split(",")
                    else:
                        nodeLine = None

        #another edge in the graph, process and store the state
        # assuming inputs are "nice"
        g_new.add_nodes_from([n1,n2])
        try:
            edgeState = 2*int(eB) + int(eA)
        except:
            logger.error("Edge '%s' cannot produce an integer valued state. Please check the input.", line)
        if (g_new.has_edge(n1,n2) and g_new.edge[n1][n2]["state"] != edgeState):
            logger.warning("Graph already has edge %s--%s in state %s",n1,n2,g_new.edge[n1][n2]["state"])
        g_new.add_edge(n1,n2, state=edgeState)
        prevTimeStep = timeStep

    logger.info("Reached end of edge list")
    logger.info("Getting counts for %s-->%s",g_old.graph['time'],g_new.graph['time'])
    c = get_counts(g_old, g_new, method)
    counts[timeStepToProcess] = c
    fEdges.close()
    return counts


