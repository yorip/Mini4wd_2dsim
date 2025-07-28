import pygame
import math

class Mini4WD:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.angle = 0
        self.speed = 0

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
car = Mini4WD()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    car.update()
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (int(car.x), int(car.y)), 10)
    pygame.display.flip()
    clock.tick(60)

