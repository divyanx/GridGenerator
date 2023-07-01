import math
import matplotlib.pyplot as plt
import numpy as np

# from polymesh.edge import Edges
from polymesh.face import Faces
from polymesh.half_edge import HalfEdges
from polymesh.vertices import Vertices


class Mesh:
    def __init__(self):
        self.vertices = Vertices()
        self.half_edges = HalfEdges()
        # self.edges = Edges()
        self.faces = Faces()

    def add_face(self, vertex_coords_list):
        print("Creating faces with vertices: ", vertex_coords_list)
        # add vertices
        vertex_id_list = []
        for vertex_coords in vertex_coords_list:
            vertex_id = self.vertices.add_vertex(vertex_coords)
            vertex_id_list.append(vertex_id)

        half_edge_id_list = []
        for i in range(len(vertex_id_list)):
            start_vertex_id = vertex_id_list[i]
            end_vertex_id = vertex_id_list[(i + 1) % len(vertex_id_list)]
            half_edge_id = self.add_new_half_edge(start_vertex_id, end_vertex_id)
            half_edge_id_list.append(half_edge_id)

        # assign next and prev half edges
        for i in range(len(half_edge_id_list)):
            half_edge_id = half_edge_id_list[i]
            next_half_edge_id = half_edge_id_list[(i + 1) % len(half_edge_id_list)]
            prev_half_edge_id = half_edge_id_list[i - 1]
            self.half_edges.set_next_half_edge_id(half_edge_id, next_half_edge_id)
            self.half_edges.set_prev_half_edge_id(half_edge_id, prev_half_edge_id)
            self.half_edges.set_twin_for_half_edge(half_edge_id, None)

        # select the half edge with the smallest start vertex id as the representative half edge
        representative_half_edge_id = min(half_edge_id_list)
        face_id = self.faces.add_new_face(representative_half_edge_id)

        for half_edge_id in half_edge_id_list:
            self.half_edges.set_face_for_half_edge(half_edge_id, face_id)

        return face_id

    def add_parent_hole_relation(self, parent_face_id, hole_face_id):
        self.faces.face_parent_face_dict[hole_face_id] = parent_face_id
        if parent_face_id not in self.faces.face_holes_dict:
            self.faces.face_holes_dict[parent_face_id] = []
        self.faces.face_holes_dict[parent_face_id].append(hole_face_id)

    def get_face_all_half_edge_ids(self, face_id):
        representative_half_edge_id = self.faces.get_face_half_edge_id(face_id)
        half_edge_id = representative_half_edge_id
        half_edge_id_list = []
        while True:
            half_edge_id_list.append(half_edge_id)
            half_edge_id = self.half_edges.get_next_half_edge_id(half_edge_id)
            if half_edge_id == representative_half_edge_id:
                break
        return half_edge_id_list

    def plot_faces(self, face_ids, head_width=0.3, head_length=0.3, shift=0.3):
        "Plot faces as polygons bounded by surrounding half edges"
        for face_id in face_ids:
            half_edge_id_list = self.get_face_all_half_edge_ids(face_id)
            # find arrow head width and length based on size of first half edge
            first_half_edge_id = half_edge_id_list[0]
            start_vertex_id = self.half_edges.get_start_vertex_id(first_half_edge_id)
            end_vertex_id = self.half_edges.get_end_vertex_id(first_half_edge_id)
            start_vertex_coords = self.vertices.get_vertex_coords(start_vertex_id)
            end_vertex_coords = self.vertices.get_vertex_coords(end_vertex_id)

            for half_edge_id in half_edge_id_list:
                start_vertex_id = self.half_edges.get_start_vertex_id(half_edge_id)
                end_vertex_id = self.half_edges.get_end_vertex_id(half_edge_id)
                start_vertex_coords = self.vertices.get_vertex_coords(start_vertex_id)
                end_vertex_coords = self.vertices.get_vertex_coords(end_vertex_id)
                start_vertex_coords, end_vertex_coords = self.shift_line(start_vertex_coords, end_vertex_coords, shift)
                # get head width and head length based on max distance between vertices
                # plot it as an arrow
                plt.arrow(start_vertex_coords[0], start_vertex_coords[1], end_vertex_coords[0] - start_vertex_coords[0],
                          end_vertex_coords[1] - start_vertex_coords[1], head_width=head_width, head_length=head_length,
                          fc='k', ec='k')

            # write face id in the middle of the face
            # find the center of the face
            center_x = 0
            center_y = 0
            x_coords = []
            y_coords = []
            for half_edge_id in half_edge_id_list:
                start_vertex_id = self.half_edges.get_start_vertex_id(half_edge_id)
                end_vertex_id = self.half_edges.get_end_vertex_id(half_edge_id)
                start_vertex_coords = self.vertices.get_vertex_coords(start_vertex_id)
                end_vertex_coords = self.vertices.get_vertex_coords(end_vertex_id)
                x_coords.append(start_vertex_coords[0])
                y_coords.append(start_vertex_coords[1])
                center_x += start_vertex_coords[0]
                center_y += start_vertex_coords[1]

            center_x /= len(half_edge_id_list)
            center_y /= len(half_edge_id_list)

            color = np.random.rand(3, )
            # write the face if with a circle around it
            plt.text(center_x, center_y, str(face_id), fontsize=12, horizontalalignment='center',
                     verticalalignment='center', color=color)

            # fill the face with the same color
            plt.fill(x_coords, y_coords, color=color, alpha=0.3)
        plt.show()

    def add_vertex(self, coords):
        vertex_id = self.vertices.add_vertex(coords)
        return vertex_id

    @staticmethod
    def is_point_on_line_segment(start_vertex_coords, end_vertex_coords, point_coords):
        # check if the point is on the line segment

        # convert typle to numpy array
        start_vertex_coords = np.array(start_vertex_coords)
        end_vertex_coords = np.array(end_vertex_coords)
        if np.allclose(start_vertex_coords, point_coords) or np.allclose(end_vertex_coords, point_coords):
            return True
        if np.allclose(start_vertex_coords, end_vertex_coords):
            return False
        if np.allclose(np.cross(end_vertex_coords - start_vertex_coords, point_coords - start_vertex_coords), 0):
            if np.dot(end_vertex_coords - start_vertex_coords, point_coords - start_vertex_coords) >= 0 and np.dot(
                    start_vertex_coords - end_vertex_coords, point_coords - end_vertex_coords) >= 0:
                return True
        return False

    def partition_half_edge_at_point(self, half_edge_id, point_coords, partition_twin=True):
        # check if the point is on the half edge
        start_vertex_id = self.half_edges.get_start_vertex_id(half_edge_id)
        end_vertex_id = self.half_edges.get_end_vertex_id(half_edge_id)
        start_vertex_coords = self.vertices.get_vertex_coords(start_vertex_id)
        end_vertex_coords = self.vertices.get_vertex_coords(end_vertex_id)

        # check if the point is on the half edge
        if np.allclose(start_vertex_coords, point_coords) or np.allclose(end_vertex_coords, point_coords):
            return half_edge_id

        # check if the point is on the line segment
        if not self.is_point_on_line_segment(start_vertex_coords, end_vertex_coords, point_coords):
            return None

        # create a new vertex at the point
        new_vertex_id = self.add_vertex(point_coords)

        # create a new half edge from the start vertex to the new vertex
        new_half_edge_id = self.add_new_half_edge(start_vertex_id, new_vertex_id)
        # create a new half edge from the new vertex to the end vertex
        new_half_edge_id_2 = self.add_new_half_edge(new_vertex_id, end_vertex_id)

        # set the next and prev half edges
        next_half_edge_id = self.half_edges.get_next_half_edge_id(half_edge_id)
        prev_half_edge_id = self.half_edges.get_prev_half_edge_id(half_edge_id)
        self.half_edges.set_next_half_edge_id(half_edge_id, new_half_edge_id)
        self.half_edges.set_prev_half_edge_id(new_half_edge_id, half_edge_id)
        self.half_edges.set_next_half_edge_id(new_half_edge_id, new_half_edge_id_2)
        self.half_edges.set_prev_half_edge_id(new_half_edge_id_2, new_half_edge_id)
        self.half_edges.set_next_half_edge_id(new_half_edge_id_2, next_half_edge_id)
        self.half_edges.set_prev_half_edge_id(next_half_edge_id, new_half_edge_id_2)
        self.half_edges.set_prev_half_edge_id(half_edge_id, prev_half_edge_id)
        self.half_edges.set_next_half_edge_id(prev_half_edge_id, half_edge_id)

        # if half edge was a representative half edge for a face, set the new half edge as the representative half edge
        face_id = self.half_edges.get_face_for_half_edge(half_edge_id)
        if face_id is not None:
            if start_vertex_id < end_vertex_id:
                self.half_edges.set_representative_half_edge_for_face(face_id, new_half_edge_id)
                self.faces.set_face_and_half_edge(face_id, new_half_edge_id)
            else:
                self.half_edges.set_representative_half_edge_for_face(face_id, new_half_edge_id_2)
                self.faces.set_face_and_half_edge(face_id, new_half_edge_id_2)

        # set the twin half edges
        if not partition_twin:
            return new_half_edge_id, new_half_edge_id_2, None, None

        twin_half_edge_id = self.half_edges.get_twin_half_edge_id(half_edge_id)
        if twin_half_edge_id is None:
            return new_half_edge_id, new_half_edge_id_2, None, None

        # use the same function to partition the twin half edge
        new_twin_half_edge_id, new_twin_half_edge_id_2, _, _ = self.partition_half_edge_at_point(twin_half_edge_id,
                                                                                                 point_coords,
                                                                                                 partition_twin=False)
        self.half_edges.set_twin_half_edge_id(new_half_edge_id, new_twin_half_edge_id_2)
        self.half_edges.set_twin_half_edge_id(new_half_edge_id_2, new_twin_half_edge_id)
        self.half_edges.set_twin_half_edge_id(new_twin_half_edge_id, new_half_edge_id_2)
        self.half_edges.set_twin_half_edge_id(new_twin_half_edge_id_2, new_half_edge_id)
        return new_half_edge_id, new_half_edge_id_2, new_twin_half_edge_id, new_twin_half_edge_id_2

    def get_half_edge_between_points(self, start_coord, end_coord):
        start_vertex_id = self.vertices.get_vertex_id(start_coord)
        end_vertex_id = self.vertices.get_vertex_id(end_coord)
        if start_vertex_id is None or end_vertex_id is None:
            return None
        half_edge_id = self.half_edges.get_half_edge_between_vertices(start_vertex_id, end_vertex_id)
        return half_edge_id

    def get_half_edge_between_vertices(self, start_vertex_id, end_vertex_id):
        half_edge_id = self.half_edges.get_half_edge_between_vertices(start_vertex_id, end_vertex_id)
        return half_edge_id

    def add_new_half_edge(self, start_vertex_id, end_vertex_id):
        # create a half edge from the start vertex to the end vertex
        half_edge_id = self.half_edges.add_new_half_edge(start_vertex_id, end_vertex_id)
        #
        self.vertices.add_starting_half_edge(start_vertex_id, half_edge_id)
        self.vertices.add_ending_half_edge(end_vertex_id, half_edge_id)

        return half_edge_id

    def join_two_vertices_with_half_edge_within_a_face(self, start_vertex_id, end_vertex_id, face_id):
        # join the two vertices with a half edge
        # reassign all the next and prev for new and old half edges correctly
        # if create_twin is True, create a twin half edge and reassign all the next and prev for new and old half edges

        # get the half edge between the two vertices
        half_edge_id = self.get_half_edge_between_vertices(start_vertex_id, end_vertex_id)
        if half_edge_id is not None:
            return half_edge_id

        # create a new half edge
        half_edge_id = self.add_new_half_edge(start_vertex_id, end_vertex_id)
        # get the twin half edge
        half_edge_id_2 = self.add_new_half_edge(end_vertex_id, start_vertex_id)

        # set the twin half edges
        self.half_edges.set_twin_half_edge_id(half_edge_id, half_edge_id_2)
        self.half_edges.set_twin_half_edge_id(half_edge_id_2, half_edge_id)

        # half edges ending at start vertex
        ending_at_start_vertex = self.vertices.get_ending_half_edges(start_vertex_id)
        # half edges starting at start vertex
        starting_at_start_vertex = self.vertices.get_starting_half_edges(start_vertex_id)
        # half edges ending at end vertex
        ending_at_end_vertex = self.vertices.get_ending_half_edges(end_vertex_id)
        # half edges starting at end vertex
        starting_at_end_vertex = self.vertices.get_starting_half_edges(end_vertex_id)

        half_edge_ending_at_start = None
        half_edge_starting_at_start = None
        half_edge_ending_at_end = None
        half_edge_starting_at_end = None

        for half_edge in ending_at_start_vertex:
            if self.half_edges.get_face_id(half_edge) == face_id:
                half_edge_ending_at_start = half_edge
                break
        for half_edge in starting_at_start_vertex:
            if self.half_edges.get_face_id(half_edge) == face_id:
                half_edge_starting_at_start = half_edge
                break
        for half_edge in ending_at_end_vertex:
            if self.half_edges.get_face_id(half_edge) == face_id:
                half_edge_ending_at_end = half_edge
                break
        for half_edge in starting_at_end_vertex:
            if self.half_edges.get_face_id(half_edge) == face_id:
                half_edge_starting_at_end = half_edge
                break

        # set the next and prev for the new half edges
        self.half_edges.set_next_half_edge_id(half_edge_id, half_edge_starting_at_end)
        self.half_edges.set_prev_half_edge_id(half_edge_id, half_edge_ending_at_start)
        self.half_edges.set_next_half_edge_id(half_edge_id_2, half_edge_starting_at_start)
        self.half_edges.set_prev_half_edge_id(half_edge_id_2, half_edge_ending_at_end)
        self.half_edges.set_prev_half_edge_id(half_edge_starting_at_end, half_edge_id)
        self.half_edges.set_next_half_edge_id(half_edge_ending_at_start, half_edge_id)
        self.half_edges.set_prev_half_edge_id(half_edge_starting_at_start, half_edge_id_2)
        self.half_edges.set_next_half_edge_id(half_edge_ending_at_end, half_edge_id_2)

        # get all the half edges in the face of which the half edge is a part of
        face_1_half_edges = []
        current_half_edge = half_edge_id
        start_half_edge = half_edge_id
        while True:
            face_1_half_edges.append(current_half_edge)
            current_half_edge = self.half_edges.get_next_half_edge(current_half_edge)
            if current_half_edge == start_half_edge:
                break

        face_2_half_edges = []
        current_half_edge = half_edge_id_2
        start_half_edge = half_edge_id_2
        while True:
            face_2_half_edges.append(current_half_edge)
            current_half_edge = self.half_edges.get_next_half_edge(current_half_edge)
            if current_half_edge == start_half_edge:
                break


        # representative half edge for face 1
        representative_half_edge_1 = min(face_1_half_edges)
        # representative half edge for face 2
        representative_half_edge_2 = min(face_2_half_edges)

        # delete old face
        self.faces.remove_face(face_id)

        # create new faces
        face_1_id = self.faces.add_new_face(representative_half_edge_1)
        face_2_id = self.faces.add_new_face(representative_half_edge_2)

        # set the face ids for the half edges
        for half_edge in face_1_half_edges:
            self.half_edges.set_face_for_half_edge(half_edge, face_1_id)
        for half_edge in face_2_half_edges:
            self.half_edges.set_face_for_half_edge(half_edge, face_2_id)

        return half_edge_id, half_edge_id_2, face_1_id, face_2_id

    def get_next_half_edge_based_on_angle(self, half_edge, next_candidates_list):
        # get the angle of the half edge
        half_edge_angle = self.get_angle_of_half_edge(half_edge)
        # get the angles of the next candidates
        next_candidates_angles = [self.get_angle_of_half_edge(next_candidate) for next_candidate in
                                  next_candidates_list]
        # get the difference between the angles

        half_edge_angle = half_edge_angle + np.pi
        # if the angle is greater than 2pi, subtract 2pi
        if half_edge_angle > 2 * np.pi:
            half_edge_angle = half_edge_angle - 2 * np.pi
        # get the angle difference between the half edge and the next candidates

        angle_differences = [next_candidate_angle - half_edge_angle for next_candidate_angle in
                             next_candidates_angles]


        # get the index of the next candidate with the smallest angle difference clockwise i.e. the smallest positive
        # angle difference
        next_candidate_index = np.argmin([angle_difference if angle_difference >= 0 else np.inf for angle_difference in
                                          angle_differences])
        # return the next candidate
        return next_candidates_list[next_candidate_index]

    def get_the_prev_half_edge_based_on_angle(self, half_edge, prev_candidates_list):
        # previous will the one with the largest angle difference
        # get the angle of the half edge
        half_edge_angle = self.get_angle_of_half_edge(half_edge)
        # get the angles of the next candidates
        prev_candidates_angles = [self.get_angle_of_half_edge(prev_candidate) for prev_candidate in
                                  prev_candidates_list]
        # get opposite of the angle of the half edge which should be between 0 and 2pi
        half_edge_angle = half_edge_angle + np.pi
        # if the angle is greater than 2pi, subtract 2pi
        if half_edge_angle > 2 * np.pi:
            half_edge_angle = half_edge_angle - 2 * np.pi

        # get the difference between the angles
        angle_differences = [prev_candidate_angle - half_edge_angle for prev_candidate_angle in
                             prev_candidates_angles]

        # the prev candidate will be the one with the smallest angle difference anti clockwise i.e. the smallest
        # difference
        prev_candidate_index = np.argmin([angle_difference if angle_difference >= 0 else np.inf for angle_difference in
                                          angle_differences])

    def get_angle_of_half_edge(self, half_edge):
        # get the vertices of the half edge
        start_vertex_coords, end_vertex_coords = self.get_vertices_coords_of_half_edge(half_edge)

        # convert coords to np array
        start_vertex_coords = np.array(start_vertex_coords)
        end_vertex_coords = np.array(end_vertex_coords)

        # get the vector
        vector = end_vertex_coords - start_vertex_coords

        # get the angle of the vector
        # angles will always be between 0 and 2pi
        angle = np.arctan2(vector[1], vector[0])
        if angle < 0:
            angle += 2 * np.pi
        return angle

    def get_vertices_coords_of_half_edge(self, half_edge_id):
        start_vertex_id = self.half_edges.get_start_vertex_id(half_edge_id)
        vertex_coords = self.vertices.get_vertex_coords(start_vertex_id)
        end_vertex_id = self.half_edges.get_end_vertex_id(half_edge_id)
        vertex_coords_2 = self.vertices.get_vertex_coords(end_vertex_id)
        return vertex_coords, vertex_coords_2

    @staticmethod
    def shift_line(start_vertex_coords, end_vertex_coords, shift):
        # shift the line perpendicular to the line
        # get the vector
        start_vertex_coords = np.array(start_vertex_coords)
        end_vertex_coords = np.array(end_vertex_coords)
        vector = end_vertex_coords - start_vertex_coords
        # get the angle of the vector
        angle = np.arctan2(vector[1], vector[0])
        # get the perpendicular angle
        perpendicular_angle = angle + np.pi / 2
        # add shift to the start and end vertex coords in the perpendicular direction
        start_vertex_coords = start_vertex_coords + shift * np.array([np.cos(perpendicular_angle), np.sin(perpendicular_angle)])
        end_vertex_coords = end_vertex_coords + shift * np.array([np.cos(perpendicular_angle), np.sin(perpendicular_angle)])

        # return them as the tuple
        return tuple(start_vertex_coords), tuple(end_vertex_coords)
