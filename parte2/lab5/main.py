import pygame
from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import glm
import pyassimp
import numpy

pygame.init()
pygame.display.set_mode((800,600), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.key.set_repeat(1,10)

glClearColor(0.18,0.18,0.18,1.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)

vertex_shader = """
#version 330
layout (location = 0) in vec4 position;
layout (location = 1) in vec4 normal;
layout (location = 2) in vec2 texcoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec4 color;
uniform vec4 light;

out vec4 vertexColor;
out vec2 vertexTexcoords;

void main(){

    float intensity = dot(normal, normalize(light - position));
    gl_Position = projection * view * model * position;
    vertexColor = color * intensity;
    vertexTexcoords = texcoords;

}
"""

fragment_shader = """
#version 330

layout (location = 0) out vec4 diffuseColor;

in vec4 vertexColor;
in vec2 vertexTexcoords;

uniform sampler2D tex;

void main(){

    diffuseColor = vertexColor * texture(tex, vertexTexcoords);

}
"""

shader = shaders.compileProgram(
    shaders.compileShader(vertex_shader,GL_VERTEX_SHADER),
    shaders.compileShader(fragment_shader,GL_FRAGMENT_SHADER),
    )


glUseProgram(shader)

model = glm.mat4(1)
view = glm.mat4(1)

projection = glm.perspective(glm.radians(45),800/600,0.1,1000.0)
scene = pyassimp.load('./models/fox.obj')

def glize(node):
    model = node.transformation.astype(numpy.float32)
    model = glm.translate(glm.mat4(model.tolist()),glm.vec3(0,-50,0))
    for mesh in node.meshes:
        material = dict(mesh.material.properties.items())
        texture = material['file'][2:]
        texture_surface = pygame.image.load('./models/'+texture)
        texture_Data = pygame.image.tostring(texture_surface,"RGB",1)
        width = texture_surface.get_width()
        height = texture_surface.get_height()
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,texture)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,width,height,0,GL_RGB,GL_UNSIGNED_BYTE,texture_Data)
        glGenerateMipmap(GL_TEXTURE_2D)

        vertex_Data = numpy.hstack((
            numpy.array(mesh.vertices, dtype=numpy.float32),
            numpy.array(mesh.normals, dtype=numpy.float32),
            numpy.array(mesh.texturecoords[0], dtype=numpy.float32),
        ))

        faces = numpy.hstack(
            numpy.array(mesh.faces, dtype=numpy.int32)
        )

        vertex_buffer_object = glGenVertexArrays(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
        glBufferData(GL_ARRAY_BUFFER,vertex_Data.nbytes,vertex_Data,GL_STATIC_DRAW)
        glVertexAttribPointer(0,3,GL_FLOAT,False,9*4, None)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1,2,GL_FLOAT,False,9*4,ctypes.c_void_p(3*4))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2,3,GL_FLOAT,False,9*4,ctypes.c_void_p(6*4))
        glEnableVertexAttribArray(2)

        element_buffer_object = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,element_buffer_object)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)

        glUniformMatrix4fv(
            glGetUniformLocation(shader, "model") ,1, GL_FALSE, glm.value_ptr(model)
        )

        glUniformMatrix4fv(
            glGetUniformLocation(shader,"view") ,1,GL_FALSE, glm.value_ptr(view)
        )

        glUniformMatrix4fv(
            glGetUniformLocation(shader, "projection") ,1, GL_FALSE, glm.value_ptr(projection)
        )

        diffuse = mesh.material.properties["diffuse"]

        glUniform4f(
            glGetUniformLocation(shader, "color"), *diffuse,1
        )

        glUniform4f(
            glGetUniformLocation(shader, "light"), -100,300,0,1
        )

        glDrawElements(GL_TRIANGLES, len(faces), GL_UNSIGNED_INT, None)
    
    for child in node.children:
        glize(child)

camera = glm.vec3(0,0,200)
camera_speed = 50

def process_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            return True
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_LEFT:
                camera.x += camera_speed
                camera.z += camera_speed
            if event.key == pygame.K_RIGHT:
                camera.x -= camera_speed
                camera.z -= camera_speed

done = False
while not done:
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    view = glm.lookAt(camera, glm.vec3(0,0,0), glm.vec3(0,1,0))
    glize(scene.rootnode)

    done = process_input()
    clock.tick(15)
    pygame.display.flip()
