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


# vertex_shader_ship
vertex_shader_ship = '''
    #version 330
    uniform mat4 Mvp;
    uniform float scale_factor;

    in vec3 in_position;
    in vec3 in_normal;
    in vec3 in_color;
    in vec3 in_origin;
    in mat3 in_basis;

    out vec3 FragPos;
    out vec3 Normal;
    out vec3 Color;

    void main() {
        vec3 worldPos = in_origin + in_basis * (in_position * scale_factor);

        worldPos.z = -worldPos.z;

        FragPos = vec3(Mvp * vec4(worldPos, 1.0));
        Normal = normalize(in_basis * in_normal);
        Color = in_color;

        gl_Position = Mvp * vec4(worldPos, 1.0);
    }
'''

# fragment_shader_ship
fragment_shader_ship = '''
    #version 330
    uniform vec3 lightPos;
    uniform vec3 viewPos;
    uniform float lightIntensity;


    in vec3 FragPos;
    in vec3 Normal;
    in vec3 Color;

    out vec4 fragColor;

    void main() {
        // Flip the Y component
        vec3 flippedFragPos = FragPos;
        flippedFragPos.y = -flippedFragPos.y;


        // Ambient
        float ambientStrength = 0.1;
        vec3 ambient = ambientStrength * Color;

        // Diffuse
        vec3 lightDir = normalize(lightPos - FragPos);
        float diff = max(dot(Normal, lightDir), 0.0);
        vec3 diffuse = diff * Color;

        // Specular
        float specularStrength = 0.5;
        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-lightDir, Normal);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
        vec3 specular = specularStrength * spec * vec3(1.0, 1.0, 1.0);

        vec3 result = ambient + diffuse + specular;
        fragColor = vec4(result * lightIntensity, 1.0);
    }
'''

# vertex_shader_enemy
vertex_shader_enemy = '''
    #version 330
    uniform mat4 Mvp;
    uniform float scale_factor;


    in vec3 in_position;
    in vec3 in_normal;
    in vec3 in_color;
    in vec3 in_origin;
    in mat3 in_basis;

    out vec3 FragPos;
    out vec3 Normal;
    out vec3 Color;

    void main() {
        vec3 worldPos = in_origin + in_basis * (in_position * scale_factor);

        // Rotate the Y component to fix upside-down rendering
        worldPos.y = -worldPos.y;

        // Rotate the X component using transformation matrix
        mat3 flip_matrix1 = mat3(
            1.0, 0.0, 0.0,
            0.0, cos(radians(90.0)), -sin(radians(90.0)),
            0.0, sin(radians(90.0)), cos(radians(90.0))
        );

        // Rotate
        worldPos = flip_matrix1 * worldPos;

        FragPos = vec3(Mvp * vec4(worldPos, 1.0));
        Normal = normalize(in_basis * in_normal);
        Color = in_color;

        gl_Position = Mvp * vec4(worldPos, 1.0);
    }

'''

# fragment_shader_enemy
fragment_shader_enemy = '''
    #version 330
    uniform vec3 lightPos;
    uniform vec3 viewPos;
    uniform float lightIntensity;



    in vec3 FragPos;
    in vec3 Normal;
    in vec3 Color;

    out vec4 fragColor;

    void main() {
        // Ambient
        float ambientStrength = 0.1;
        vec3 ambient = ambientStrength * Color;

        // Diffuse
        vec3 lightDir = normalize(lightPos - FragPos);
        float diff = max(dot(Normal, lightDir), 0.0);
        vec3 diffuse = diff * Color;

        // Specular
        float specularStrength = 0.5;
        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-lightDir, Normal);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
        vec3 specular = specularStrength * spec * vec3(1.0, 1.0, 1.0);

        vec3 result = ambient + diffuse + specular;
        fragColor = vec4(result * lightIntensity, 1.0);
    }
'''

# vertex_shader_bullet
vertex_shader_bullet = '''
    #version 330
    uniform mat4 Mvp;
    uniform float scale_factor;

    in vec3 in_position;
    in vec3 in_normal;
    in vec3 in_color;
    in vec3 in_origin;
    in mat3 in_basis;

    out vec3 FragPos;
    out vec3 Normal;
    out vec3 Color;

    void main() {
        vec3 worldPos = in_origin + in_basis * (in_position * scale_factor);

        // Rotate the Y component to fix upside-down rendering
        mat3 flip_matrix = mat3(
            1.0, 0.0, 0.0,
            0.0, cos(radians(180.0)), -sin(radians(180.0)),
            0.0, sin(radians(180.0)), cos(radians(180.0))
        );
        worldPos = flip_matrix * worldPos;

        FragPos = vec3(Mvp * vec4(worldPos, 1.0));
        Normal = normalize(in_basis * in_normal);
        Color = in_color;

        gl_Position = Mvp * vec4(worldPos, 1.0);
    }
'''

# fragment_shader_bullet
fragment_shader_bullet = '''
    #version 330
    uniform vec3 lightPos;
    uniform vec3 viewPos;
    uniform float lightIntensity;


    in vec3 FragPos;
    in vec3 Normal;
    in vec3 Color;

    out vec4 fragColor;

    void main() {
        // Ambient
        float ambientStrength = 0.1;
        vec3 ambient = ambientStrength * Color;

        // Diffuse
        vec3 lightDir = normalize(lightPos - FragPos);
        float diff = max(dot(Normal, lightDir), 0.0);
        vec3 diffuse = diff * Color;

        // Specular
        float specularStrength = 0.5;
        vec3 viewDir = normalize(viewPos - FragPos);
        vec3 reflectDir = reflect(-lightDir, Normal);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
        vec3 specular = specularStrength * spec * vec3(1.0, 1.0, 1.0);

        vec3 result = ambient + diffuse + specular;
        fragColor = vec4(result * lightIntensity, 1.0);
    }
'''
