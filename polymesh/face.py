class Faces:
    def __init__(self):
        # faces are set if clockwise half edges
        self.face_half_edge_dict = dict()
        self.half_edge_face_dict = dict()
        self.face_holes_dict = dict()
        self.face_inside_holes_dict = dict()
        self.face_parent_face_dict = dict()
        self._next_face_id = 0

    def get_next_avail_id(self):
        print("current face id: ", self._next_face_id)
        new_face_id = self._next_face_id
        self._next_face_id += 1
        return new_face_id

    def add_new_face(self, half_edge_id):
        # check if face already exists and return the face id
        if half_edge_id in self.half_edge_face_dict.keys():
            return self.half_edge_face_dict[half_edge_id]

        new_face_id = self.get_next_avail_id()
        self.face_half_edge_dict[new_face_id] = half_edge_id
        self.half_edge_face_dict[half_edge_id] = new_face_id
        return new_face_id

    def get_face_half_edge_id(self, face_id):
        return self.face_half_edge_dict[face_id]

    def set_face_and_half_edge(self, face_id, half_edge_id):
        self.face_half_edge_dict[face_id] = half_edge_id
        self.half_edge_face_dict[half_edge_id] = face_id

    def remove_face(self, face_id):
        half_edge_id = self.face_half_edge_dict[face_id]
        del self.face_half_edge_dict[face_id]
        del self.half_edge_face_dict[half_edge_id]

