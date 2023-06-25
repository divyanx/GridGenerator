class Faces:
    def __init__(self, half_edge=None):
        self.half_edge = half_edge
        self.vertices = []
        self.edges = []
        self.half_edges = []

    def __str__(self):
        return f"Face({self.vertices})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(tuple(self.vertices))

    def __eq__(self, other):
        if self.half_edge is None or other.half_edge is None:
            return False
        self.set_half_edges_from_half_edge()
        other.set_half_edges_from_half_edge()

        if len(self.half_edges) != len(other.half_edges):
            return False

        for he in self.half_edges:
            if he not in other.half_edges:
                return False

        return True

    def set_vertices_from_half_edge(self):
        """
        Set vertices from half_edge
        :return: None
        """
        self.vertices = []
        he = self.half_edge
        while True:
            self.vertices.append(he.start_vertex)
            he = he.next
            if he == self.half_edge:
                break

    def set_edges_from_half_edge(self):
        """
        Set edges from half_edge
        :return: None
        """
        self.edges = []
        he = self.half_edge
        while True:
            self.edges.append(he.edge)
            he = he.next
            if he == self.half_edge:
                break

    def set_half_edges_from_half_edge(self):
        """
        Set half_edges from half_edge
        :return: None
        """
        self.half_edges = []
        he = self.half_edge
        while True:
            self.half_edges.append(he)
            he = he.next
            if he == self.half_edge:
                break





