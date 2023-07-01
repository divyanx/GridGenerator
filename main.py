import numpy as np

from polymesh.mesh import Mesh

mesh = Mesh()

vertex_cord_list = [(0, 0), (10, 0), (10, 7), (6, 10), (0, 10)]

faceId = mesh.add_face(vertex_cord_list)

# get halfedge id between vertex (0,0) and (10,0)
half_edge_id = mesh.get_half_edge_between_points((0, 0), (10, 0))

print("Half edge id: ", half_edge_id)
# partition the half edge at the point (5,0)
mesh.partition_half_edge_at_point(half_edge_id, (5, 0))

print(mesh.half_edges.half_edge_vertex_dict)

hole_vertex_cord_list = [(2, 2), (4, 2), (4, 4), (2, 4)]

holeId = mesh.add_face(hole_vertex_cord_list)

print(mesh.half_edges.half_edge_vertex_dict)

mesh.add_parent_hole_relation(faceId, holeId)
print("faceId: ", faceId, " holeId: ", holeId)
mesh.plot_faces([faceId, holeId])

