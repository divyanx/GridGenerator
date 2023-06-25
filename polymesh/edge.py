from .half_edge import HalfEdge
from .virtex import Virtex


class Edges:
    """
    An edge is a line segment between two vertices.
    Edge is denoted by two half-edges, one for each direction.
    """

    def __init__(self, half_edge1: HalfEdge, half_edge2: HalfEdge):
        self.half_edge1 = half_edge1
        self.half_edge2 = half_edge2
        self.vertices = [half_edge1.start_vertex, half_edge1.end_vertex]

    def __eq__(self, other):
        return self.half_edge1 == other.half_edge1 and self.half_edge2 == other.half_edge2

    def __hash__(self):
        return hash((self.half_edge1, self.half_edge2))

    def __str__(self):
        return f"Edge({self.vertices})"

    def __repr__(self):
        return str(self)

    def is_vertex_on_edge(self, vertex: Virtex):
        """
        Check if the vertex is on the edge
        :param vertex: Vertex
        :return: bool
        """
        # check if the vertex is on the line segment

    def get_slope(self):
        """
        Get the slope of the edge
        :return: float
        """
        # get the slope of the line segment
        vertex1 = self.half_edge1.start_vertex
        vertex2 = self.half_edge1.end_vertex
        return (vertex2.coords[1] - vertex1.coords[1]) / (vertex2.coords[0] - vertex1.coords[0])

    def create_split_edge(self, split_at: Virtex):
        # match slope of the line segment
        p = split_at.coords
        a = self.half_edge1.start_vertex.coords
        b = self.half_edge1.end_vertex.coords
        if (p[0] - a[0]) * (b[1] - a[1]) == (p[1] - a[1]) * (b[0] - a[0]):
            # Check if the point is within the line segment.
            if (min(a[0], b[0]) <= p[0] <= max(a[0], b[0])) and (min(a[1], b[1]) <= p[1] <= max(a[1], b[1])):
                pass
            else:
                return False
        else:
            return False

        # create split edges and half edges and return them
        # split the edge at the vertex
        # create two new edges and corresponding four half edges
        # return the two new edges and four half edges

        # create two new half edges
        new_half_edge1 = HalfEdge(start_vertex=self.half_edge1.start_vertex, end_vertex=split_at)
        new_half_edge2 = HalfEdge(start_vertex=split_at, end_vertex=self.half_edge1.end_vertex)
        new_half_edge1_opposite = HalfEdge(start_vertex=split_at, end_vertex=self.half_edge1.start_vertex)
        new_half_edge2_opposite = HalfEdge(start_vertex=self.half_edge1.end_vertex, end_vertex=split_at)

        # assign the next and previous half edges
        new_half_edge1.next = new_half_edge2
        new_half_edge2.next = new_half_edge1_opposite
        new_half_edge1_opposite.next = new_half_edge2_opposite
        new_half_edge2_opposite.next = new_half_edge1

        new_half_edge1.previous = new_half_edge2_opposite
        new_half_edge2.previous = new_half_edge1
        new_half_edge1_opposite.previous = new_half_edge2
        new_half_edge2_opposite.previous = new_half_edge1_opposite

        # create edges from the half edges
        new_edge1 = Edge(new_half_edge1, new_half_edge2)
        new_edge2 = Edge(new_half_edge1_opposite, new_half_edge2_opposite)

        # assign the edges to the half edges
        new_half_edge1.edge = new_edge1
        new_half_edge2.edge = new_edge1

        new_half_edge1_opposite.edge = new_edge2
        new_half_edge2_opposite.edge = new_edge2

        # assign the half edges to the vertices
        new_half_edge1.start_vertex.half_edges.append(new_half_edge1)
        new_half_edge1.start_vertex.half_edges.append(new_half_edge1_opposite)

        new_half_edge1.end_vertex.half_edges.append(new_half_edge2)
        new_half_edge1.end_vertex.half_edges.append(new_half_edge2_opposite)

        # assign the edges to the vertices
        new_half_edge1.start_vertex.edges.append(new_edge1)
        new_half_edge1.end_vertex.edges.append(new_edge1)









