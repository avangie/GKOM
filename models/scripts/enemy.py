import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

faces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (
    (1, 0, 1),
)

positions = [
    (0, -4, 0),
    (0, -2, 0),
    (0, 0, 0),
    (2, 0, 0),
    (2, 2, 0),
    (4, 2, 0),
    (4, 4, 0),
    (4, 0, 0),
    (4, -2, 0),
    (4, -4, 0),
    (4, 8, 0),
    (6, 0, 0),
    (6, 4, 0),
    (6, 6, 0),
    (6, -2, 0),
    (6, -6, 0),
    (8, -6, 0),
    (8, -2, 0),
    (8, 0, 0),
    (8, 2, 0),
    (8, 4, 0),
    (10, 0, 0),
    (10, 2, 0),
    (10, 4, 0),
    (10, -2, 0),
    (12, -6, 0),
    (12, 0, 0),
    (12, 2, 0),
    (12, 4, 0),
    (12, -2, 0),
    (14, 6, 0),
    (14, 4, 0),
    (14, 0, 0),
    (14, -2, 0),
    (14, -6, 0),
    (16, 8, 0),
    (16, 4, 0),
    (16, 2, 0),
    (16, 0, 0),
    (16, -2, 0),
    (16, -4, 0),
    (18, 2, 0),
    (18, 0, 0),
    (20, 0, 0),
    (20, -2, 0),
    (20, -4, 0)
]

def Cube(position, vertex_dict, vertices_list, faces_list):
    glBegin(GL_QUADS)
    for face in faces:
        glColor3fv(colors[0])
        face_indices = []
        for vertex in face:
            vertex_coordinates = [v + p for v, p in zip(vertices[vertex], position)]
            if tuple(vertex_coordinates) not in vertex_dict:
                vertex_dict[tuple(vertex_coordinates)] = len(vertices_list) + 1
                vertices_list.append(vertex_coordinates)
            face_indices.append(vertex_dict[tuple(vertex_coordinates)])
        faces_list.append(face_indices)
        glVertex3fv(vertices_list[face_indices[0] - 1])
        glVertex3fv(vertices_list[face_indices[1] - 1])
        glVertex3fv(vertices_list[face_indices[2] - 1])
        glVertex3fv(vertices_list[face_indices[3] - 1])
    glEnd()


def save_to_obj(filename, vertices_list, faces_list):
    unique_vertices = {}
    new_vertices = []
    new_faces = []

    for face_indices in faces_list:
        new_face = []
        for idx in face_indices:
            vertex = vertices_list[idx - 1]
            vertex_tuple = tuple(vertex)
            if vertex_tuple not in unique_vertices:
                unique_vertices[vertex_tuple] = len(new_vertices) + 1
                new_vertices.append(vertex)
            new_face.append(unique_vertices[vertex_tuple])

        new_faces.append(new_face)

    with open(filename, 'w') as f:
        for vertex in new_vertices:
            f.write(f"v {' '.join(map(str, vertex))}\n")
        for face in new_faces:
            f.write(f"f {' '.join(map(str, face))}\n")


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(-10.0, 0.0, -30)

    glEnable(GL_DEPTH_TEST)
    glClearDepth(1.0)

    vertex_dict = {}
    vertices_list = []
    faces_list = []

    while True:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for i, position in enumerate(positions):
                Cube(position, vertex_dict, vertices_list, faces_list)
        
        save_to_obj("../enemy.obj", vertices_list, faces_list)

        pygame.display.flip()
        pygame.time.wait(5000)
        break

if __name__ == "__main__":
    main()
