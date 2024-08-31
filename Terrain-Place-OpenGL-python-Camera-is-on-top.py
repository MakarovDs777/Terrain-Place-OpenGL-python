import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Инициализация Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Инициализация камеры
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -30)
glRotatef(90, 1, 0, 0)  # Повернуть камеру на 90 градусов вокруг оси X

# Генерация шума
def generate_noise_2d(shape, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0):
    import noise
    noise_map = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            noise_map[i][j] = noise.pnoise2(i/scale, j/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=42)
    return noise_map

# Создание террейна
def create_terrain(width, height):
    noise_map = generate_noise_2d((width, height))
    vertices = []
    for i in range(width):
        for j in range(height):
            x = i - width // 2
            z = j - height // 2
            y = noise_map[i][j] * 10
            vertices.append((x, y, z))
    return vertices

# Отрисовка террейна
def draw_terrain(vertices, width, height):
    glBegin(GL_LINES)
    for i in range(width):
        for j in range(height):
            if i < width - 1:
                glVertex3fv(vertices[i * height + j])
                glVertex3fv(vertices[(i + 1) * height + j])
            if j < height - 1:
                glVertex3fv(vertices[i * height + j])
                glVertex3fv(vertices[i * height + j + 1])
    glEnd()

# Основной цикл
width, height = 100, 100
vertices = create_terrain(width, height)
x_move = 0
z_move = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                z_move += 0.1
            if event.key == pygame.K_s:
                z_move -= 0.1
            if event.key == pygame.K_a:
                x_move -= 0.1
            if event.key == pygame.K_d:
                x_move += 0.1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glTranslatef(x_move, 0, z_move)
    x_move = 0
    z_move = 0
    draw_terrain(vertices, width, height)
    pygame.display.flip()
    pygame.time.wait(10)
