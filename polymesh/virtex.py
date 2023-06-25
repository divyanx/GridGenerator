import numpy as np


class Vertices:
    def __init__(self):
        self.vertex_dict = dict()
        self._next_vertex_id = 0
        self.vertex_half_edge_dict = dict()
        self.vertex_face_dict = dict()
        self.vertex_edge_dict = dict()

    def get_new_vertex_id(self):
        new_vertex_id = self._next_vertex_id
        self._next_vertex_id += 1
        return new_vertex_id

    def add_vertex(self, coords: np.array):
        # check if vertex already exists and return the vertex id
        for vertex_id, vertex in self.vertex_dict.items():
            if np.array_equal(vertex.coords, coords):
                return vertex_id

        # create a new vertex and return the vertex id
        new_vertex_id = self.get_new_vertex_id()
        self.vertex_dict[new_vertex_id] = coords
        return new_vertex_id

    def get_vertex_coords(self, vertex_id):
        return self.vertex_dict[vertex_id]







