import time
import random
import math
import NbackPygameRenderer as render
import pygame
import sys

#LAYOUT CONSTANTS
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 700
#grid
GRID_HEIGHT=400
GRID_WIDTH=400
GRID_GAP=10
GRID_NUMBER=3

#vertical padding values (CANVAS_HEIGHT=CANVAS_BOTTOM_PADDING+CANVAS_TOP_PADDING+MIDDLE_BUFFER+TOOLBOX_HEIGHT+GRID_HEIGHT)
CANVAS_BOTTOM_PADDING=(CANVAS_HEIGHT-GRID_HEIGHT)*0.05
CANVAS_TOP_PADDING=(CANVAS_HEIGHT-GRID_HEIGHT)*0.05
MIDDLE_BUFFER=(CANVAS_HEIGHT-GRID_HEIGHT)*0.10
#toolbox values
TOOLBOX_HEIGHT=(CANVAS_HEIGHT-GRID_HEIGHT)*0.80
#horizontal padding values (CANVAS_WIDTH=CANVAS_PADDING)
CANVAS_SIDE_PADDING=10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

NBACK_NUMBER=1

render.initialize_pygame()
screen=render.canvas_setup()
running=True
past_letters=[]
past_index=[]
#start_button = render.Button(100, 100, 200, 50, (100, 100, 100), "Click me!", 30)

def main():
    """Main game loop"""
    clock = pygame.time.Clock()
    pygame.display.set_caption("Button Test")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(WHITE)

        # Draw your GUI elements here
        Header=render.create_centered_text("N-Back Trainer","header",None,"X")
        boxes=create_grid()
        Letter=render.create_centered_text(get_random_letter()[0],"letter",boxes[get_random_index()[0]],"Y")
        #start_button.draw(screen)


        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        #if start_button.is_clicked(mouse_pos, mouse_pressed):
            #print("Button clicked!")

        # for event in pygame.event.get():
        #     start_button.handle_event(event)
        # start_button.draw(screen)
        # start_button.animate_click()
        #pygame.display.flip()
        #pygame.time.Clock().tick(60)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(1)

    #render.bind_mouse()
    #render.bind_func_to_window_close(set_running_false)
    ##boxes=create_grid()
    #print_letters("A",boxes[0])
    ##for box in boxes:
        ##print_letters("A",box)
    #text_id=render.create_text(10,10,"A","Arial",20)
    #print(render.get_text_width(text_id))
    ##render.create_text(250,25,"N-Back Trainer",'header')

    ##time.sleep(1)

    ##render.setup_mainloop()


def set_running_false():
    #says that you're modifying the global variable running when making modifications (must instantiate first)
    global running
    running = False
    #destroy canvas
    render.destroy_canvas()

def get_grid_position():
    box_width=((GRID_WIDTH-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
    box_height=((GRID_HEIGHT-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
    upper_x=(CANVAS_WIDTH/2)-(GRID_WIDTH/2)
    middle_x=upper_x+box_width+GRID_GAP
    bottom_x=middle_x+box_width+GRID_GAP
    upper_y=CANVAS_TOP_PADDING+TOOLBOX_HEIGHT+MIDDLE_BUFFER
    #print(CANVAS_TOP_PADDING,CANVAS_BOTTOM_PADDING,TOOLBOX_HEIGHT,MIDDLE_BUFFER,"Padding")
    middle_y=upper_y+box_height+GRID_GAP
    bottom_y=middle_y+box_height+GRID_GAP
    return upper_x,middle_x,bottom_x,upper_y,middle_y,bottom_y

def create_grid():
    x_coords=get_grid_position()[0:3]
    #print(x_coords,"X_coords set")
    y_coords=get_grid_position()[3:6]
    #print(y_coords,"Y_coords set")
    #x_coord=get_grid_position()[0]
    #print(x_coord,"Xcoord")
    #y_coord=get_grid_position()[5]
    #print(y_coord,"Ycoord")
    box_width=((GRID_WIDTH-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
    box_height=((GRID_HEIGHT-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
    #box=render.draw_rectangle(x_coord,y_coord,x_coord+box_width,y_coord+box_height,"black")
    #check=render.get_coords(box)
    #print(check,"box coords")

    boxes=[]
    for x_coord in x_coords:
        for y_coord in y_coords:
             box=render.draw_rectangle(x_coord,y_coord,x_coord+box_width,y_coord+box_height,"grey")
             boxes.append(box)
    return boxes

def print_letters(letter,container):
    #text_id=render.create_text(10,10,letter)
    text_id=render.create_letter(10,10,letter,'letter')
    print(text_id)
    render.set_text_to_center(text_id,container)

def get_random_index():
    rand_index=random.randint(0,((GRID_NUMBER*GRID_NUMBER)-1))
    past_index.append(get_random_index)
    correct_place=0
    if rand_index==past_index[-NBACK_NUMBER]:
        correct_place=1
    return rand_index,correct_place

def get_random_letter():
    rand_repeat=random.randint(0,4)
    random_upper_letter = chr(random.randint(ord('A'), ord('Z')))
    correct_letter=0
    if rand_repeat==3 and len(past_letters)>NBACK_NUMBER:
        letter=past_letters[-NBACK_NUMBER]
        past_letters.append(letter)
    else:
        letter=random_upper_letter
        past_letters.append(letter)
    if letter==past_letters[-NBACK_NUMBER]:
        correct_letter=1
    return letter,correct_letter

if __name__ == '__main__':
    main()