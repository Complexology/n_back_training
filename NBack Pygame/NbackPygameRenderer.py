import pygame
import pygame_widgets as widg
from pygame_widgets.button import Button
import time 
import math

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 700
TEXT_H1_SIZE=80
TEXT_H1_STYLE='Arial'
TEXT_L_SIZE=120
TEXT_L_STYLE='Arial'
TEXT_B1_SIZE=30
TEXT_B1_STYLE='Arial'
TEXT_S1_SIZE=40
TEXT_S1_STYLE='Arial'
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CORRECT=(0, 200, 20)
INCORRECT=(200,0,20)
screen=None
started=False
correct_letter_answer=None
correct_position_answer=None
pulse_speed=0.2
####ACTUALLY USED IN NBACK#####
def initialize_pygame():
    pygame.init()

def bind_func_to_window_close(my_function):
    pygame.quit()
    sys.exit()

def canvas_setup():
    global screen
    # Set up the screen and font
    screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
    return screen

def draw_rectangle(upper_x, upper_y, lower_x, lower_y, color):
    # Draw a rectangle on the screen
    rectangle=pygame.draw.rect(screen, color, (upper_x, upper_y, lower_x - upper_x, lower_y - upper_y))
    return rectangle

def draw_circle(upper_x, upper_y, lower_x, lower_y, color):
    # Draw a circle on the screen
    pygame.draw.circle(screen, color, (upper_x, upper_y), (lower_x - upper_x) / 2)

def create_text(x, y, words, type):
    font_to_use = get_font(type)
    text_surface = font_to_use.render(words, True, BLACK)
    screen.blit(text_surface, (x, y))
    return text_surface

def create_centered_text(words, type,container,axis,y):
    font_to_use = get_font(type)
    text_surface = font_to_use.render(words, True, BLACK)
    text_rect=text_surface.get_rect()
    if container is None:
        text_rect.move_ip(0, y)
        text_rect.centerx = screen.get_rect().centerx
        screen.blit(text_surface, text_rect)
    else:
        if axis=="Y":
            text_rect.center = container.center
            screen.blit(text_surface, text_rect)
        if axis=="X":
            text_rect.centerx = container.centerx
            screen.blit(text_surface, text_rect)
    return text_surface

def get_font(type):
    # Get the font for the specified type
    if type == 'header':
        return pygame.font.SysFont(TEXT_H1_STYLE, TEXT_H1_SIZE)
    elif type == 'letter':
        return pygame.font.SysFont(TEXT_L_STYLE, TEXT_L_SIZE)
    elif type == 'button':
        return pygame.font.SysFont(TEXT_B1_STYLE, TEXT_B1_SIZE)
    elif type == 'score':
        return pygame.font.SysFont(TEXT_S1_STYLE, TEXT_S1_SIZE)
    else:
        return pygame.font.SysFont("Arial", 30)
    
def destroy_canvas():
    pygame.quit()
    sys.exit()

##### NBACK BUTTONS FUNCTIONS #####

def button_widget(x,y,width,height,text,font_size,margin,default_color,hover_color,pressed_color,radius,on_click,on_click_parameters):
    button = Button(
        # Mandatory Parameters
        screen,  # Surface to place button on
        x,  # X-coordinate of top left corner
        y,  # Y-coordinate of top left corner
        width,  # Width
        height,  # Height

        # Optional Parameters
        text=text,  # Text to display
        fontSize=font_size,  # Size of font
        margin=margin,  # Minimum distance between text/image and edge of button
        inactiveColour=default_color,  # Colour of button when not being interacted with
        hoverColour=hover_color,  # Colour of button when being hovered over
        pressedColour=pressed_color,  # Colour of button when being clicked
        radius=radius,  # Radius of border corners (leave empty for not curved)
        onClick=lambda: on_click(on_click_parameters),  # Function to call when clicked on
        shadowDistance=1
        )
    return button

def start_game(args):
    global started
    print('Start') 
    started=True

def letter_check(args):
    global correct_letter_answer
    correct_letter_flg = args[0]
    IncrementScoreCallback = args[1]
    increment_miss_callback=args[2]
    #if len(correct_letter_flg)==0:
        #return
    if correct_letter_flg==1:
        correct_letter_answer=True
        IncrementScoreCallback()
        #draw_rectangle(250,140,480,200,CORRECT)
        #print("correct")
    elif correct_letter_flg==0:
        correct_letter_answer=False
        increment_miss_callback()
        #draw_rectangle(250,140,480,200,INCORRECT)
        #print("incorrect")
    #else:
        #print("no val")
    print(correct_letter_answer,correct_letter_flg)

def position_check(args):
    global correct_position_answer
    correct_position_flg = args[0]
    increment_score_callback = args[1]
    increment_miss_callback=args[2]
    #if len(correct_position_flg)==0:
        #return
    if correct_position_flg==1:
        correct_position_answer=True
        increment_score_callback()
        #draw_rectangle(250,140,480,200,CORRECT)
        #print("correct")
    elif correct_position_flg==0:
        correct_position_answer=False
        increment_miss_callback()
        #draw_rectangle(250,140,480,200,INCORRECT)
        #print("incorrect")
    #else:
        #print("no val")
    print(correct_position_answer,correct_position_flg)

def check_both(args):
    if(letter_check(args[0]) and position_check(args[1])):
        print("Both correct")
        return True
    return False

def answer_indicator_color_blink(correct_answer_flag):
    if correct_answer_flag:
        # Calculate pulsing color (green)
        t = pygame.time.get_ticks() * pulse_speed
        pulse_factor = (math.sin(t) + 1) / 2  # Maps [-1, 1] to [0, 1]
        box_color = (
            int(WHITE[0] + (CORRECT[0] - WHITE[0]) * pulse_factor),
            int(WHITE[1] + (CORRECT[1] - WHITE[1]) * pulse_factor),
            int(WHITE[2] + (CORRECT[2] - WHITE[2]) * pulse_factor),
        )
    else:
        # Calculate pulsing color (red)
        t = pygame.time.get_ticks() * pulse_speed
        pulse_factor = (math.sin(t) + 1) / 2  # Maps [-1, 1] to [0, 1]
        box_color = (
            int(WHITE[0] + (INCORRECT[0] - WHITE[0]) * pulse_factor),
            int(WHITE[1] + (INCORRECT[1] - WHITE[1]) * pulse_factor),
            int(WHITE[2] + (INCORRECT[2] - WHITE[2]) * pulse_factor),
        )

    return box_color


#####MIGHT BE USEFUL BUT NOT USED######

def obj_move_to(obj_to_move, x, y):
    # Move the object to the specified position
    obj_to_move.rect.x = x
    obj_to_move.rect.y = y

def obj_move(obj_to_move, delta_x, delta_y):
    # Move the object by the specified amount
    obj_to_move.rect.x += delta_x
    obj_to_move.rect.y += delta_y

def get_coords(obj_for_coords):
    # Get the coordinates of the object
    return obj_for_coords.rect.x, obj_for_coords.rect.y

def get_center_coords(obj):
    x = obj.rect.x + obj.rect.width / 2
    y = obj.rect.y + obj.rect.height / 2
    return x, y

def get_width(object):
    # Get the width of the object
    return object.rect.width

def get_height(object):
    # Get the height of the object
    return object.rect.height

def get_text_width(text):
    # Get the width of the text
    return font.size(text)[0]

def get_text_height(text):
    # Get the height of the text
    return font.size(text)[1]

def set_object_to_center(object, container):
    # Set the text to the center of the container
    if container is None:
        object_rect = object.get_rect(center=screen.get_rect().center)
        screen.blit(object, object_rect)
    else:
        object_rect = object.get_rect(center=container.get_rect().center)
        screen.blit(object,object_rect)

def update_mouse_coords(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.pos

def find_overlaps(upper_x, upper_y, lower_x, lower_y):
    overlaps = []
    for obj in all_sprites:
        if (upper_x <= obj.rect.x <= lower_x and
            upper_y <= obj.rect.y <= lower_y):
            overlaps.append(obj)
    return overlaps
