import pygame
import numpy

import OpenGL.GL as gl 
import OpenGL.GL.shaders as shaders 



pygame.init()
WHITE = (255,255,255)
render = pygame.display.set_mode((800,600), pygame.OPENGL)

vertex_shader = """
#version 330
in vec4 position;
void main() {
    gl_Position = position;
}
"""

fragment_shader = """
#version 330
void main() {
    gl_FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
}
"""

shader = shaders.compileProgram(
    shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
    shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
)

vertex_data = numpy.array([
    0.0,0.5,0.0,
    0.5,-0.5,0.0,
    -0.5,-0.5,0.0
], dtype=numpy.float32)

#vertex buffer object

vertex_buffer_object = gl.glGenBuffers(1)
gl.glBindBuffer(
    gl.GL_ARRAY_BUFFER, vertex_buffer_object
)
gl.glBufferData(gl.GL_ARRAY_BUFFER, 9 * 4, vertex_data,gl.GL_STATIC_DRAW)

#vertex array object

vertext_array_object = gl.glGenVertexArrays(1)
gl.glBindVertexArray(vertext_array_object)

#shaders
position = gl.glGetAttribLocation(shader, 'position')
gl.glEnableVertexAttribArray(position)
gl.glVertexAttribPointer(position, 3, gl.GL_FLOAT, False,0, None)


done = False
gl.glClearColor(0.5,1.0,0.5,1.0)
while not done:
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glUseProgram(shader)
    gl.glDrawArrays(gl.GL_TRIANGLES,0,3)
    
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            done = True
    pass