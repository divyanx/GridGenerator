import numpy as np

from polymesh.mesh import Mesh
from polymesh.virtex import Virtex

coords_list = [1, 2]
coords_tuple = (2, 4)
coords_ndarray = np.array([3, 6])

coords_np_1 = np.array(coords_list)
coords_np_2 = np.array(coords_tuple)
coords_np_3 = np.ndarray(coords_ndarray)

print(coords_np_1)
print(coords_np_2)
print(coords_np_3)


vertex_1 = Virtex(np.array([0, 0]))
vertex_2 = Virtex(np.array([1, 0]))
vertex_3 = Virtex(np.array([1, .7]))
vertex_4 = Virtex(np.array([.7, 1]))
vertex_5 = Virtex(np.array([0, 1]))

mesh = Mesh()
mesh.add_face_from_vertices_list([vertex_1, vertex_2, vertex_3, vertex_4, vertex_5])

vertex_7 = Virtex(np.array([.3, .3]))
vertex_8 = Virtex(np.array([.3, .6]))
vertex_9 = Virtex(np.array([.6, .6]))
vertex_10 = Virtex(np.array([.6, .3]))

mesh.add_face_from_vertices_list([vertex_7, vertex_8, vertex_9, vertex_10])
mesh.plot()
print(mesh)




