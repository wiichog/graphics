import pygame
from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
from vertices import *
import glm

#Crear una ventana
# #1 Inicializar ventana

pygame.init()
screen = pygame.display.set_mode((800,600),pygame.OPENGL|pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# #2 inicializar shaders

vertex_shader = """ 
#version 330
layout(location = 0) in vec4 position;
layout(location = 1) in vec4 color;
layout(location = 2) in vec4 textCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec4 vertexColor;
out vec2 vertexTextCoord;

void main(){
    gl_Position = projection * view * model * position;
    vertexColor = color;
    vertexTextCoord = textCoord;
}

"""

fragment_shader = """
#version 330

layout(location = 0) out vec4 diffuseColor;

in vec4 vertexColor;
in vec2 vertexTextCoord;

uniform sampler2D texture1;
uniform sampler2D texture2;

void main(){
    diffuseColor = vertexColor * texture(texture1,vertexTextCoord) * mix(texture(texture1,vertexTextCoord),texture(texture2,vertexTextCoord),0.9)

}
"""

# #3 vertex Data
shader = shaders.compileProgram(
    shaders.compileShader(vertex_shader,GL_VERTEX_SHADER),
    shaders.compileShader(fragment_shader,GL_FRAGMENT_SHADER),
    )

vertex_data = vertices.data 
vertex_buffer_object = glGenVertexArrays(1)
glBindBuffer(GL_ARRAY_BUFFER,vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER,vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

glVertexAttribPointer(0,3,GL_FLOAT, False, 8*4)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0,3,GL_FLOAT, False, 8*4,ctypes.c_void_p(3*4))
glEnableVertexAttribArray(1)
glVertexAttribPointer(0,3,GL_FLOAT, False, 8*4,ctypes.c_void_p(6*4))
glEnableVertexAttribArray(2)

# #4 Texturas

glEnable(GL_TEXTURE_2D)
texture_surface = pygame.image.load('./texture.png')
texture_data = pygame.image.tostring(texture_surface,"RGB",1)
width = texture_surface.get_width()
height = texture_surface.get_height()

texture1 = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D,texture1)
glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,width,height,0,GL_RGB,GL_UNSIGNED_BYTE,texture_data)
glGenerateMipmap(GL_TEXTURE_2D)


glEnable(GL_TEXTURE_2D)
texture_surface = pygame.image.load('./meme.png')
texture_data = pygame.image.tostring(texture_surface,"RGB",1)
width = texture_surface.get_width()
height = texture_surface.get_height()

texture2 = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D,texture2)
glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,width,height,0,GL_RGB,GL_UNSIGNED_BYTE,texture_data)
glGenerateMipmap(GL_TEXTURE_2D)

glUseProgram(shader)
glUniform1i(glGetUniformLocation(shader,"texture1"),0)
glUniform1i(glGetUniformLocation(shader,"texture2"),1)

# #5 matrixes
i = glm.mat4(1)
model = glm.rotate(i,glm.radians(-55.0),glm.vec3(1.0,0,0))
view = glm.translate(i,glm.vec3(0.0,0.0,-3.0))
projection = glm.perspective(glm.radians(45),800/600,0.1,100.0)

glClearColor(0.5,1.0,0.5,1.0)
glEnable(GL_DEPTH_TEST)
def process_input():
    for event in pygame.event.get():
        if event.type == pygame.event.QUIT():
            return True
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            return True
    return False

done = False

while not done:
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D,texture1)
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D,texture2)

    model = glm.rotate(model, glm.radians(1),glm.vec3(0.0,0.0,1.0))

    glUniformMatrix4fv(glGetUniformLocation(shader,"model"), 1, GL_FALSE,glm.value_ptr(model))
    glUniformMatrix4fv(glGetUniformLocation(shader,"view"), 1, GL_FALSE,glm.value_ptr(view))
    glUniformMatrix4fv(glGetUniformLocation(shader,"projection"), 1, GL_FALSE,glm.value_ptr(projection))

    glDrawArrays(GL_TRIANGLES,0,36)
    done = process_input()
    clock.tick(15)
    pygame.display.flip()