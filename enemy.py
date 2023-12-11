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

def Cube(position):
    glBegin(GL_QUADS)
    for face in faces:
        glColor3fv(colors[0])
        for vertex in face:
            glVertex3fv([v + p for v, p in zip(vertices[vertex], position)])
    glEnd()

def save_to_obj(filename, vertices, faces, all_positions):
    with open(filename, 'w') as f:
        for i, position in enumerate(all_positions):
            for vertex in vertices:
                f.write(f"v {' '.join(map(str, [v + p for v, p in zip(vertex, position)]))}\n")
            for face in faces:
                f.write(f"f {' '.join(map(lambda x: str(x + 1 + i * 8), face))}\n")

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(-10.0, 0.0, -30)

    glEnable(GL_DEPTH_TEST)
    glClearDepth(1.0)

    all_positions = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_to_obj("enemy.obj", vertices, faces, all_positions)
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for position in positions:
            Cube(position)
            all_positions.append(position)

        pygame.display.flip()
        pygame.time.wait(10)

main()
