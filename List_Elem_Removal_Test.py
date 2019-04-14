query_graph_edges = [('a1', 'b1'), ('a1', 'c1'), ('b1', 'd1'), ('b1', 'e1'), ('c1', 'd1'), ('c1', 'f1'), ('d1', 'f1'), ('d1', 'e1')]
e = tuple(['b1', 'd1'])
query_graph_edges.remove(e)
print(query_graph_edges)
