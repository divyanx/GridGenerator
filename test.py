import numpy as np

from polymesh.mesh import Mesh

mesh = Mesh()

vertex_cord_list = [(0, 0), (10, 0), (10, 7), (6, 10), (0, 10)]

faceId = mesh.add_face(vertex_cord_list)

# get halfedge id between vertex (0,0) and (10,7)
mesh.join_two_vertices_with_half_edge_within_a_face(0, 3, 0)

mesh.plot_faces([1, 2])



