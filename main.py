import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

textures = {}
LightAmb = (0.7, 0.7, 0.7)
LightDif = (1.0, 1.0, 0.0)
LightPos = (4.0, 4.0, 6.0, 1.0)
earth_rot = 0.0
moon_rot = 0.0
year = 0
day = 0

def DrawGLScene(x, y):
    global earth_rot, moon_rot, year, day
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glRotatef(x, 1, 0, 0)
    glRotatef(y, 0, 1, 0)
    glTranslatef(0, 0, -10)

    glPushMatrix()
    drawSun()

    glRotatef(year, 0, 1, 0)
    year = (year + 1) % 360

    glPushMatrix()
    drawEarthAndMoon(earth_rot, moon_rot)
    glPopMatrix()

    glPopMatrix()

    earth_rot = (earth_rot + 1) % 360
    moon_rot = (moon_rot + 13) % 360

def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height = 1
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def LoadTextures(fname):
    if textures.get(fname) is not None:
        return textures.get(fname)
    texture = textures[fname] = glGenTextures(1)
    image = Image.open(fname)
    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBX", 0, -1)

    glBindTexture(GL_TEXTURE_2D, texture)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    return texture

def InitGL(Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glClearStencil(0)
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_TEXTURE_2D)

    glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDif)
    glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def drawSun():
    global Q
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/sun.tga"))

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GLU_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    gluSphere(Q, 0.7, 32, 16)

    glColor4f(1, 1, 1, 0.4)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    gluSphere(Q, 0.7, 32, 16)

    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_BLEND)
    gluDeleteQuadric(Q)

def drawEarthAndMoon(earth_rot, moon_rot):
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/earthmap.bmp"))

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GLU_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glRotatef(earth_rot, 0, 1, 0)
    glTranslatef(2, 0, 0)
    gluSphere(Q, 0.4, 32, 16)

    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/2k_moon.jpg"))

    glRotatef(moon_rot, 0, 1, 0)
    glTranslatef(0.6, 0, 0)
    gluSphere(Q, 0.1, 32, 16)

    gluDeleteQuadric(Q)
    glPopMatrix()

def main():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)
    pg.display.set_caption("Solar System Simulation")
    InitGL(*display)
    x = y = 0
    while True:
        pg.time.Clock().tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    x += 2
                if event.key == pg.K_RIGHT:
                    x -= 2
                if event.key == pg.K_UP:
                    y += 2
                if event.key == pg.K_DOWN:
                    y -= 2
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

        DrawGLScene(x, y)
        pg.display.flip()
        pg.time.wait(10)

main()
