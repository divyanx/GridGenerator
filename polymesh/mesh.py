import math
import matplotlib.pyplot as plt
import numpy as np

from .half_edge import HalfEdge
from .virtex import Virtex
from .face import Face
from .edge import Edge


class Mesh:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.faces = []
        self.half_edges = []

    def __str__(self):
        return f"Mesh(\nVertices: {self.vertices},\n Edges: {self.edges}, \nFaces: {self.faces})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((tuple(self.vertices), tuple(self.edges), tuple(self.faces), tuple(self.half_edges)))

    def add_face_from_vertices_list(self, vertices: list[Virtex]):
        """
        Add face from list of vertices (in order)
        :type vertices: list[Virtex]
        :param vertices: list of vertices
        :return: face
        """
        self.vertices.extend(vertices)
        half_edges = []
        half_edges_opposite = []
        for i in range(len(vertices)):
            he = HalfEdge(vertices[i], vertices[(i + 1) % len(vertices)])
            half_edges.append(he)
            self.half_edges.append(he)
            he = HalfEdge(vertices[(i + 1) % len(vertices)], vertices[i])
            half_edges_opposite.append(he)
            self.half_edges.append(he)

        half_edges_opposite = half_edges_opposite[::-1]

        n = len(half_edges)
        for i in range(n):
            half_edges[i].opposite = half_edges_opposite[(n - i - 1) % n]
            half_edges_opposite[i].opposite = half_edges[(n - i - 1) % n]

            # assign next and prev
            half_edges[i].next = half_edges[(i + 1) % n]
            half_edges[i].prev = half_edges[(i - 1) % n]

            half_edges_opposite[i].next = half_edges_opposite[(i - 1) % n]
            half_edges_opposite[i].prev = half_edges_opposite[(i + 1) % n]

        print("half_edges", half_edges)
        print("half_edges_opposite", half_edges_opposite)

        edges, half_edges, half_edges_opposite = Mesh.assign_edges_from_half_edge_pair_lists(
            half_edges, half_edges_opposite[:: -1]
        )

        self.edges.extend(edges)

        if Mesh.check_if_list_half_edges_clockwise(half_edges):
            clock_wise_half_edges = half_edges
            counter_clock_wise_half_edges = half_edges_opposite
        else:
            clock_wise_half_edges = half_edges_opposite
            counter_clock_wise_half_edges = half_edges

        # create a face with clockwise half edge
        face = Face(clock_wise_half_edges[0])
        self.faces.append(face)
        face.set_vertices_from_half_edge()
        face.set_edges_from_half_edge()
        face.set_half_edges_from_half_edge()

        for he in clock_wise_half_edges:
            he.face = face

        for he in counter_clock_wise_half_edges:
            he.face = None
            he.is_boundary = True

        return face

    @staticmethod
    def assign_edges_from_half_edge_pair_lists(half_edges: list[HalfEdge], half_edges_opposite: list[HalfEdge]):
        """
        Create edges from half edge pair lists
        :param half_edges: list of half edges
        :param half_edges_opposite: list of half edges opposite
        :return: list of edges

        """
        assert len(half_edges) == len(half_edges_opposite)
        n = len(half_edges)
        edges = []
        for i in range(n):
            assert half_edges[i].start_vertex == half_edges_opposite[i].end_vertex
            assert half_edges[i].end_vertex == half_edges_opposite[i].start_vertex
            edge = Edge(half_edges[i], half_edges_opposite[i])
            half_edges[i].edge = edge
            half_edges_opposite[i].edge = edge
            edges.append(edge)
        return edges, half_edges, half_edges_opposite

    @staticmethod
    def check_if_list_half_edges_clockwise(half_edges: list[HalfEdge]):
        """
        Check if list of half_edges is clockwise or counterclockwise
        :param half_edges: list of half_edges
        :return: True if clockwise, False if counterclockwise
        """
        # TODO: verify if the logic is correct

        area = 0
        n = len(half_edges)
        for i in range(len(half_edges)):
            from_vertex = half_edges[i].start_vertex.coords
            j = (i + 1) % n
            to_vertex = half_edges[j].start_vertex.coords
            # calculate the cross product of the two vectors
            cross = (to_vertex[0] - from_vertex[0]) * (half_edges[j].next.start_vertex.coords[1] - from_vertex[1]) - (
                    half_edges[j].next.start_vertex.coords[0] - from_vertex[0]) * (to_vertex[1] - from_vertex[1])
            area += cross / 2
        return area < 0

    def plot(self):
        """
        Plot mesh
        :return: None
        """
        # plot half_edges and vertices
        # represent half edges as arrows pointing in the direction of the half edge

        # set figure size
        plt.figure(figsize=(10, 10))

        for he in self.half_edges:
            he_shifted_start_coords, he_shifted_end_coords = Mesh.shift_half_edge_coordinates(he.start_vertex.coords,
                                                                                              he.end_vertex.coords)
            if he.is_boundary:
                plt.arrow(he_shifted_start_coords[0], he_shifted_start_coords[1],
                          he_shifted_end_coords[0] - he_shifted_start_coords[0],
                          he_shifted_end_coords[1] - he_shifted_start_coords[1], color="red", head_width=0.02, head_length=0.03)
            else:
                plt.arrow(he_shifted_start_coords[0], he_shifted_start_coords[1],
                          he_shifted_end_coords[0] - he_shifted_start_coords[0],
                          he_shifted_end_coords[1] - he_shifted_start_coords[1], color="blue", head_width=0.02, head_length=0.03)
        for v in self.vertices:
            plt.scatter(v.coords[0], v.coords[1], color="black")

        # plot faces as polygons with different colors
        for f in self.faces:
            vertices = f.vertices
            x = [v.coords[0] for v in vertices]
            y = [v.coords[1] for v in vertices]
            plt.fill(x, y, color=np.random.rand(3, ), alpha=0.5)

        plt.show()

    @staticmethod
    def shift_half_edge_coordinates(start_vertex_coords, end_vertex_coords, distance=0.02):
        x1 = start_vertex_coords[0]
        y1 = start_vertex_coords[1]
        x2 = end_vertex_coords[0]
        y2 = end_vertex_coords[1]
        direction = math.atan2(y2 - y1, x2 - x1)

        # Calculate the perpendicular direction.
        perpendicular_direction = direction + math.pi / 2

        # Calculate the coordinates of the shifted line.
        x1_shifted = x1 - distance * math.cos(perpendicular_direction)
        y1_shifted = y1 - distance * math.sin(perpendicular_direction)
        x2_shifted = x2 - distance * math.cos(perpendicular_direction)
        y2_shifted = y2 - distance * math.sin(perpendicular_direction)

        return (x1_shifted, y1_shifted), (x2_shifted, y2_shifted)
