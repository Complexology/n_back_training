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
BUTTON_DEFAULT=(119, 119, 119)
BUTTON_HOVER=(150, 150, 150)
BUTTON_CLICK=(0, 200, 20)
CORRECT=(0, 200, 20)
INCORRECT=(200,0,20)
##########GAME SETTINGS#########
NBACK_NUMBER=1
GAME_SPEED=100
CORRECT_ANSWER_DELAY=0.5
#########GLOBAL INSTANTIATIONS######
# running=True
past_letters=[]
# correct_ls=[]
past_index=[]
correct_place=0
correct_letter=0
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
score=0
class NBackGame:

    ######START MAIN GAME LOOP########
    def main(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        ######INSTANTIATIONS OUTSIDE LOOP BUT NOT GLOBAL######
        next_game_update_time=0
        next_correct_answer_time=0
        letter=None
        index=0
        #correct_place=0
        letter_flg=0
        running=True
        correct_ls=[]
        #correct_place=0
        global correct_letter
        global correct_place
        answer_box=None
        

        ######INITIALIZE BUTTONS#######

        args=[]
        start_button=render.button_widget(30,80,440,50,"START",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.start_game,args)
        started=False
        letter_args=[correct_letter, self.IncrementScore]
        L_BUTTON_CLICK=self.get_button_colors()[0]
        letter_button=render.button_widget(340,150,120,50,"LETTER",20,5,BUTTON_DEFAULT,BUTTON_HOVER,L_BUTTON_CLICK,0,render.letter_check,letter_args)
        #position_button=render.button_widget()
        position_args=[correct_place, self.IncrementScore]
        P_BUTTON_CLICK=self.get_button_colors()[1]
        position_button=render.button_widget(40,150,120,50,"POSITION",20,5,BUTTON_DEFAULT,BUTTON_HOVER,P_BUTTON_CLICK,0,render.position_check,position_args)
        both_args=[letter_args,position_args]
        BOTH_BUTTON_CLICK=self.get_button_colors()[2]
        both_button=render.button_widget(190,150,120,50,"BOTH",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BOTH_BUTTON_CLICK,0,render.check_both,both_args)
        
        while True:

            ###SETUP TIME FOR NEXT UPDATE AND SET UPDATE FLAG WHEN IT HAS PASSED###
            current_time=time.time()
            game_update=False
            # answer_indicator_update=False
            if current_time>next_game_update_time:
                next_game_update_time=current_time+(GAME_SPEED/100)
                game_update=True
                answer_indicator_update=False
                
            if current_time>next_correct_answer_time:
                next_correct_answer_time=current_time+((GAME_SPEED/100)*CORRECT_ANSWER_DELAY)
                answer_indicator_update=True
                


            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Clear the screen
            screen.fill(WHITE)
            
            
            ################ Draw your GUI elements here########################
            Header=render.create_centered_text("N-Back Trainer","header",None,"X",0)
            boxes=self.create_grid()

            ######SLOWER EVENT LOOP THAT STARTS WITH SATRT BUTTON CLICK########
            if render.started:
                if game_update:
                    return_index=self.get_random_index()
                    index=return_index[0]
                    correct_place=return_index[1]
                    return_letter=self.get_random_letter()
                    letter=return_letter[0]
                    letter_flg=return_letter[1]
                    letter_args=[correct_letter,self.IncrementScore]
                    L_BUTTON_CLICK=self.get_button_colors()[0]
                    letter_button=render.button_widget(340,150,120,50,"LETTER",20,5,BUTTON_DEFAULT,BUTTON_HOVER,L_BUTTON_CLICK,0,render.letter_check,letter_args)
                    #letter_button=render.button_widget(270,150,200,50,"LETTER",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.letter_check,letter_args)
                    position_args=[correct_place,self.IncrementScore]
                    P_BUTTON_CLICK=self.get_button_colors()[1]
                    position_button=render.button_widget(40,150,120,50,"POSITION",20,5,BUTTON_DEFAULT,BUTTON_HOVER,P_BUTTON_CLICK,0,render.position_check,position_args)
                    BOTH_BUTTON_CLICK=self.get_button_colors()[2]
                    both_args=[letter_args,position_args]
                    print(both_args)
                    both_button=render.button_widget(190,150,120,50,"BOTH",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BOTH_BUTTON_CLICK,0,render.check_both,both_args)
                
                #if answer_indicator_update:
                    #indicator_color=render.answer_indicator_color_blink(render.correct_letter_answer)
                    #answer_box=render.draw_rectangle(250,140,480,200,indicator_color)
            ######RENDERED BEFORE GAME STARTED AND AT 60FPS###########
            Letter=render.create_centered_text(letter,"letter",boxes[index],"Y",None)
            Score_text="Score: " + str(score)
            Score=render.create_centered_text(Score_text,"score",None,"X",220)
            #Position_flg=render.create_text(10,120,f"Position: {correct_place}","button")
            #Letter_flg=render.create_text(10,140,f"Letter: {letter_flg}","button")
            #render.letter_check(letter_args)
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


    def start_game(self):
        started=True

    def set_running_false(self):
        global running
        running = False
        #destroy canvas
        render.destroy_canvas()

    def get_grid_positions(self):
        box_width=((GRID_WIDTH-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
        box_height=((GRID_HEIGHT-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
        upper_x=(CANVAS_WIDTH/2)-(GRID_WIDTH/2)
        middle_x=upper_x+box_width+GRID_GAP
        bottom_x=middle_x+box_width+GRID_GAP
        upper_y=CANVAS_TOP_PADDING+TOOLBOX_HEIGHT+MIDDLE_BUFFER
        middle_y=upper_y+box_height+GRID_GAP
        bottom_y=middle_y+box_height+GRID_GAP
        return upper_x,middle_x,bottom_x,upper_y,middle_y,bottom_y

    def create_grid(self):
        x_coords=self.get_grid_positions()[0:3]
        y_coords=self.get_grid_positions()[3:6]
        box_width=((GRID_WIDTH-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
        box_height=((GRID_HEIGHT-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
        boxes=[]
        for x_coord in x_coords:
            for y_coord in y_coords:
                box=render.draw_rectangle(x_coord,y_coord,x_coord+box_width,y_coord+box_height,"grey")
                boxes.append(box)
        return boxes

    def print_letters(self,letter,container):
        text_id=render.create_letter(10,10,letter,'letter')
        print(text_id)
        render.set_text_to_center(text_id,container)

    def get_random_index(self):
        global correct_place
        rand_index=random.randint(0,((GRID_NUMBER*GRID_NUMBER)-1))
        past_index.append(rand_index)
        correct_place=0
        if len(past_index)>(NBACK_NUMBER):
            if rand_index==past_index[-1*(NBACK_NUMBER+1)]:
                correct_place=1
        return rand_index,correct_place

    def get_random_letter(self):
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

    def get_button_colors(self):
        global correct_letter
        global correct_place
        if correct_letter==1 and correct_place==1:
            BOTH_BUTTON_CLICK=CORRECT
        else:
            BOTH_BUTTON_CLICK=INCORRECT
        if correct_letter==1:
            L_BUTTON_CLICK=CORRECT
        else:
            L_BUTTON_CLICK=INCORRECT
        if correct_place==1:
            P_BUTTON_CLICK=CORRECT
        else:
            P_BUTTON_CLICK=INCORRECT
        return L_BUTTON_CLICK,P_BUTTON_CLICK,BOTH_BUTTON_CLICK

    def IncrementScore(self):
        global score
        score+=1
        print("Score Incremented. New Score: ",score)
        return score



if __name__ == '__main__':
    NBackGame=NBackGame()
    NBackGame.main()