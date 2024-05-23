import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import math

textures = {}
LightAmb=(0.7,0.7,0.7)  
LightDif=(1.0,1.0,0.0)  
LightPos=(4.0,4.0,6.0,1.0)
sun_rot = 0.0
earth_rot = 0.0
earth_orbit = 0.0
moon_rot = 0.0
moon_orbit = 0.0
mercury_rot = 0.0
venus_rot = 0.0
mars_rot = 0.0
jupiter_rot = 0.0
saturn_rot = 0.0
uranus_rot = 0.0
neptune_rot = 0.0
pluto_rot = 0.0
year = 0
day = 0 
focus_object = None
camera_distance = 10

'''
The distance and size of the planets might need to be change for more accurate representation
'''
def DrawGLScene(x,y, zoom):
    global earth_rot, moon_rot, earth_orbit, moon_orbit, sun_rot, camera_distance, focus_object, mercury_rot, venus_rot, mars_rot, jupiter_rot, saturn_rot, uranus_rot, neptune_rot, pluto_rot, year
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(x, 1, 0, 0)
    glRotatef(y, 0, 1, 0)

    glDisable(GL_DEPTH_TEST)
    drawSkyBox(50)
    glEnable(GL_DEPTH_TEST)

    glTranslatef(0, 0, -10)

    glPushMatrix()

    '''
    To change position of the camera, change the first 3 parameters of gluLookAt
    '''
    gluLookAt(0, zoom, zoom,  
                0, 0, 0,    
                0, 1, 0) 

    #the sun
    glPushMatrix()
    drawSun()
    glRotatef(year, 0, 1, 0)
    year = (year + 1) % 360
    glPopMatrix()

    #Mercury
    glPushMatrix()
    draw_orbit(4)
    drawPlanet(0.2, 4, mercury_rot, "./TexImg/mercurymap.bmp")
    glPopMatrix()

    #Venus
    glPushMatrix()
    draw_orbit(8)
    drawPlanet(0.3, 8, venus_rot, "./TexImg/venusmap.bmp")
    glPopMatrix()

    #Earth
    glPushMatrix()
    draw_orbit(12)
    drawEarthAndMoon(earth_rot, moon_rot)
    glPopMatrix()

    #Mars
    glPushMatrix()
    draw_orbit(16)
    drawPlanet(0.5, 16, mars_rot, "./TexImg/marsmap.bmp")
    glPopMatrix()
    
    #Jupiter
    glPushMatrix()
    draw_orbit(20)
    drawPlanet(0.6, 20, jupiter_rot, "./TexImg/jupitermap.bmp")
    glPopMatrix()

    #saturn
    glPushMatrix()
    draw_orbit(24)
    drawPlanet(0.7, 24, saturn_rot, "./TexImg/saturnmap.bmp")
    glPopMatrix()

    #uranus
    glPushMatrix()
    draw_orbit(30)
    drawPlanet(0.8, 30, uranus_rot, "./TexImg/uranusmap.bmp")
    glPopMatrix()

    #neptune
    glPushMatrix()
    draw_orbit(34)
    drawPlanet(0.9, 34, neptune_rot, "./TexImg/neptunemap.bmp")
    glPopMatrix()

    #pluto
    glPushMatrix()
    draw_orbit(40)
    drawPlanet (0.25, 40, pluto_rot, "./TexImg/Pluto_Made.jpg")
    glPopMatrix()

    glPopMatrix() 

    earth_rot = (earth_rot + 1) % 360
    moon_rot = (moon_rot + 13) % 360
    mercury_rot = (mercury_rot + 4.1) % 360
    venus_rot = (venus_rot + 1.6) % 360
    mars_rot = (mars_rot + 0.5) % 360
    jupiter_rot = (jupiter_rot + 0.4) % 360
    saturn_rot = (saturn_rot + 0.3) % 360
    uranus_rot = (uranus_rot + 0.2) % 360
    neptune_rot = (neptune_rot + 0.1) % 360
    pluto_rot = (pluto_rot + 0.04) % 360

def ReSizeGLScene(Width, Height):
    if Height == 0:                        
        Height = 1

    glViewport(0, 0, Width, Height)        
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def LoadTextures(fname):
    if textures.get( fname ) is not None:
        return textures.get( fname )
    texture = textures[fname] = glGenTextures(1)
    image = Image.open(fname)

    ix = image.size[0]
    iy = image.size[1]
    image = image.tobytes("raw", "RGBX", 0, -1)
       
    glBindTexture(GL_TEXTURE_2D, texture)   
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
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
    glLoadIdentity()                    # Reset The Projection Matrix

                                                    # Calculate The Aspect Ratio Of The Window
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

    gluSphere(Q, 1.1, 32, 16)

    glColor4f(1, 1, 1, 0.4)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    gluSphere(Q, 1.1, 32, 16)

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
    glTranslatef(12, 0, 0)
    gluSphere(Q, 0.4, 32, 16)

    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/2k_moon.jpg"))

    draw_orbit(0.6)

    glRotatef(moon_rot, 0, 1, 0)
    glTranslatef(0.6, 0, 0)
    gluSphere(Q, 0.1, 32, 16)

    gluDeleteQuadric(Q)
    glPopMatrix()

'''
radius: 0 < radius < 1
distance_to_sun: distance from the sun following the x-axis
'''
def drawPlanet(radius, distance_to_sun, planet_rot, texture):
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, LoadTextures(texture))

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GLU_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glRotatef(planet_rot, 0, 1, 0)
    glTranslatef(distance_to_sun, 0, 0)
    gluSphere(Q, radius, 32, 16)

    gluDeleteQuadric(Q)
    glPopMatrix()

def draw_orbit(distance):
    num_segments = 100  # Số lượng đoạn dùng để vẽ đường tròn
    angle_step = 2.0 * math.pi / num_segments  # Góc giữa mỗi đoạn

    glColor3f(1, 1, 1)  # Màu của quỹ đạo
    glBegin(GL_LINE_LOOP)

    for i in range(num_segments):
        angle = i * angle_step
        glVertex3f(distance * math.cos(angle), 0, distance * math.sin(angle))

    glEnd()

def pickPlanet(x, y):
    glSelectBuffer(512)
    glRenderMode(GL_SELECT)
    glInitNames()
    glPushName(0)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    viewport = glGetIntegerv(GL_VIEWPORT)
    gluPickMatrix(x, viewport[3] - y, 5, 5, viewport)
    gluPerspective(45.0, float(viewport[2])/float(viewport[3]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    DrawGLScene(0, 0, 1)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    hits = glRenderMode(GL_RENDER)

    if hits:
        return hits[0][2][0]
    return None

def drawSkyBox(size):
    textures = LoadTextures("./TexImg/stars.bmp")

    glBindTexture(GL_TEXTURE_2D, textures)
    glBegin(GL_QUADS)

    # Front Face
    glTexCoord2f(0, 0); glVertex3f(-size / 2, -size / 2, -size / 2)
    glTexCoord2f(1, 0); glVertex3f( size / 2, -size / 2, -size / 2)
    glTexCoord2f(1, 1); glVertex3f( size / 2,  size / 2, -size / 2)
    glTexCoord2f(0, 1); glVertex3f(-size / 2,  size / 2, -size / 2)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures)
    glBegin(GL_QUADS)

    # Back Face
    glTexCoord2f(0, 0); glVertex3f(-size / 2, -size / 2,  size / 2)
    glTexCoord2f(1, 0); glVertex3f( size / 2, -size / 2,  size / 2)
    glTexCoord2f(1, 1); glVertex3f( size / 2,  size / 2,  size / 2)
    glTexCoord2f(0, 1); glVertex3f(-size / 2,  size / 2,  size / 2)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures)
    glBegin(GL_QUADS)

    # Top Face
    glTexCoord2f(0, 0); glVertex3f(-size / 2,  size / 2, -size / 2)
    glTexCoord2f(1, 0); glVertex3f( size / 2,  size / 2, -size / 2)
    glTexCoord2f(1, 1); glVertex3f( size / 2,  size / 2,  size / 2)
    glTexCoord2f(0, 1); glVertex3f(-size / 2,  size / 2,  size / 2)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures)
    glBegin(GL_QUADS)

    # Bottom Face
    glTexCoord2f(0, 0); glVertex3f(-size / 2, -size / 2, -size / 2)
    glTexCoord2f(1, 0); glVertex3f( size / 2, -size / 2, -size / 2)
    glTexCoord2f(1, 1); glVertex3f( size / 2, -size / 2,  size / 2)
    glTexCoord2f(0, 1); glVertex3f(-size / 2, -size / 2,  size / 2)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures)
    glBegin(GL_QUADS)

    # Right face
    glTexCoord2f(0, 0); glVertex3f( size / 2, -size / 2, -size / 2)
    glTexCoord2f(1, 0); glVertex3f( size / 2,  size / 2, -size / 2)
    glTexCoord2f(1, 1); glVertex3f( size / 2,  size / 2,  size / 2)
    glTexCoord2f(0, 1); glVertex3f( size / 2, -size / 2,  size / 2)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, textures)
    glBegin(GL_QUADS)

    # Left Face
    glTexCoord2f(0, 0); glVertex3f(-size / 2, -size / 2, -size / 2)
    glTexCoord2f(1, 0); glVertex3f(-size / 2,  size / 2, -size / 2)
    glTexCoord2f(1, 1); glVertex3f(-size / 2,  size / 2,  size / 2)
    glTexCoord2f(0, 1); glVertex3f(-size / 2, -size / 2,  size / 2)
    glEnd()

def main():
    global focus_object, prev_mouse_pos
    pg.init()
    display = (1920, 1080)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)
    pg.display.set_caption("Solar System Simulation")
    InitGL(*display)
    x = y = 0
    zoom = 1
    prev_mouse_pos = None
    while True:
        pg.time.Clock().tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    y += 2
                if event.key == pg.K_RIGHT:
                    y -= 2
                if event.key == pg.K_UP:
                    x += 2 
                if event.key == pg.K_DOWN:
                    x -= 2
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    focus_object = pickPlanet(mouse_x, mouse_y)
                    prev_mouse_pos = (mouse_x, mouse_y)
                if event.button == 3: # Right mouse button
                    focus_object = None
                    prev_mouse_pos = None
                    x = y = 0
            if event.type == pg.MOUSEMOTION and pg.mouse.get_pressed()[0]:
                if prev_mouse_pos:
                    current_mouse_pos = pg.mouse.get_pos()
                    dx = current_mouse_pos[0] - prev_mouse_pos[0]
                    dy = current_mouse_pos[1] - prev_mouse_pos[1]
                    prev_mouse_pos = current_mouse_pos
                    y += dx * 0.1  # Adjust the multiplier for sensitivity
                    x += dy * 0.1  # Adjust the multiplier for sensitivity
            if event.type == pg.MOUSEWHEEL:
                if zoom > 1 and event.y > 0 or zoom < 43 and event.y < 0:
                    if event.y > 0:
                        zoom -= 1
                    else:
                        zoom += 1
        DrawGLScene(x, y,zoom)
        pg.display.flip()
        pg.time.wait(10)

main()