__author__ = 'wisp'

# Import a library of functions called 'pygame'
import pygame
from math import sin,cos,pi
import time

# Initialize the game engine
pygame.init()

# Text using system font
font = pygame.font.SysFont("monospace", 15)

# Define the colors we will use in RGB format
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
COLORS = [BLUE, GREEN, RED]

# Set the height and width of the screen
canvas = 1000
size = [canvas, canvas]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Polypoly")

#Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

def translate(poly, x, y):
    for point in poly:
        point[0] += x
        point[1] += y
    return poly

# translate point to new coordinate system
def point(point, length):
    return [point[0] + length, point[1] + length]

def radians(deg):
    return deg * pi/180

def rotate(point, degrees, origin = [0,0]):
    x = point[0] - origin[0]
    y = point[1] - origin[1]
    newx = (x*cos(radians(degrees))) - (y*sin(radians(degrees)))
    newy = (x*sin(radians(degrees))) + (y*cos(radians(degrees)))
    newx += origin[0]
    newy += origin[1]

    return [int(newx), int(newy)]

def rotate_all(poly, angle):
    new_poly = []
    for points in poly:
        new_poly.append(rotate(points, angle))
    return new_poly

def polygon(n, size = 50):

    start_point = [-size, -size]
    all_points = []

    for i in range(0, n):
        all_points.append(rotate(start_point, 360 / n * i))

    return all_points

def handleMouseMotionEvent(event):
   (mouseX,mouseY) = event.pos
   print "Mouse is at x=" + str(mouseX) + " y=" + str(mouseY)

min_poly = 3
poly_count = 8
circle_radius = 250
current_rotation = 0
speed = .3
running = True
while not done:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # mouse wheel up
            if event.button == 4:
                speed += .1
            # mouse wheel down
            elif event.button == 5:
                speed -= .1

    # left mouse button
    if pygame.mouse.get_pressed()[0] == 1:
        if poly_count > 3:
            poly_count -= 1
    # middle mouse button
    if pygame.mouse.get_pressed()[1] == 1:
        running = not running
    # right mouse button
    if pygame.mouse.get_pressed()[2] == 1:
        poly_count += 1

    # This limits the while loop to a max of 30 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(30)

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop

    # All drawing code happens after the for loop and but
    # inside the main while done==False loop.

    # Clear the screen and set the screen background
    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, [0, canvas/2], [canvas, canvas/2])
    pygame.draw.line(screen, BLACK, [canvas/2, 0], [canvas/2, canvas])

    my_poly = translate(polygon(poly_count, circle_radius), canvas/2, canvas/2)
    pygame.draw.polygon(screen, BLACK, my_poly, 2)

    for i in range(min_poly, min_poly+poly_count):
        angle = (360.0 / poly_count * (i-min_poly)) + current_rotation
        if running:
            current_rotation += speed
        my_poly = translate(rotate_all(translate(polygon(i), circle_radius, circle_radius), angle), canvas/2, canvas/2)
        r = (255.0 / poly_count + i * poly_count + current_rotation) % 255
        g = (255.0 / poly_count + 2 * i * poly_count + current_rotation) % 255
        b = (255.0 / poly_count + 3 * i * poly_count + current_rotation) % 255
        pygame.draw.polygon(screen, (r, g, b), my_poly, 5)

    # render text
    text_poly_count = font.render('Number of polygones: %d' % poly_count, 1, (255,0,0))
    text_speed = font.render('Current speed: %.1f' % speed, 1, (255,0,0))
    text_paused = font.render('PAUSE', 1, (255,0,0))
    screen.blit(text_poly_count, (10, 10))
    screen.blit(text_speed, (10, 30))
    if not running and (int(time.time()*5) % 2 == 0):
        screen.blit(text_paused, (canvas - 60, 10))

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()