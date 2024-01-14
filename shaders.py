vertex_shader_bullet='''
    #version 330
    uniform mat4 Mvp;
    uniform float scale_factor;

    in vec3 in_position;
    in vec3 in_normal;
    in vec3 in_color;
    in vec3 in_origin;
    in mat3 in_basis;

    out vec3 v_vert;
    out vec3 v_norm;
    out vec3 v_color;

    void main() {
        // Transform position using origin, basis, and scale_factor
        v_vert = in_origin + in_basis * (in_position * scale_factor);
        
        // Rotate the position 180 degrees around the x-axis to turn it upside down
        mat3 flip_matrix = mat3(
            -1.0, 0.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, 0.0, -1.0
        );
        v_vert = flip_matrix * v_vert;

        // Transform normal using basis
        v_norm = in_basis * in_normal;
        
        // Pass color through
        v_color = in_color;
        
        gl_Position = Mvp * vec4(v_vert, 1.0);
    }
'''

fragment_shader_bullet='''
    #version 330
    uniform vec3 Light;
    in vec3 v_vert;
    in vec3 v_norm;
    in vec3 v_color;
    out vec4 fragColor;
    void main() {
        float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
        fragColor = vec4(v_color * lum, 1.0);
    }
'''

vertex_shader_enemy='''
    #version 330
    uniform mat4 Mvp;
    uniform float scale_factor;

    in vec3 in_position;
    in vec3 in_normal;
    in vec3 in_color;
    in vec3 in_origin;
    in mat3 in_basis;

    out vec3 v_vert;
    out vec3 v_norm;
    out vec3 v_color;

    void main() {
        // Transform position using origin, basis, and scale_factor
        v_vert = in_origin + in_basis * (in_position * scale_factor);
        
        // Rotate the position 180 degrees around the x-axis to turn it upside down
        mat3 flip_matrix = mat3(
            -1.0, 0.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, 0.0, -1.0
        );
        v_vert = flip_matrix * v_vert;

        // Transform normal using basis
        v_norm = in_basis * in_normal;
        
        // Pass color through
        v_color = in_color;
        
        gl_Position = Mvp * vec4(v_vert, 1.0);
    }
'''

fragment_shader_enemy='''
    #version 330
    uniform vec3 Light;
    in vec3 v_vert;
    in vec3 v_norm;
    in vec3 v_color;
    out vec4 fragColor;
    void main() {
        float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
        fragColor = vec4(v_color * lum, 1.0);
    }
'''


vertex_shader_grid='''
    #version 330
    uniform mat4 Mvp;
    in vec3 in_vert;
    void main() {
        gl_Position = Mvp * vec4(in_vert, 1.0);
    }
'''
fragment_shader_grid='''
    #version 330
    out vec4 fragColor;
    uniform vec2 u_resolution;

    void main() {
        vec2 st = gl_FragCoord.xy / u_resolution;
        float stars = step(0.98, fract(sin(dot(st, vec2(12.9898, 78.233))) * 43758.5453));
        fragColor = vec4(vec3(stars), 1.0);
    }
'''

vertex_shader_enemy = '''
    #version 330
    uniform mat4 Mvp;
    uniform float scale_factor;

    in vec3 in_position;
    in vec3 in_normal;
    in vec3 in_color;
    in vec3 in_origin;
    in mat3 in_basis;

    out vec3 v_vert;
    out vec3 v_norm;
    out vec3 v_color;

    void main() {
        // Transform position using origin, basis, and scale_factor
        v_vert = in_origin + in_basis * (in_position * scale_factor);

        // Rotate the position 270 degrees around the x-axis to turn it upside down
        mat3 flip_matrix = mat3(
            1.0, 0.0, 0.0,
            0.0, cos(radians(270.0)), -sin(radians(270.0)),
            0.0, sin(radians(270.0)), cos(radians(270.0))
        );
        v_vert = flip_matrix * v_vert;

        // Transform normal using basis
        v_norm = in_basis * in_normal;

        // Pass color through
        v_color = in_color;

        gl_Position = Mvp * vec4(v_vert, 1.0);
    }
'''

fragment_shader_enemy='''
    #version 330
    uniform vec3 Light;
    in vec3 v_vert;
    in vec3 v_norm;
    in vec3 v_color;
    out vec4 fragColor;
    void main() {
        float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
        fragColor = vec4(v_color * lum, 1.0);
    }
'''