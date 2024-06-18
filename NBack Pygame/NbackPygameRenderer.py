import pygame

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 700
TEXT_H1_SIZE=30
TEXT_H1_STYLE='Arial'
TEXT_L_SIZE=80
TEXT_L_STYLE='Arial'
TEXT_B1_SIZE=80
TEXT_B1_STYLE='Arial'
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen=None

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
    pygame.draw.rect(screen, color, (upper_x, upper_y, lower_x - upper_x, lower_y - upper_y))

def draw_circle(upper_x, upper_y, lower_x, lower_y, color):
    # Draw a circle on the screen
    pygame.draw.circle(screen, color, (upper_x, upper_y), (lower_x - upper_x) / 2)

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

def create_text(x, y, words, type):
    font_to_use = get_font(type)
    text_surface = font_to_use.render(words, True, BLACK)
    screen.blit(text_surface, (x, y))
    return text_surface

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

def get_font(type):
    # Get the font for the specified type
    if type == 'header':
        return pygame.font.SysFont("Arial", 30)
    elif type == 'letter':
        return pygame.font.SysFont("Arial", 80)
    elif type == 'button':
        return pygame.font.SysFont("Arial", 80)
    else:
        return pygame.font.SysFont("Arial", 30)
    
def set_text_to_center(object, container):
    # Set the text to the center of the container
    object_rect = object.get_rect(center=screen.get_rect().center)
    screen.blit(object, object_rect)
    
    #object_rect = object.get_rect()
    #if container is None:
    
        # center_x = CANVAS_WIDTH / 2
        # center_y = CANVAS_HEIGHT / 2
        # object_rect.centerx = center_x
        # object_rect.centery = center_y
        # object.rect = object_rect
    # else:
    #     container_rect = container.rect
    #     object_rect.centerx = container_rect.centerx
    #     object_rect.centery = container_rect.centery
    #     object.rect = object_rect

def delete_object(obj_to_delete):
    # Remove the object from the list of sprites
    all_sprites.remove(obj_to_delete)
    # Or set its visible attribute to False
    obj_to_delete.visible = False

def update_mouse_coords(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.pos

def destroy_canvas():
    pygame.quit()
    sys.exit()

def find_overlaps(upper_x, upper_y, lower_x, lower_y):
    overlaps = []
    for obj in all_sprites:
        if (upper_x <= obj.rect.x <= lower_x and
            upper_y <= obj.rect.y <= lower_y):
            overlaps.append(obj)
    return overlaps

# class Button:
#     def __init__(self, x, y, width, height, color, text, font_size):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.color = color
#         self.text = text
#         self.font = pygame.font.SysFont("Arial", 20)
#         self.clicked = False
#         self.original_width = width  # Store the original width
#         self.original_height = height  # Store the original height

#     def draw(self, screen):
#         pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
#         font = self.font
#         #pygame.font.SysFont(None, self.font_size)
#         text_surface = font.render(self.text, True, (255, 255, 255))
#         screen.blit(text_surface, (self.x + (self.width / 2) - (text_surface.get_width() / 2), self.y + (self.height / 2) - (text_surface.get_height() / 2)))

#     def is_hovered(self, mouse_pos):
#         return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

#     def is_clicked(self, mouse_pos, mouse_pressed):
#         return self.is_hovered(mouse_pos) and mouse_pressed[0]
    
#     # def animate_click(self):
#     #     if self.clicked:
#     #         self.color = (200, 200, 200)  # Change the color to a lighter shade
#     #         if self.width>= self.original_width-50:
#     #             self.width -= 5  # Shrink the button slightly
#     #             self.height -= 5
#     #     else:
#     #         self.color = (100, 100, 100)  # Change the color back to the original
#     #         if self.width<self.original_width:
#     #             self.width+=5
#     #             self.height+=5

#     # def animate_click(self):
#     #     if self.clicked:
#     #         self.animation_state = "shrinking"
#     #     else:
#     #         self.animation_state = "growing"

#     #     if self.animation_state == "shrinking":
#     #         if self.width > 20:  # Minimum width
#     #             self.width -= 5
#     #             self.height -= 5
#     #         else:
#     #             self.animation_state = "done"
#     #     elif self.animation_state == "growing":
#     #         if self.width < self.original_width:
#     #             self.width += 5
#     #             self.height += 5
#     #         else:
#     #             self.animation_state = "done"

#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
#                 self.clicked = True
#         elif event.type == pygame.MOUSEBUTTONUP:
#             if self.clicked:
#                 self.clicked = False
#                 # Call the on_click function here
#                 self.on_click()

#     def on_click():
#         print("Button clicked!")
