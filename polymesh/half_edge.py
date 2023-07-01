
class HalfEdges:
    def __init__(self):
        self.half_edge_vertex_dict = dict()
        self.vertex_to_half_edge_dict = dict()  # ((start_x, start_y), (end_x, end_y)) -> half_edge_id
        self._next_half_edge_id = 0
        self.half_edge_next_half_edge_dict = dict()
        self.half_edge_prev_half_edge_dict = dict()
        self.half_edge_face_dict = dict()
        self.half_edge_boundary_dict = dict()
        self.half_edge_coords_dict = dict()
        self.half_edge_twin_half_edge_dict = dict()
        self.half_edge_name_dict = dict()

    def get_next_avail_id(self):
        new_half_edge_id = self._next_half_edge_id
        self._next_half_edge_id += 1
        return new_half_edge_id

    def add_new_half_edge(self, start_vertex_id, end_vertex_id):
        # check if half edge already exists with same start and end vertex
        if (start_vertex_id, end_vertex_id) in self.vertex_to_half_edge_dict:
            print("half edge already exists")
            return self.vertex_to_half_edge_dict[(start_vertex_id, end_vertex_id)]

        # create a new half edge
        new_half_edge_id = self.get_next_avail_id()
        self.half_edge_vertex_dict[new_half_edge_id] = (start_vertex_id, end_vertex_id)
        self.vertex_to_half_edge_dict[(start_vertex_id, end_vertex_id)] = new_half_edge_id
        self.half_edge_next_half_edge_dict[new_half_edge_id] = None
        self.half_edge_prev_half_edge_dict[new_half_edge_id] = None
        # self.half_edge_face_dict[new_half_edge_id] = None
        self.half_edge_boundary_dict[new_half_edge_id] = False
        return new_half_edge_id

    def get_next_half_edge(self, half_edge_id):
        return self.half_edge_next_half_edge_dict[half_edge_id]

    def get_prev_half_edge(self, half_edge_id):
        return self.half_edge_prev_half_edge_dict[half_edge_id]

    def get_half_edge_vertices(self, half_edge_id):
        return self.half_edge_vertex_dict[half_edge_id]

    def get_half_edge_start_vertex(self, half_edge_id):
        return self.half_edge_coords_dict[half_edge_id][0]

    def get_half_edge_end_vertex(self, half_edge_id):
        return self.half_edge_coords_dict[half_edge_id][1]

    def iterate_half_edge_loop(self, start_half_edge_id):
        current_half_edge_id = start_half_edge_id
        while True:
            yield current_half_edge_id
            current_half_edge_id = self.get_next_half_edge(current_half_edge_id)
            if current_half_edge_id == start_half_edge_id:
                break

    def set_next_half_edge_id(self, half_edge_id, next_half_edge_id):
        self.half_edge_next_half_edge_dict[half_edge_id] = next_half_edge_id

    def set_prev_half_edge_id(self, half_edge_id, prev_half_edge_id):
        self.half_edge_prev_half_edge_dict[half_edge_id] = prev_half_edge_id

    def get_next_half_edge_id(self, half_edge_id):
        return self.half_edge_next_half_edge_dict[half_edge_id]

    def get_prev_half_edge_id(self, half_edge_id):
        return self.half_edge_prev_half_edge_dict[half_edge_id]

    def get_start_vertex_id(self, half_edge_id):
        return self.half_edge_vertex_dict[half_edge_id][0]

    def get_end_vertex_id(self, half_edge_id):
        return self.half_edge_vertex_dict[half_edge_id][1]

    def set_face_for_half_edge(self, half_edge_id, face_id):
        self.half_edge_face_dict[half_edge_id] = face_id

    def set_twin_for_half_edge(self, half_edge_id, twin_half_edge_id):
        self.half_edge_twin_half_edge_dict[half_edge_id] = twin_half_edge_id

    def get_twin_half_edge_id(self, half_edge_id):
        return self.half_edge_twin_half_edge_dict[half_edge_id]

    def get_face_for_half_edge(self, half_edge_id):
        return self.half_edge_face_dict[half_edge_id]

    def set_representative_half_edge_for_face(self, face_id, new_half_edge_id):
        self.half_edge_face_dict[face_id] = new_half_edge_id

    def set_twin_half_edge_id(self, new_half_edge_id, new_twin_half_edge_id_2):
        self.half_edge_twin_half_edge_dict[new_half_edge_id] = new_twin_half_edge_id_2
        self.half_edge_twin_half_edge_dict[new_twin_half_edge_id_2] = new_half_edge_id

    def get_half_edge_between_vertices(self, start_vertex_id, end_vertex_id):
        # check if half edge already exists with same start and end vertex
        if (start_vertex_id, end_vertex_id) not in self.vertex_to_half_edge_dict:
            return None
        return self.vertex_to_half_edge_dict[(start_vertex_id, end_vertex_id)]

    def get_face_id(self, half_edge_id):
        return self.half_edge_face_dict[half_edge_id]

