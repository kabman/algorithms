import numpy as np

BIG_INT = int(2**31 - 1)


def read_weighted_edge_list(filename):
    edges = []
    with open(filename, 'r') as f:
        l = f.readline()
        n, m = map(int, l.split())
        for i, l in enumerate(f):
            u, v, c = map(int, l.split())
            edges.append((u, v, c))
    return n, m, edges


def floydwarshall(n, edges):
    '''
    Returns the minimum shortest path in a directed graph with n nodes and edge
    list edges. Uses the Floyd Warshall algorithm.
    '''
    # A is an n+1 x n+1 x n+1 array. The first dimension is indexed by k. Each
    # n+1 x n+1 array at each k is the minimum shortest path from node i to
    # node j using k or fewer edges. The values for i = 0 or j = 0 are
    # undefined for all k. The redundant 0th row/column simplifies dealing with
    # the conventional input for this problem, in which nodes are numbered 1 to
    # n. Effectivtly it turns Python into a 1-indexing language.
    #
    # int(2**31 - 1) is an arbitrary large integer (the largest possible in 32
    # bit precision), and denotes the absence of a path between two nodes
    # (which is true for all pairs of nodes not connected by 1 edge, at the
    # beginning of the code).
    A = np.zeros((n+1, n+1), dtype=np.int) + BIG_INT
    # Read in the edges.
    for u, v, c in edges:
        A[u, v] = c
    # Nodes are connected to themselves.
    for i in range(1, n+1):
        A[i, i] = 0

    # The Floyd Warshall algorithm considers subproblems of size k and solves
    # for the shortest path i, j with all internal nodes in the range 1...k
    # inclusive, i.e. k is the the maximum node id that can be used to
    # construct a candidate path between i and j. The shortest path from i to j
    # using nodes up to k is then the shorter of:
    #  1. The shortest path from i to j using nodes up to k - 1,
    #  2. The paths from i to k using nodes up to k - 1 + the path from k to j,
    #     using nodes up to k - 1
    # The two subproblems in case 2 are themselves optimal solutions, so this
    # is a recursive algorithm
    for k in range(1, n+1):
        # Broadcasting outer operation trick:
        #   X[i, k] + Y[k, j] = Z[i, j] if
        #   Z = X[:, k]_T + Y[k, :]
        # Where the calculation of the matrix Z uses broadcasting rather than a
        # double for loop. To take the transpose of a 1-D vector x in numpy,
        # x[:, np.newaxis]. The (n+1, n+1) array B is then case 2 above
        B = A[:, k, np.newaxis] + A[k, :]
        A = np.minimum(A, B)

    # Floyd Warshall has at least one negative number on the leading diagonal
    # if a negative weight closed cycle was found (in which case the minimum
    # shortest path is not defined).
    if np.any(np.diag(A) < 0):
        return BIG_INT
    else:
        return np.min(A)


def test_floydwarshall():
    n, m, edges = read_weighted_edge_list('apsp_tests/tc1.txt')
    assert floydwarshall(n, edges) == -10003
    n, m, edges = read_weighted_edge_list('apsp_tests/tc2.txt')
    assert floydwarshall(n, edges) == -6
    n, m, edges = read_weighted_edge_list('apsp_tests/tc3.txt')
    assert floydwarshall(n, edges) == BIG_INT


def solve_assignment4():
    n, m, edges = read_weighted_edge_list('apsp_tests/g1.txt')
    g1_solution = floydwarshall(n, edges)
    print g1_solution
    n, m, edges = read_weighted_edge_list('apsp_tests/g2.txt')
    g2_solution = floydwarshall(n, edges)
    print g2_solution
    n, m, edges = read_weighted_edge_list('apsp_tests/g3.txt')
    g3_solution = floydwarshall(n, edges)
    print g3_solution

    solution = min(g1_solution, g2_solution, g3_solution)
    assert solution == -19
    print solution
