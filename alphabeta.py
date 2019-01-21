import re

traces_enabled = False
leaf_nodes_examined = 0

def read_file():
    """Read in data input from the 'alphabeta.txt' file and call write_file for data output."""
    minimax = []
    edges = []
    line = 0
    with open('alphabeta.txt') as f:
        for line in f:
            if not line.strip():
                continue
            line = line.strip().split(' ')
            minimax_list = re.findall('[a-zA-Z]+', line[0])
            edges_list = re.findall('\w+', line[1])
            for i in range(len(minimax_list)//2):
                minimax_list[i] = (minimax_list[i], minimax_list[i+1])
                del minimax_list[i+1]
            for i in range(len(edges_list)//2):
                edges_list[i] = (edges_list[i], edges_list[i+1])
                del edges_list[i+1]

            minimax.append(minimax_list)
            edges.append(edges_list)

    if traces_enabled:
        print("minimax =", minimax)
        print("edges =", edges)

    write_file(minimax, edges)

def write_file(minimax, edges):
    """Write to output file ('alphabeta_out.txt') after calling minimax (alpha_beta) with the input graph(s)."""
    global leaf_nodes_examined
    f = open('alphabeta_out.txt', 'w')

    for edge in range(len(edges)):
        leaf_nodes_examined = 0
        current_node = edges[edge][edge]
        if traces_enabled:
            print("==========Graph {}==========".format(edge+1))
            print("current_node[0] =", current_node, "\nminimax[edge] =", minimax[edge], "\nedges[edge] =", edges[edge])
        score = alpha_beta(current_node[0], minimax[edge], edges[edge], -float('inf'), float('inf'))
        if traces_enabled:
            print("score =", score)
        f.write('Graph {}: Score: {}; Leaf Nodes Examined: {}\n\n'.format(edge+1, score, leaf_nodes_examined))


def alpha_beta(current_node, minimax, edges, alpha, beta):
    """Minimax algorithm using alpha-beta pruning."""
    
    def is_leaf(node):
        """Return True if the input node is a leaf node; False otherwise."""
        try:
            int(node)
            return True
        except ValueError:
            return False

    def is_max_node(node):
        """Return True if an input node is a max node; False otherwise."""
        def getMaxNodes():
            max_nodes = []
            for i in range(len(minimax)):
                if minimax[i][1] == 'MAX':
                    max_nodes.append(minimax[i][0])

            return max_nodes

        max_nodes = getMaxNodes()
        if node[0] in max_nodes:
            return True

        return False

    def getChildren():
        """Return the child nodes of the current node as a list"""
        children = []
        for i in range(len(edges)):
            if edges[i][0] == current_node:
                children.append(edges[i][1])
        return children

    if traces_enabled:
        print("current_node =", current_node)

    if is_leaf(current_node):
        global leaf_nodes_examined
        leaf_nodes_examined += 1
        if traces_enabled:
            print("is_leaf", int(current_node))
        return int(current_node)

    if is_max_node(current_node):
        maximum = -float("inf")
        children = getChildren()
        if traces_enabled:
            print("in method is_max_node")
            print("children =", children)
        for child in children:
            if traces_enabled:
                print("child", child, "alpha", alpha, "beta", beta)
            maximum = max(alpha, alpha_beta(child, minimax, edges, alpha, beta))
            alpha = max(alpha, maximum)
            if alpha >= beta:
                if traces_enabled:
                    print("beta", beta, "<=", "alpha", alpha)
                break
        return maximum

    else:
        minimum = float("inf")
        children = getChildren()
        if traces_enabled:
            print("in is_min_node")
            print("children =", children)
        for child in children:
            if traces_enabled:
                print("child", child, "alpha", alpha, "beta", beta)
            minimum = min(beta, alpha_beta(child, minimax, edges, alpha, beta))
            beta = min(beta, minimum)
            if beta <= alpha:
                if traces_enabled:
                    print("beta", beta, "<=", "alpha", alpha)
                break
        return minimum


def main():
    read_file()
    if traces_enabled:
        print("leaf_nodes_examined =", leaf_nodes_examined)


if __name__=='__main__':
    main()
