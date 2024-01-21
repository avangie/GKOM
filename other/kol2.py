import moderngl_window as mglw
import moderngl
import numpy as np

class Scene(mglw.WindowConfig):
    title = "Combined Objects"
    gl_version = (3, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.transformation_matrix = self.get_transformation_matrix()
        self.shadow_matrix = self.get_shadow_matrix()  # Replace with your shadow matrix calculation

        # Define cube vertices
        vertices = np.array([
            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, 1.0, -1.0,
            -1.0, 1.0, -1.0,
            -1.0, -1.0, 1.0,
            1.0, -1.0, 1.0,
            1.0, 1.0, 1.0,
            -1.0, 1.0, 1.0,
        ], dtype='f4')

        # Define cube indices
        indices = np.array([
            0, 1, 2, 2, 3, 0,
            4, 5, 6, 6, 7, 4,
            0, 3, 7, 7, 4, 0,
            1, 2, 6, 6, 5, 1,
            2, 3, 7, 7, 6, 2,
            0, 1, 5, 5, 4, 0
        ], dtype='u4')

        self.buffer = self.ctx.buffer(vertices)
        self.index_buffer = self.ctx.buffer(indices)
         # Create the shader program
        self.program = self.ctx.program(
            vertex_shader="""
            #version 330

            uniform mat4 model;

            in vec3 in_vert;

            void main() {
                gl_Position = model * vec4(in_vert, 1.0);
            }
            """,
            fragment_shader="""
            #version 330

            out vec4 fragColor;

            void main() {
                fragColor = vec4(1.0, 1.0, 1.0, 1.0);
            }
            """
        )

        self.vao = self.ctx.simple_vertex_array(self.program, self.buffer, self.index_buffer, 'in_vert')

    def get_transformation_matrix(self):
        # Example transformation matrix for translation, rotation, and scaling
        translation = np.array([
            [1.0, 0.0, 0.0, 2.0],  # Translate along the X-axis by 2 units
            [0.0, 1.0, 0.0, 3.0],  # Translate along the Y-axis by 3 units
            [0.0, 0.0, 1.0, 1.0],  # Translate along the Z-axis by 1 unit
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)

        rotation = np.array([
            [0.866, -0.5, 0.0, 0.0],  # Rotate around the X-axis
            [0.5, 0.866, 0.0, 0.0],   # Rotate around the Y-axis
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)

        scaling = np.array([
            [2.0, 0.0, 0.0, 0.0],  # Scale along the X-axis by a factor of 2
            [0.0, 3.0, 0.0, 0.0],  # Scale along the Y-axis by a factor of 3
            [0.0, 0.0, 1.0, 0.0],  
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)

        # Combine translation, rotation, and scaling into a single transformation matrix
        return np.dot(translation, np.dot(rotation, scaling))


    def get_shadow_matrix(self):
        # Replace these values with your actual light position, look_at, and up_direction
        light_position = np.array([5.0, 5.0, 5.0])
        look_at = np.array([0.0, 0.0, 0.0])
        up_direction = np.array([0.0, 1.0, 0.0])

        # Calculate the light's view matrix manually
        forward = look_at - light_position
        forward /= np.linalg.norm(forward)

        right = np.cross(up_direction, forward)
        right /= np.linalg.norm(right)

        up = np.cross(forward, right)
        up /= np.linalg.norm(up)

        view_matrix = np.eye(4)
        view_matrix[0:3, 0] = right
        view_matrix[0:3, 1] = up
        view_matrix[0:3, 2] = -forward
        view_matrix[0:3, 3] = light_position

        # Calculate the bounding box of your scene or adjust it based on your needs
        scene_min = np.array([-1.0, -1.0, -1.0])
        scene_max = np.array([1.0, 1.0, 1.0])

        # Create an orthographic projection matrix manually
        ortho_matrix = np.diag([2.0 / (scene_max[0] - scene_min[0]),
                                2.0 / (scene_max[1] - scene_min[1]),
                                -2.0 / (scene_max[2] - scene_min[2]),
                                1.0])
        ortho_matrix[3, 0] = -(scene_max[0] + scene_min[0]) / (scene_max[0] - scene_min[0])
        ortho_matrix[3, 1] = -(scene_max[1] + scene_min[1]) / (scene_max[1] - scene_min[1])
        ortho_matrix[3, 2] = -(scene_max[2] + scene_min[2]) / (scene_max[2] - scene_min[2])

        # Calculate the shadow matrix (light's view matrix * orthographic projection matrix)
        shadow_matrix = np.dot(view_matrix, ortho_matrix)

        return shadow_matrix

    def multiply_transform_and_shadow_matrices(self, transformation_matrix, shadow_matrix):
        # Perform matrix multiplication of transformation and shadow matrices
        return np.dot(transformation_matrix, shadow_matrix)

    def render(self, time, frame_time):
        # Call the matrix multiplication function
        combined_matrix = self.multiply_transform_and_shadow_matrices(
            self.transformation_matrix, self.shadow_matrix
        )

        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Use the combined_matrix in the shader
        self.program['model'].write(combined_matrix)
        
        # Render the cube
        self.vao.render(moderngl.TRIANGLES, index_buffer=self.index_buffer)

if __name__ == '__main__':
    Scene.run()
