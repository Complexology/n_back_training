import time
import random
import math
import NbackPygameRenderer as render
import pygame
import sys
import pygame_widgets as widg   
from pygame_widgets.button import Button

####LAYOUT CONSTANTS#####
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

########COLOR CONSTANTS########
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_DEFAULT=(200, 50, 0)
BUTTON_HOVER=(150, 0, 0)
BUTTON_CLICK=(0, 200, 20)
CORRECT=(0, 200, 20)
INCORRECT=(200,0,20)
##########GAME SETTINGS#########
NBACK_NUMBER=1
GAME_SPEED=100
#########INSTANTIATIONS######
# running=True
past_letters=[]
# correct_ls=[]
past_index=[]
# correct_place=0
# correct_letter=0
######SETUP CANVAS & WINDOW#####
render.initialize_pygame()
screen=render.canvas_setup()
######INITIALIZE BUTTONS#######
# args=[]
# start_button=render.button_widget(30,80,440,50,"START",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.start_game,args)
# started=False
# letter_args=[]
# letter_button=render.button_widget(270,150,200,50,"LETTER",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.letter_check,letter_args)
#position_button=render.button_widget()

######START MAIN GAME LOOP########
def main():
    """Main game loop"""
    clock = pygame.time.Clock()
    ######VARIABLES TO BE RESET EACH LOOP######
    next_game_update_time=0
    letter=None
    index=0
    index_flg=0
    letter_flg=0
    running=True
    correct_ls=[]
    correct_place=0
    correct_letter=0
    ######INITIALIZE BUTTONS#######
    args=[]
    start_button=render.button_widget(30,80,440,50,"START",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.start_game,args)
    started=False
    letter_args=[]
    letter_button=render.button_widget(270,150,200,50,"LETTER",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.letter_check,letter_args)
    #position_button=render.button_widget()

    while True:

        ###SETUP TIME FOR NEXT UPDATE AND SET UPDATE FLAG WHEN IT HAS PASSED###
        current_time=time.time()
        game_update=False
        if current_time>next_game_update_time:
            next_game_update_time=current_time+(GAME_SPEED/100)
            game_update=True


        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(WHITE)
        
         
        ################ Draw your GUI elements here########################
        Header=render.create_centered_text("N-Back Trainer","header",None,"X")
        boxes=create_grid()

        ######SLOWER EVENT LOOP THAT STARTS WITH SATRT BUTTON CLICK########
        if render.started:
            if game_update:
                return_index=get_random_index()
                index=return_index[0]
                index_flg=return_index[1]
                return_letter=get_random_letter()
                letter=return_letter[0]
                letter_flg=return_letter[1]
                letter_args=[correct_letter]
                letter_button=render.button_widget(270,150,200,50,"LETTER",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.letter_check,letter_args)

        ######RENDERED BEFORE GAME STARTED AND AT 60FPS###########
        Letter=render.create_centered_text(letter,"letter",boxes[index],"Y")
        Position_flg=render.create_text(10,120,f"Position: {index_flg}","button")
        Letter_flg=render.create_text(10,140,f"Letter: {letter_flg}","button")
        render.letter_check(letter_args)
        #letter_button.draw()
        #start_button.draw()
        #position_button.draw()    


        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        #Prints the widgets#
        widg.update(events)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(30)


def start_game():
    started=True

def set_running_false():
    global running
    running = False
    #destroy canvas
    render.destroy_canvas()

def get_grid_positions():
    box_width=((GRID_WIDTH-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
    box_height=((GRID_HEIGHT-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
    upper_x=(CANVAS_WIDTH/2)-(GRID_WIDTH/2)
    middle_x=upper_x+box_width+GRID_GAP
    bottom_x=middle_x+box_width+GRID_GAP
    upper_y=CANVAS_TOP_PADDING+TOOLBOX_HEIGHT+MIDDLE_BUFFER
    middle_y=upper_y+box_height+GRID_GAP
    bottom_y=middle_y+box_height+GRID_GAP
    return upper_x,middle_x,bottom_x,upper_y,middle_y,bottom_y

def create_grid():
    x_coords=get_grid_positions()[0:3]
    y_coords=get_grid_positions()[3:6]
    box_width=((GRID_WIDTH-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
    box_height=((GRID_HEIGHT-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
    boxes=[]
    for x_coord in x_coords:
        for y_coord in y_coords:
             box=render.draw_rectangle(x_coord,y_coord,x_coord+box_width,y_coord+box_height,"grey")
             boxes.append(box)
    return boxes

def print_letters(letter,container):
    text_id=render.create_letter(10,10,letter,'letter')
    print(text_id)
    render.set_text_to_center(text_id,container)

def get_random_index():
    global correct_place
    rand_index=random.randint(0,((GRID_NUMBER*GRID_NUMBER)-1))
    past_index.append(rand_index)
    correct_place=0
    if len(past_index)>(NBACK_NUMBER):
        if rand_index==past_index[-1*(NBACK_NUMBER+1)]:
            correct_place=1
    return rand_index,correct_place

def get_random_letter():
    global correct_letter
    rand_repeat=random.randint(0,5)
    random_upper_letter = chr(random.randint(ord('A'), ord('Z')))
    correct_letter=0
    if rand_repeat==3 and len(past_letters)>NBACK_NUMBER:
        letter=past_letters[-NBACK_NUMBER]
        past_letters.append(letter)
    else:
        letter=random_upper_letter
        past_letters.append(letter)
    if len(past_letters)>(NBACK_NUMBER+1):
        if letter==past_letters[-1*(NBACK_NUMBER+1)]:
            correct_letter=1
    #correct_ls.append(correct_letter)
    return letter,correct_letter



if __name__ == '__main__':
    main()