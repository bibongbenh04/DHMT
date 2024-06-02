import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import math
import imgui
from imgui.integrations.pygame import PygameRenderer

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
year_ui = 0
day_ui = 0 
camera_distance = 10
skybox_size = 100
can_moving = False
move_speed = 1.0
self_rotate = 10.0
planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto']

'''
The distance and size of the planets might need to be change for more accurate representation
'''
def DrawGLScene(x, y, camera_pos,planet_visibility):
    global earth_rot, moon_rot, earth_orbit, moon_orbit, sun_rot, camera_distance, focus_object, mercury_rot, venus_rot, mars_rot, jupiter_rot, saturn_rot, uranus_rot, neptune_rot, pluto_rot, year, day_ui, year_ui
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(y, 1, 0, 0)
    glRotatef(x, 0, 1, 0)
    glTranslatef(-camera_pos[0], -camera_pos[1], -camera_pos[2])

    glDisable(GL_DEPTH_TEST)
    drawSkyBox(skybox_size + 10)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0, 0, 20)

    glPushMatrix()

    '''
    To change position of the camera, change the first 3 parameters of gluLookAt
    '''
    gluLookAt(0, 30, 30,  
                0, 0, 0,    
                0, 1, 0) 
    
    #the sun
    glPushMatrix()
    drawSun()
    glRotatef(year, 0, 1, 0)
    year = (year + 1) % 360
    glPopMatrix()

    if planet_visibility[0] == True:
        #Mercury
        glPushMatrix()
        draw_orbit(4)
        #glRotatef((mercury_rot + 0.05) % 360, 0, 1, 0)
        drawPlanet(0.2, 4, mercury_rot, "./TexImg/mercurymap.bmp")
        glPopMatrix()

    if planet_visibility[1] == True:
        #Venus
        glPushMatrix()
        draw_orbit(8)
        drawPlanet(0.3, 8, venus_rot, "./TexImg/venusmap.bmp")
        glPopMatrix()

    if planet_visibility[2] == True:
        #Earth
        glPushMatrix()
        draw_orbit(12)
        drawEarthAndMoon(earth_rot, moon_rot)
        glPopMatrix()

    if planet_visibility[3] == True:
        #Mars
        glPushMatrix()
        draw_orbit(16)
        drawPlanet(0.5, 16, mars_rot, "./TexImg/marsmap.bmp")
        glPopMatrix()
    
    if planet_visibility[4] == True:
        #Jupiter
        glPushMatrix()
        draw_orbit(20)
        drawPlanet(0.6, 20, jupiter_rot, "./TexImg/jupitermap.bmp")
        glPopMatrix()

    if planet_visibility[5] == True:
        #saturn
        glPushMatrix()
        draw_orbit(24)
        drawPlanet(0.7, 24, saturn_rot, "./TexImg/saturnmap.bmp")
        glPopMatrix()

    if planet_visibility[6] == True:
        #uranus
        glPushMatrix()
        draw_orbit(30)
        drawPlanet(0.8, 30, uranus_rot, "./TexImg/uranusmap.bmp")
        glPopMatrix()

    if planet_visibility[7] == True:
        #neptune
        glPushMatrix()
        draw_orbit(34)
        drawPlanet(0.9, 34, neptune_rot, "./TexImg/neptunemap.bmp")
        glPopMatrix()

    if planet_visibility[8] == True:
        #pluto
        glPushMatrix()
        draw_orbit(40)
        drawPlanet (0.25, 40, pluto_rot, "./TexImg/Pluto_Made.jpg")
        glPopMatrix()

    glPopMatrix()     

    if can_moving:
        earth_rot = (earth_rot + 1) % 360
        day_ui = (day_ui + 1) % 365
        if day_ui == 0:
            year_ui += 1
        moon_rot = (moon_rot + 13 * move_speed) % 360
        mercury_rot = (mercury_rot + 4.1 * move_speed) % 360
        venus_rot = (venus_rot + 1.6 * move_speed) % 360
        mars_rot = (mars_rot + 0.5 * move_speed) % 360
        jupiter_rot = (jupiter_rot + 0.4 * move_speed) % 360
        saturn_rot = (saturn_rot + 0.3 * move_speed) % 360
        uranus_rot = (uranus_rot + 0.2 * move_speed) % 360
        neptune_rot = (neptune_rot + 0.1 * move_speed) % 360
        pluto_rot = (pluto_rot + 0.04 * move_speed) % 360

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
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/earthmap.bmp"))
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GLU_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    glPushMatrix()
    glRotatef(earth_rot, 0, 1, 0)
    glTranslatef(12, 0, 0)
    
    glLightfv(GL_LIGHT0, GL_POSITION, [-50.0, 0.0, 0.0, 1.0])  
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])  
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.5, 1.5, 1.5, 1.0])  
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.5, 1.5, 1.5, 1.0])  

    glRotatef(earth_rot * self_rotate, 0, 1, 0)
    gluSphere(Q, 0.4, 32, 16)

    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)

    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/2k_moon.jpg"))

    draw_orbit(0.6)

    glRotatef(moon_rot, 0, 1, 0)
    glTranslatef(0.6, 0, 0)

    glRotatef(moon_rot * self_rotate, 0, 1, 0)
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
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GLU_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    # Enable lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glPushMatrix()
    glRotatef(planet_rot, 0, 1, 0)
    glTranslatef(distance_to_sun, 0, 0)

    glLightfv(GL_LIGHT0, GL_POSITION, [-50.0, 0.0, 0.0, 1.0])  
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])  
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.5, 1.5, 1.5, 1.0])  
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.5, 1.5, 1.5, 1.0])  

    glRotatef(planet_rot * self_rotate, 0, 1, 0)

    gluSphere(Q, radius, 32, 16)

    glDisable(GL_LIGHTING)
    glDisable(GL_LIGHT0)

    if texture == "./TexImg/saturnmap.bmp":
        drawSaturnRing()

    gluDeleteQuadric(Q)
    glPopMatrix()

def drawSaturnRing():
    inner_radius = 1.0
    outer_radius = 1.6
    num_segments = 100  # Số lượng đoạn dùng để vẽ đường tròn
    angle_step = 2.0 * math.pi / num_segments  # Góc giữa mỗi đoạn

    glColor3f(1, 1, 1)  # Màu của quỹ đạo
    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/r.jpg"))
    glBegin(GL_QUAD_STRIP)

    for i in range(num_segments + 1):
        angle = i * angle_step
        glVertex3f(inner_radius * math.cos(angle), 0, inner_radius * math.sin(angle))
        glVertex3f(outer_radius * math.cos(angle), 0, outer_radius * math.sin(angle))

    glEnd()

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

def LoadSmolImage(fname):
    image = pg.image.load(fname)

    image = pg.transform.flip(image, False, True)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, *image.get_size(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pg.image.tostring(image, 'RGBA', 1))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id

def main():
    global focus_object, prev_mouse_pos, can_moving,planets,move_speed,self_rotate
    pg.init()
    display = (1920, 1080)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)
    pg.display.set_caption("Solar System Simulation")
    InitGL(*display)
    prev_mouse_pos = None
    camera_pos = [0, 0, -5]
    target_camera_pos = [0, 0, -5]
    smooth_factor = 0.1
    camera_rot = [0,0]
    mouse_down = False
    camera_senv = 0.5
    mouse_senv = 0.5
    max_up_down_angle = 85

    #try to create gui maybe?
    imgui.create_context()
    imgui.get_io().display_size = display
    window_created = False
    renderer = PygameRenderer()

    planet_visibility = [True for _ in range(len(planets))]

    while True:
        pg.time.Clock().tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                imgui.shutdown()
                renderer.shutdown()
                pg.quit()
                quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    pg.mouse.get_rel()
                if event.button == 3:
                    camera_rot = [0, 0]
                    camera_pos = [0, 0, -5]
                    target_camera_pos = [0, 0, -5]
                    mouse_down = False        

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False

            if pg.mouse.get_focused() and mouse_down and not imgui.get_io().want_capture_mouse:
                temp = pg.mouse.get_rel()
                camera_rot[0] += temp[0] * mouse_senv
                camera_rot[1] += temp[1] * mouse_senv

                camera_rot[0] %= 360

                if camera_rot[1] > max_up_down_angle:
                    camera_rot[1] = max_up_down_angle
                if camera_rot[1] < -max_up_down_angle:
                    camera_rot[1] = -max_up_down_angle

            keys = pg.key.get_pressed()
            if keys[pg.K_w]:
                target_camera_pos[2] += camera_senv
            if keys[pg.K_s]:
                target_camera_pos[2] -= camera_senv
            if keys[pg.K_a]:
                target_camera_pos[0] -= camera_senv
            if keys[pg.K_d]:
                target_camera_pos[0] += camera_senv
            if keys[pg.K_q]:
                camera_rot[0] -= camera_senv
            if keys[pg.K_e]:
                camera_rot[0] += camera_senv

            target_camera_pos[0] = max(min(target_camera_pos[0], skybox_size/2), -skybox_size/2)
            target_camera_pos[1] = max(min(target_camera_pos[1], skybox_size/2), -skybox_size/2)
            target_camera_pos[2] = max(min(target_camera_pos[2], skybox_size/2), -skybox_size/2)

            camera_pos[0] += (target_camera_pos[0] - camera_pos[0]) * smooth_factor
            camera_pos[1] += (target_camera_pos[1] - camera_pos[1]) * smooth_factor
            camera_pos[2] += (target_camera_pos[2] - camera_pos[2]) * smooth_factor

            if keys[pg.K_ESCAPE]:
                imgui.shutdown()
                renderer.shutdown()
                pg.quit()
                quit()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    can_moving = not can_moving
            
            renderer.process_event(event)

        #Ui things start here
        imgui.new_frame()

        if not window_created:
            imgui.set_next_window_position(191, 108)
            imgui.set_next_window_size(410, 400)
        if imgui.begin("About",True):
            imgui.text("Solar System Simulation")
            imgui.text("From Group 2 - Computer Graphics")
            imgui.text("Group Members:")
            imgui.image(LoadSmolImage("./TexImg/5-1.jpg"), 100, 100)
            imgui.same_line()
            cursor_pos = imgui.get_cursor_pos()
            text_pos = cursor_pos[1] + 25
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            #Tai's info
            imgui.text("Name: Tran Duc Tai")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("Student ID: 48.01.103.068")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("Job: Main Coding At Least I Think So xD")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("About me: *uwanttopickafightorwhat?*") 

            #Quan's info
            imgui.text("")
            imgui.image(LoadSmolImage("./TexImg/5-3.jpg"), 100, 100)
            imgui.same_line()
            cursor_pos = imgui.get_cursor_pos()
            text_pos = cursor_pos[1] + 25
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("Name: Le Hong Quan")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("Student ID: 48.01.104.108")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("Job: Main Coding yes There's 2 of us")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("About me: Look at the person below me") 

            #Tuan's info
            imgui.text("")   
            imgui.image(LoadSmolImage("./TexImg/5-2.jpg"), 100, 100)
            imgui.same_line()
            cursor_pos = imgui.get_cursor_pos()
            text_pos = cursor_pos[1]
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("Name: Tran Van Tuan")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("Student ID: 48.01.103.086")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("Job: Report Writing, Word, PPT, ...")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("About me: Everybody on this group seem to")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("not interested in this about me stuff so")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("I'll just leave it blank but maybe it's")
            text_pos += 15
            imgui.set_cursor_pos((cursor_pos[0], text_pos))
            imgui.text("not blank anymore lol xD")
            imgui.end()

        if not window_created:
            imgui.set_next_window_position(191 + 410, 108)
        if imgui.begin("Control Panel", True):
            imgui.text("Camera Position")
            imgui.text("X: %.2f" % camera_pos[0])
            imgui.text("Y: %.2f" % camera_pos[1])
            imgui.text("Z: %.2f" % camera_pos[2])
            imgui.text("Camera Rotation")
            imgui.text("X: %.2f" % camera_rot[0])
            imgui.text("Y: %.2f" % camera_rot[1])
            imgui.text("Can Move: %s" % can_moving)
            imgui.text("Year: %d" % year_ui)
            imgui.text("Day: %d" % day_ui)
            imgui.text("Press SPACE to toggle moving")
            imgui.text("Press W/A/S/D/Q/E to move the camera")
            imgui.text("Hold Left Mouse Button to rotate the camera")
            imgui.text("Hold Right Mouse Button to reset the camera")
            imgui.end()

        if not window_created:
            imgui.set_next_window_position(1920 - 342, 108)
            imgui.set_next_window_size(150, 243)
        if imgui.begin("Planet Renders", True):
            for i, planet in enumerate(planets):
                _, planet_visibility[i] = imgui.checkbox(planet, planet_visibility[i])
            imgui.end()

        if not window_created:
            imgui.set_next_window_position(1920 - 752, 108)
            imgui.set_next_window_size(410, 130)
            window_created = True
        if imgui.begin("Config",True):
            _, camera_senv = imgui.slider_float("Camera Sensitivity", camera_senv, 0.1, 1.0)
            _, mouse_senv = imgui.slider_float("Mouse Sensitivity", mouse_senv, 0.1, 1.0)
            _, move_speed = imgui.slider_float("Orbital Speed", move_speed, 0.1, 10.0)
            _, self_rotate = imgui.slider_float("Rotate Speed", self_rotate, 1.0, 100.0)
            imgui.end()

        #Ui Things end here
        
        DrawGLScene(camera_rot[0], camera_rot[1], camera_pos,planet_visibility)
        imgui.render()
        renderer.render(imgui.get_draw_data())
        pg.display.flip()
        pg.time.wait(10)

main()