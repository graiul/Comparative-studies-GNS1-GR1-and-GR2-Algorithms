class EdgeFinderTool(object):
    input_edge = None
    list_of_edges = []
    def __init__(self, input_edge, list_of_edges):
        self.input_edge = input_edge
        self.list_of_edges = list_of_edges

    def edge_found(self):
        for edge in self.list_of_edges:
            found = False
            if self.input_edge[0] in edge and self.input_edge[1] in edge:
                return True
            else:
                return False
