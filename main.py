import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

pygame.init()

WIDTH, HEIGHT = 1600, 1600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Galaxy Simulator")

WHITE = (1, 1, 1)
YELLOW = (1, 1, 0)
BLUE = (0.39, 0.58, 0.93)
RED = (0.74, 0.15, 0.2)
DARK_GREY = (0.31, 0.31, 0.32)
ORANGE = (1, 0.65, 0)
LIGHT_BLUE = (0.68, 0.85, 0.9)
LIGHT_GREY = (0.83, 0.83, 0.83)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 100 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_POLYGON)
        for i in range(360):
            angle = math.radians(i)
            glVertex2f(self.x * self.SCALE + self.radius * math.cos(angle), self.y * self.SCALE + self.radius * math.sin(angle))
        glEnd()

        if len(self.orbit) > 2:
            glBegin(GL_LINE_STRIP)
            for point in self.orbit:
                x, y = point
                glVertex2f(x * self.SCALE, y * self.SCALE)
            glEnd()

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000 

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 20, ORANGE, 1.898 * 10**27)
    jupiter.y_vel = -13.06 * 1000

    saturn = Planet(9.58 * Planet.AU, 0, 18, LIGHT_GREY, 5.683 * 10**26)
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(19.22 * Planet.AU, 0, 16, LIGHT_BLUE, 8.681 * 10**25)
    uranus.y_vel = -6.80 * 1000

    neptune = Planet(30.05 * Planet.AU, 0, 16, BLUE, 1.024 * 10**26)
    neptune.y_vel = -5.43 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    glOrtho(-WIDTH//2, WIDTH//2, -HEIGHT//2, HEIGHT//2, -1, 1)

    while run:
        clock.tick(60)
        glClear(GL_COLOR_BUFFER_BIT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw()

        pygame.display.flip()

    pygame.quit()

main()
