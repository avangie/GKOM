import struct
from colorsys import hls_to_rgb as hls
from random import uniform

import numpy as np
from pyrr import Matrix44, Quaternion, matrix44


import moderngl
from _main import SetupScene
from shaders import *
from particle_emitter import Particles


def grid(size, steps):
    u = np.repeat(np.linspace(-size, size, steps), 2)
    v = np.tile([-size, size], steps)
    w = np.zeros(steps * 2)
    return np.concatenate([np.dstack([u, v, w]), np.dstack([v, u, w])])

def random_color():
    return hls(uniform(0.0, 1.0), 0.5, 0.5)

class Scene(SetupScene):
    title = "Combined Objects"
    gl_version = (3, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ship_position = np.array([0.0, 13, 0.0], dtype=np.float32)
        self.enemies_position_list = []
        for i in np.arange(-12, 15, 3):
            for j in np.arange(0, 12, 3):
                self.enemies_position_list.append(np.array([i, -14, j], dtype=np.float32))
        self.grid_size = 15
        self.enemies_list = []
        # Initialize SimpleGrid
        self.prog_grid = self.ctx.program(
            vertex_shader=vertex_shader_grid,
            fragment_shader=fragment_shader_grid
        )
        self.mvp_grid = self.prog_grid['Mvp']
        self.vbo_grid = self.ctx.buffer(grid(self.grid_size, 10).astype('f4'))
        self.vao_grid = self.ctx.simple_vertex_array(self.prog_grid, self.vbo_grid, 'in_vert')

        # Initialize Ship
        self.ship_color = random_color()
        self.prog_ship = self.ctx.program(
            vertex_shader=vertex_shader_bullet,
            fragment_shader=fragment_shader_bullet
        )

        self.mvp_ship = self.prog_ship['Mvp']
        self.light_ship = self.prog_ship['Light']

        obj = self.load_scene('spaceship.obj')
        #self.rotate_ship(180.0, [0.0, 1.0, 0.0])
        self.vbo_ship = self.ctx.buffer(struct.pack(
            '15f',
            *self.ship_color,
            0.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
        ))
        vao_wrapper = obj.root_nodes[0].mesh.vao
        vao_wrapper.buffer(self.vbo_ship, '3f 3f 9f/i', ['in_color', 'in_origin', 'in_basis'])
        self.vao_ship = vao_wrapper.instance(self.prog_ship)

        # Initialize Enemy
        self.prog_enemy = self.ctx.program(
            vertex_shader=vertex_shader_bullet,
            fragment_shader=fragment_shader_bullet
        )

        self.mvp_enemy = self.prog_enemy['Mvp']
        self.light_enemy = self.prog_enemy['Light']

        obj = self.load_scene('enemy.obj')
        for i in range(36):
            self.enemy_color = random_color()
            #self.rotate_enemy(180.0, [0.0, 1.0, 0.0])
            self.vbo_enemy = self.ctx.buffer(struct.pack(
                '15f',
                *self.enemy_color,
                0.0, 0.0, 0.0,
                1.0, 0.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 0.0, 1.0,
            ))
            vao_wrapper = obj.root_nodes[0].mesh.vao
            vao_wrapper.buffer(self.vbo_enemy, '3f 3f 9f/i', ['in_color', 'in_origin', 'in_basis'])
            self.enemies_list.append(vao_wrapper.instance(self.prog_enemy))


    def key_event(self, key, action, modifiers):
        """Handle key events."""
        if action == self.wnd.keys.ACTION_PRESS:
            # Calculate the step size based on grid size and number of steps
            step_size = 2 * self.grid_size / 10
            if key == self.wnd.keys.UP:
                print("UP PRESSED")
                print(self.ship_position)
                if self.ship_position[2] < 9:
                    self.ship_position[2] += step_size  # Move up
                else:
                    print('CANT GO HIGHER')
            elif key == self.wnd.keys.DOWN:
                print("DOWN PRESSED")
                print(self.ship_position)
                if self.ship_position[2] > 0:
                    self.ship_position[2] -= step_size  # Move down
                else:
                    print('CANT GO LOWER')
            elif key == self.wnd.keys.LEFT:
                print("LEFT PRESSED")
                print(self.ship_position)
                if self.ship_position[0] < 12:
                    self.ship_position[0] += step_size  # Move left
                else:
                    print("CANNOT LEAVE THE BOARD ")
            elif key == self.wnd.keys.RIGHT:
                print("RIGHT PRESSED")
                print(self.ship_position)
                if self.ship_position[0] > -12:
                    self.ship_position[0] -= step_size  # Move left
                else:
                    print("CANNOT LEAVE THE BOARD ")
            elif key == self.wnd.keys.Z:
                print("DOWN PRESSED")
                print(self.ship_position)
                if self.ship_position[1] > -12:
                    self.ship_position[1] -= step_size  # Move left
                else:
                    print("CANNOT LEAVE THE BOARD ")
            elif key == self.wnd.keys.X:
                print("UP PRESSED")
                print(self.ship_position)
                if self.ship_position[1] < 12:
                    self.ship_position[1] += step_size  # Move left
                else:
                    print("CANNOT LEAVE THE BOARD ")
            elif key == self.wnd.keys.SPACE:
                print("BULLET SHOT")

    def render(self, time, frame_time):

        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Render SimpleGrid
        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (0.0, 30.0, 30.0),
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        )
        self.mvp_grid.write((proj * lookat).astype('f4'))
        self.vao_grid.render(moderngl.LINES)

        # Render Ship
        scale_factor = 0.1
        self.prog_ship['scale_factor'].value = scale_factor
        camera_pos = (20, 20, -20.0)

        ship_model = Matrix44.from_translation(self.ship_position).astype('f4')
        ship_mvp = (proj * lookat * ship_model).astype('f4')
        self.mvp_ship.write(ship_mvp.tobytes())

        self.light_ship.value = camera_pos
        self.vao_ship.render()

        # Render Enemy
        for i in range(36):
            scale_factor = 0.1
            self.prog_enemy['scale_factor'].value = scale_factor
            camera_pos = (20, 20, -20.0)

            enemy_model = Matrix44.from_translation(self.enemies_position_list[i]).astype('f4')
            enemy_mvp = (proj * lookat * enemy_model).astype('f4')
            self.mvp_enemy.write(enemy_mvp.tobytes())

            self.light_enemy.value = camera_pos
            self.enemies_list[i].render()


if __name__ == '__main__':
    Scene.run()
