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

def Cube(position):
    glBegin(GL_QUADS)
    for face in faces:
        glColor3fv(colors[0])
        for vertex in face:
            glVertex3fv([v + p for v, p in zip(vertices[vertex], position)])
    glEnd()

def save_to_obj(filename, vertices, faces):
    with open(filename, 'w') as f:
        for vertex in vertices:
            f.write(f"v {' '.join(map(str, vertex))}\n")
        for face in faces:
            f.write(f"f {' '.join(map(lambda x: str(x + 1), face))}\n")

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(-10.0, 0.0, -30)

    glEnable(GL_DEPTH_TEST) 
    glClearDepth(1.0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        Cube((0, -4, 0))
        Cube((0, -2, 0))
        Cube((0, 0, 0))
        Cube((2, 0, 0))
        Cube((2, 2, 0))
        Cube((4, 2, 0))
        Cube((4, 4, 0))
        Cube((4, 0, 0))
        Cube((4, -2, 0))
        Cube((4, -4, 0))
        Cube((4, 8, 0))
        Cube((6, 0, 0))
        Cube((6, 4, 0))
        Cube((6, 6, 0))
        Cube((6, -2, 0))
        Cube((6, -6, 0))
        Cube((8, -6, 0))
        Cube((8, -2, 0))
        Cube((8, 0, 0))
        Cube((8, 2, 0))
        Cube((8, 4, 0))
        Cube((10, 0, 0))
        Cube((10, 2, 0))
        Cube((10, 4, 0))
        Cube((10, -2, 0))
        Cube((12, -6, 0))
        Cube((12, 0, 0))
        Cube((12, 2, 0))
        Cube((12, 4, 0))
        Cube((12, -2, 0))
        Cube((14, 6, 0))
        Cube((14, 4, 0))
        Cube((14, 0, 0))
        Cube((14, -2, 0))
        Cube((14, -6, 0))
        Cube((16, 8, 0))
        Cube((16, 4, 0))
        Cube((16, 2, 0))
        Cube((16, 0, 0))
        Cube((16, -2, 0))
        Cube((16, -4, 0))
        Cube((18, 2, 0))
        Cube((18, 0, 0))
        Cube((20, 0, 0))
        Cube((20, -2, 0))
        Cube((20, -4, 0))

        pygame.display.flip()
        pygame.time.wait(10)
        save_to_obj("output.obj", vertices, faces)

main()
