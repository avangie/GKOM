import struct
from colorsys import hls_to_rgb as hls
from random import uniform
import numpy as np
from pyrr import Matrix44
import moderngl
from _main import SetupScene
from shaders import *
from particle_emitter import Particles
import pygame
from pygame import mixer
import os
import time as tm


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
        self.game_end = False
        self.bullet_list = []
        self.bullets_positions = []

        self.enemies_position_list = []
        for i in np.arange(-12, 15, 3):
            for j in np.arange(0, 12, 3):
                self.enemies_position_list.append(np.array([i, -14, j], dtype=np.float32))

        self.grid_size = 15
        self.enemies_list = []

        self.points = 0

        # Initialize Pygame mixer
        pygame.mixer.init()
        mixer.init()
        background_music_path = os.path.join(BASE_DIR, 'audio', 'background.mp3')

        pygame.mixer.music.load(background_music_path)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.shoot_sound_path = background_music_path = os.path.join(BASE_DIR, 'audio', 'bullet.wav')
        self.death_sound_path = background_music_path = os.path.join(BASE_DIR, 'audio', 'death.wav')

        self.shoot_sound = mixer.Sound(self.shoot_sound_path)
        self.death_sound = mixer.Sound(self.death_sound_path)

        self.death_sound.set_volume(0.3)
        self.shoot_sound.set_volume(0.3)


        # initialize SimpleGrid
        self.prog_grid = self.ctx.program(
            vertex_shader=vertex_shader_grid,
            fragment_shader=fragment_shader_grid
        )
        self.mvp_grid = self.prog_grid['Mvp']
        self.vbo_grid = self.ctx.buffer(grid(self.grid_size, 10).astype('f4'))
        self.vao_grid = self.ctx.simple_vertex_array(self.prog_grid, self.vbo_grid, 'in_vert')

        # Initialize Bullet
        self.bullet_color = random_color()
        self.prog_bullet = self.ctx.program(
            vertex_shader=vertex_shader_bullet,
            fragment_shader=fragment_shader_bullet
        )

        self.mvp_bullet = self.prog_bullet['Mvp']
        self.light_bullet = self.prog_bullet['Light']

        obj = self.load_scene('bullet.obj')
        self.vbo_bullet = self.ctx.buffer(struct.pack(
            '15f',
            *self.bullet_color,
            0.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
        ))
        self.vao_wrapper = obj.root_nodes[0].mesh.vao
        self.vao_wrapper.buffer(self.vbo_bullet, '3f 3f 9f/i', ['in_color', 'in_origin', 'in_basis'])
        self.vao_bullet = self.vao_wrapper.instance(self.prog_bullet)
        self.bullet_list.append(self.vao_wrapper.instance(self.prog_bullet))


        # Initialize Ship
        self.ship_color = random_color()
        self.prog_ship = self.ctx.program(
            vertex_shader=vertex_shader_ship,
            fragment_shader=fragment_shader_ship
        )

        self.mvp_ship = self.prog_ship['Mvp']
        self.light_ship = self.prog_ship['Light']

        obj = self.load_scene('spaceship_with_fire.obj')
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


        # initialize enemies
        self.prog_enemy = self.ctx.program(
            vertex_shader=vertex_shader_enemy,
            fragment_shader=fragment_shader_enemy
        )

        self.mvp_enemy = self.prog_enemy['Mvp']
        self.light_enemy = self.prog_enemy['Light']

        obj = self.load_scene('enemy.obj')
        for i in range(36):
            self.enemy_color = random_color()
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

        # initialize enemy movement variables
        self.enemy_current_step = 0
        self.enemy_time_since_last_step = 0
        self.enemy_step_interval = 1.0

    def update_enemy_positions(self, frame_time):
        self.enemy_time_since_last_step += frame_time

        if self.enemy_time_since_last_step >= self.enemy_step_interval:
            self.enemy_time_since_last_step = 0

            # one step up
            if self.enemy_current_step == 0:
                for i in range(len(self.enemies_list)):
                    self.enemies_position_list[i][2] += 2.0

            # three steps to the right
            elif 1 <= self.enemy_current_step <= 3:
                for i in range(len(self.enemies_list)):
                    self.enemies_position_list[i][0] -= 2.0

            # one step down
            elif self.enemy_current_step == 4:
                for i in range(len(self.enemies_list)):
                    self.enemies_position_list[i][2] -= 2.0

            # three steps to the left
            elif 5 <= self.enemy_current_step <= 7:
                for i in range(len(self.enemies_list)):
                    self.enemies_position_list[i][0] += 2.0

            # one step forward
            elif self.enemy_current_step == 8:
                for i in range(len(self.enemies_list)):
                    self.enemies_position_list[i][1] += 2.0

            # reset the step count and check if it's time to switch
            self.enemy_current_step = (self.enemy_current_step + 1) % 9

    def key_event(self, key, action, modifiers):
        """Handle key events."""
        if not self.game_end:
            if action == self.wnd.keys.ACTION_PRESS:
                # Calculate the step size based on grid size and number of steps
                step_size = 2 * self.grid_size / 10
                if key == self.wnd.keys.UP:
                    print("UP PRESSED")
                    if self.ship_position[2] < 9:
                        self.ship_position[2] += step_size  # Move up
                    else:
                        print('CANT GO HIGHER')
                elif key == self.wnd.keys.DOWN:
                    print("DOWN PRESSED")
                    if self.ship_position[2] > 0:
                        self.ship_position[2] -= step_size  # Move down
                    else:
                        print('CANT GO LOWER')
                elif key == self.wnd.keys.LEFT:
                    print("LEFT PRESSED")
                    if self.ship_position[0] < 12:
                        self.ship_position[0] += step_size  # Move left
                    else:
                        print("CANNOT LEAVE THE BOARD ")
                elif key == self.wnd.keys.RIGHT:
                    print("RIGHT PRESSED")
                    if self.ship_position[0] > -12:
                        self.ship_position[0] -= step_size  # Move left
                    else:
                        print("CANNOT LEAVE THE BOARD ")
                elif key == self.wnd.keys.Z:
                    print("FORWARDS PRESSED")
                    if self.ship_position[1] > -12:
                        self.ship_position[1] -= step_size  # Move forward
                    else:
                        print("CANNOT LEAVE THE BOARD ")
                elif key == self.wnd.keys.X:
                    print("BACKWARDS PRESSED")
                    if self.ship_position[1] < 12:
                        self.ship_position[1] += step_size  # Move back
                    else:
                        print("CANNOT LEAVE THE BOARD ")
                print(self.ship_position)
                if key == self.wnd.keys.SPACE:
                    print("BULLET SHOT")
                    self.shoot_sound.play()
                    bullet_position = self.ship_position.copy()
                    bullet_position[1] -= 2
                    self.bullets_positions.append(np.array(bullet_position, dtype=np.float32))
                    self.bullet_list.append(self.vao_wrapper.instance(self.prog_bullet))

    def update_bullet_positions(self, step_size):
        # Update positions of all bullets in every frame
        i = 0
        while i < len(self.bullets_positions):
            bullet_position = self.bullets_positions[i]
            bullet_position[1] -= step_size

            if bullet_position[1] < -20:
                del self.bullets_positions[i]
                del self.bullet_list[i]
            else:
                self.bullets_positions[i] = np.array(bullet_position, dtype=np.float32)
                i += 1

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

        self.update_enemy_positions(frame_time)

        # Render Ship
        scale_factor = 0.1
        self.prog_ship['scale_factor'].value = scale_factor
        camera_pos = (20, 20, -20.0)

        ship_model = Matrix44.from_translation(self.ship_position).astype('f4')
        ship_mvp = (proj * lookat * ship_model).astype('f4')
        self.mvp_ship.write(ship_mvp.tobytes())

        self.light_ship.value = camera_pos
        self.vao_ship.render()

        # Render Bullet
        scale_factor = 0.1
        self.prog_bullet['scale_factor'].value = scale_factor

        self.update_bullet_positions(frame_time*30)  # Update bullet position in every frame

        for i in range(len(self.bullets_positions)):

            bullet_model = Matrix44.from_translation(self.bullets_positions[i]).astype('f4')
            bullet_mvp = (proj * lookat * bullet_model).astype('f4')
            self.mvp_bullet.write(bullet_mvp.tobytes())

            self.light_enemy.value = camera_pos
            self.bullet_list[i].render()





        # Render Enemy
        for i in reversed(range(len(self.enemies_list))):
            scale_factor = 0.12
            self.prog_enemy['scale_factor'].value = scale_factor
            camera_pos = (0, 10, 20)

            enemy_model = Matrix44.from_translation(self.enemies_position_list[i]).astype('f4')
            enemy_mvp = (proj * lookat * enemy_model).astype('f4')
            self.mvp_enemy.write(enemy_mvp.tobytes())
            camera_pos = (0, 10, 20.0)
            self.light_enemy.value = camera_pos
            self.enemies_list[i].render()

            # Check collision with the ship
            ship_box = [self.ship_position[0] - 1, self.ship_position[0] + 1,
                        self.ship_position[1] - 1, self.ship_position[1] + 1,
                        self.ship_position[2] - 1, self.ship_position[2] + 1]

            enemy_box = [self.enemies_position_list[i][0] - 1, self.enemies_position_list[i][0] + 1,
                        self.enemies_position_list[i][1] - 1, self.enemies_position_list[i][1] + 1,
                        self.enemies_position_list[i][2] - 1, self.enemies_position_list[i][2] + 1]

            for j in range(len(self.bullets_positions)):
                bullet_box = [self.bullets_positions[j][0] - 0.5, self.bullets_positions[j][0] + 0.5,
                            self.bullets_positions[j][1] - 0.5, self.bullets_positions[j][1] + 0.5,
                            self.bullets_positions[j][2] - 0.5, self.bullets_positions[j][2] + 0.5]

                if check_collision(bullet_box, enemy_box):
                    self.death_sound.play()
                    self.points += 10
                    print(f"Points: {self.points}")
                    del self.enemies_position_list[i]
                    del self.enemies_list[i]
            if check_collision(ship_box, enemy_box):
                print("Game Over: Ship collided with an enemy!")
                self.game_end = True
                self.death_sound.play()
                self.ship_position = np.array([1.3, 24, 18.5], dtype=np.float32)

                self.ship_color = random_color()
                self.prog_ship = self.ctx.program(
                    vertex_shader=vertex_shader_game_over,
                    fragment_shader=fragment_shader_game_over
                )

                self.mvp_ship = self.prog_ship['Mvp']
                self.light_ship = self.prog_ship['Light']

                
                obj = self.load_scene('gover.obj')
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
                camera_pos = (20, 20, 50.0)
                self.light_ship.value = camera_pos
                self.vao_ship.render()
        
        if len(self.enemies_list) == 0 and not self.game_end:
            self.game_won()
            

    def game_won(self):
        print("Game WON!")
        self.game_end = True
        self.death_sound.play()
        self.ship_position = np.array([1.3, 24, 18.5], dtype=np.float32)
        camera_pos = (0, 20, 20.0)
        self.light_enemy.value = camera_pos
        self.light_ship.value = camera_pos
        self.ship_color = random_color()
        self.prog_ship = self.ctx.program(
            vertex_shader=vertex_shader_game_over,
            fragment_shader=fragment_shader_game_over
        )

        self.mvp_ship = self.prog_ship['Mvp']
        self.light_ship = self.prog_ship['Light']

        obj = self.load_scene('gwon.obj')
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
        self.vao_ship.render()





def check_collision(box1, box2):
# box: [min_x, max_x, min_y, max_y, min_z, max_z]
    return not (box1[1] < box2[0] or
                box1[0] > box2[1] or
                box1[3] < box2[2] or
                box1[2] > box2[3] or
                box1[5] < box2[4] or
                box1[4] > box2[5])


if __name__ == '__main__':
    Scene.run()
