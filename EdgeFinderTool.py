class EdgeFinderTool(object):
    input_edge = None
    list_of_edges = []
    def __init__(self, input_edge, list_of_edges):
    # def __init__(self, input_edge, list_of_edges, data_graph):
        self.input_edge = input_edge
        self.list_of_edges = list_of_edges
        # self.data_graph = data_graph

    def edge_found(self):
        if len(self.list_of_edges) == 0:
            return False
        if len(self.list_of_edges) > 0:
            found = False
            for edge in self.list_of_edges:
                node1 = self.input_edge[0]
                node2 = self.input_edge[1]
                if self.input_edge[0] in edge and self.input_edge[1] in edge:
                    # if self.data_graph.nodes[self.input_edge[0]]['label'] == self.data_graph.nodes[edge[0]]['label'] and self.data_graph.nodes[self.input_edge[1]]['label'] == self.data_graph.nodes[edge[1]]['label']:

                    return True
                else:
                    found = False
            return found
