import math
import numpy
import pygame
import random
import ctypes
import glm

import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders


# initialize pygame

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.OPENGL|pygame.DOUBLEBUF)
clock = pygame.time.Clock()


# initialize shaders

vertex_shader = """
#version 330
layout (location = 0) in vec4 position;
layout (location = 1) in vec4 color;
layout (location = 2) in vec2 texCoord;

out vec4 vertexColor;
out vec2 vertexTexCoord;

void main()
{
   gl_Position = position;
   vertexColor = color;
   vertexTexCoord = texCoord;
}
"""

fragment_shader = """
#version 330
layout(location = 0) out vec4 secColor;

in vec4 vertexColor;
in vec2 vertexTexCoord;
uniform sampler2D ourTexture;

void main()
{
   secColor = vertexColor * texture(ourTexture, vertexTexCoord);
}
"""

shader = shaders.compileProgram(
    shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
    shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
)


# initialize vertex data

vertex_data = numpy.array([
     0.5,  0.5, 0,   1, 0, 0,    1, 1,
     0.5, -0.5, 0,   0, 1, 0,    1, 0,
    -0.5, -0.5, 0,   0, 0, 1,    0, 0,
    -0.5,  0.5, 0,   1, 1, 0,    0, 1  
], dtype=numpy.float32)

index_data = numpy.array([
    0, 1, 3, 
    1, 2, 3
], dtype=numpy.uint32)

vertex_array_object = gl.glGenVertexArrays(1)
gl.glBindVertexArray(vertex_array_object)

vertex_buffer_object = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer_object)
gl.glBufferData(gl.GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, gl.GL_STATIC_DRAW)

element_buffer_object = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, gl.GL_STATIC_DRAW)

gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, 8 * 4, ctypes.c_void_p(0))
gl.glEnableVertexAttribArray(0)
gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, 8 * 4, ctypes.c_void_p(3 * 4))
gl.glEnableVertexAttribArray(1)
gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, False, 8 * 4, ctypes.c_void_p(6 * 4))
gl.glEnableVertexAttribArray(2);
    

# initialize texture data

texture_surface = pygame.image.load('./texture.png')
texture_data = pygame.image.tostring(texture_surface,"RGBA",1)
width = texture_surface.get_width()
height = texture_surface.get_height()

gl.glEnable(gl.GL_TEXTURE_2D)
texture = gl.glGenTextures(1)
gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, texture_data)
gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

gl.glClearColor(0.5, 1.0, 0.5, 1.0)



def process_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            return True
    return False


done = False
while not done:
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glUseProgram(shader)

    gl.glBindVertexArray(vertex_array_object)
    gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None)
    gl.glBindVertexArray(0)

    done = process_input()
    clock.tick(15)
    pygame.display.flip()

