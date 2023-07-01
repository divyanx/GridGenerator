#
# class Edges:
#     """
#     An edge is a line segment between two vertices.
#     Edge is denoted by two half-edges, one for each direction.
#     """
#
#     def __init__(self):
#         self.edges_half_edges_dict = {}
#         self._next_edge_id = 0
#
#     def get_next_avail_id(self):
#         new_edge_id = self._next_edge_id
#         self._next_edge_id += 1
#         return new_edge_id
#
#     def add_new_edge(self, half_edge_id_1, half_edge_id_2):
#         new_edge_id = self.get_next_avail_id()
#         self.edges_half_edges_dict[new_edge_id] = [half_edge_id_1, half_edge_id_2]
#         return new_edge_id
#
#     def get_edge_half_edge_ids(self, edge_id):
#         return self.edges_half_edges_dict[edge_id]
#
#
#
#
#
#
#
#
#
#
#
