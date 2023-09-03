# import the pygame module, so you can use it
import pygame
import random
import time
import math
from array import *
 
pygame.font.init()

small_font_size = 15
small_font = pygame.font.SysFont(None, small_font_size)

normal_font_size = 40
normal_font = pygame.font.SysFont(None, normal_font_size)

huge_font_size = 80
huge_font = pygame.font.SysFont(None, huge_font_size)

start_time = time.time()

game_won = False

# size of screen and blocks
block_size = 64
columns = 18
rows = 14
max_x = columns - 1
max_y = rows - 1
s_width = (1 + columns) * block_size
s_height = (1 + rows) * block_size

# game grid
grid =[[None]*rows for x in range(columns)]

elements = []

moving_element = None

class Element:
    def __init__(self, name, abbr, atomic, correct_pos):
        self.name = name
        self.abbr = abbr
        self.atomic = atomic
        self.correct_pos = correct_pos

    def draw(self, surface, x, y):
        pos_x = (1 + x) * block_size
        pos_y = (s_height - block_size) - ((1 + y) * block_size)
        pygame.draw.rect(
                surface, 
                (255, 255, 255), 
                (pos_x, pos_y, block_size, block_size))

        abbr = normal_font.render(self.abbr, True, (0, 0, 0))
        text_rect = abbr.get_rect(center=(pos_x + block_size / 2, pos_y + block_size / 2 - 5))
        surface.blit(abbr, text_rect)
        
        name = small_font.render(self.name, True, (0, 0, 0))
        text_rect = name.get_rect(center=(pos_x + block_size / 2, pos_y + block_size / 2 + 15))
        surface.blit(name, text_rect)
        
        atomic = small_font.render(self.atomic, True, (0, 0, 0))
        text_rect = atomic.get_rect(topright=(pos_x + block_size - 5, pos_y + 5))
        surface.blit(atomic, text_rect)

    def check_pos(self, x, y):
        global grid
        global elements
        if self.correct_pos == (x,y):
            elements.remove(self)
        else:
            grid[x][y] = None

def gravity():
    global grid
    global moving_element

    if moving_element is not None:
        x = moving_element[0]
        y = moving_element[1]
        element = grid[x][y]
        if y > 0 and grid[x][y-1] is None:
            grid[x][y-1] = element
            grid[x][y] = None
            moving_element = (x, y-1)
        else:
            moving_element = None
            element.check_pos(x,y)

def move_left():
    global grid
    global moving_element
    if moving_element is not None:
        x = moving_element[0]
        y = moving_element[1]
        element = grid[x][y]
        if x > 0 and grid[x - 1][y] is None:
            grid[x - 1][y] = element
            grid[x][y] = None
            moving_element = (x - 1, y)

def move_right():
    global grid
    global moving_element
    if moving_element is not None:
        x = moving_element[0]
        y = moving_element[1]
        element = grid[x][y]
        if x < max_x and grid[x + 1][y] is None:
            grid[x + 1][y] = element
            grid[x][y] = None
            moving_element = (x + 1, y)

def create_elements():
    global elements
    f = open("elements.csv", "r")
    for line in f:
        split = line.split(",")
        elements.append(Element(split[0], split[1], split[2], (int(split[3]) - 1, int(split[4]) - 1)))

def spawn_element():
    global grid
    global moving_element
    if moving_element is None:
        x = random.randint(0, max_x)
        while(grid[x][max_y] is not None):
            x = random.randint(0, max_x)
        moving_element = (x, max_y)
        grid[x][max_y] = get_random_element()

def get_random_element():
    global elements
    while True:
        element = elements[random.randint(0, len(elements) - 1)]
        x = element.correct_pos[0]
        y = element.correct_pos[1]
        if y == 0 or grid[x][y - 1] is not None:
            return element

# define a main function
def main():
    global game_won
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("petris32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Petris")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((s_width, s_height))

    # define a variable to control the main loop
    running = True

    TICKEVENT = pygame.USEREVENT+1
    tick_time = 500

    pygame.time.set_timer(TICKEVENT, tick_time)

    create_elements()
    
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == TICKEVENT:
                gravity()
                if len(elements) > 0:
                    spawn_element()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left()
                if event.key == pygame.K_RIGHT:
                    move_right()
                if event.key == pygame.K_DOWN:
                    gravity()

        if(len(elements) > 0):
            draw_grid(screen)
        elif not game_won:
            game_won = True
            win_text = "Alles richtig!"
            win = huge_font.render(win_text, True, (10,200,10))
            text_rect = win.get_rect(center=(s_width / 2, s_height / 2 - 55))
            screen.blit(win, text_rect)

            current_time = time.time()
            time_diff = math.trunc(current_time - start_time)
            time_text = "Zeit: {time_diff} Sekunden".format(time_diff = time_diff)
            timer = huge_font.render(time_text, True, (10,200,10))
            text_rect = timer.get_rect(center=(s_width / 2, s_height / 2 + 55))
            screen.blit(timer, text_rect)

            pygame.display.update()


def draw_grid(surface):
    surface.fill((0,0,0))

    coord_color = (30, 30, 30)

    for x in range(columns):
        pygame.draw.line(surface, coord_color, ((x + 1) * block_size, 0), ((x + 1) * block_size, s_height))
        x_coord = normal_font.render(str(x + 1), True, coord_color)
        text_rect = x_coord.get_rect(center=((x + 1.5) * block_size, (rows + 0.5) * block_size))
        surface.blit(x_coord, text_rect)

    for y in range(rows):
        pygame.draw.line(surface, coord_color, (0, (y + 1) * block_size), (s_width, (y + 1) * block_size))
        y_coord = normal_font.render(str(y + 1), True, coord_color)
        text_rect = y_coord.get_rect(center=(0.5 * block_size, s_height - (y + 1.5) * block_size))
        surface.blit(y_coord, text_rect)

    current_time = time.time()
    time_diff = math.trunc(current_time - start_time)

    timer = normal_font.render(str(time_diff), True, coord_color)
    text_rect = timer.get_rect(center=((columns + 0.5) * block_size, 0.5 * block_size))
    surface.blit(timer, text_rect)

    for x in range(columns):
        for y in range(rows):
            if grid[x][y] is not None:
                grid[x][y].draw(surface,x,y)


    pygame.display.update()

     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
