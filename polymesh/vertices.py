import numpy as np


class Vertices:
    def __init__(self):
        self.vertex_dict = dict()
        self.coords_to_vertex_id_dict = dict()
        self._next_vertex_id = 0
        self.vertex_starting_half_edges_dict = dict()
        self.vertex_ending_half_edges_dict = dict()
        self.vertex_face_dict = dict()
        self.vertex_edge_dict = dict()

    def get_next_avail_id(self):
        new_vertex_id = self._next_vertex_id
        self._next_vertex_id += 1
        return new_vertex_id

    def add_vertex(self, coords: np.array):
        # check if vertex already exists and return the vertex id
        for vertex_id, vertex in self.vertex_dict.items():
            if np.array_equal(vertex, coords):
                "vertex already exists"
                return vertex_id

        # create a new vertex and return the vertex id
        new_vertex_id = self.get_next_avail_id()
        self.vertex_dict[new_vertex_id] = coords
        self.coords_to_vertex_id_dict[coords] = new_vertex_id
        return new_vertex_id

    def get_vertex_coords(self, vertex_id):
        return self.vertex_dict[vertex_id]

    def get_vertex_id(self, coords):
        return self.coords_to_vertex_id_dict[coords]

    def add_starting_half_edge(self, vertex_id, half_edge_id):
        # append half edge id to the list of starting half edges
        if vertex_id in self.vertex_starting_half_edges_dict.keys():
            if half_edge_id not in self.vertex_starting_half_edges_dict[vertex_id]:
                self.vertex_starting_half_edges_dict[vertex_id].append(half_edge_id)
        else:
            self.vertex_starting_half_edges_dict[vertex_id] = [half_edge_id]

    def add_ending_half_edge(self, vertex_id, half_edge_id):
        # append half edge id to the list of ending half edges
        if vertex_id in self.vertex_ending_half_edges_dict.keys():
            if half_edge_id not in self.vertex_ending_half_edges_dict[vertex_id]:
                self.vertex_ending_half_edges_dict[vertex_id].append(half_edge_id)
        else:
            self.vertex_ending_half_edges_dict[vertex_id] = [half_edge_id]

    def get_starting_half_edges(self, vertex_id):
        return self.vertex_starting_half_edges_dict[vertex_id]

    def get_ending_half_edges(self, vertex_id):
        return self.vertex_ending_half_edges_dict[vertex_id]









