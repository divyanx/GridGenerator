from .virtex import Virtex


class HalfEdge:
    def __init__(self, start_vertex: Virtex, end_vertex: Virtex):
        self.start_vertex: Virtex = start_vertex
        self.end_vertex = end_vertex
        self.next = None
        self.prev = None
        self.opposite = None
        self.face = None
        self.edge = None
        self.is_boundary = False

    def __eq__(self, other):
        return self.start_vertex == other.start_vertex and self.end_vertex == other.end_vertex

    def __hash__(self):
        return hash((self.start_vertex, self.end_vertex))

    def __str__(self):
        return f"HalfEdge({self.start_vertex}, {self.end_vertex})"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self
