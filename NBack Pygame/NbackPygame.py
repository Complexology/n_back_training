import time
import random
import math
import NbackPygameRenderer as render
import pygame
import sys
import pygame_widgets as widg   
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.toggle import Toggle
import pygame_chart as pyc
import os
from gtts import gTTS
from playsound import playsound
import tempfile

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
START_BUTTON_DEFAULT=(0,100,150)
BUTTON_DEFAULT=(119, 119, 119)
BUTTON_HOVER=(150, 150, 150)
BUTTON_CLICK=(0, 200, 20)
CORRECT=(0, 200, 20)
INCORRECT=(200,0,20)
BOX_COLOR="grey"
##########GAME SETTINGS#########
NBACK_NUMBER=1 
GAME_SPEED=150
CORRECT_ANSWER_DELAY=0.5
FLASH_DELAY=0.75
GAME_ROUNDS=4
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
score=0
can_score=True
possible_score=0
misses=0
view="main"
score_array=[]
misses_array=[]
possible_score_array=[]
rounds_array=[]
rounds=0
end_round=0
set_end_flg=True
class NBackGame:

    ######START MAIN GAME LOOP########
    def main(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        ######INSTANTIATIONS OUTSIDE LOOP BUT NOT GLOBAL######
        next_game_update_time=0
        #next_correct_answer_time=0
        next_letter_flash_time=0
        letter=None
        index=0
        #correct_place=0
        letter_flg=0
        running=True
        correct_ls=[]
        #correct_place=0
        global correct_letter
        global correct_place
        global can_score
        global possible_score
        global misses
        global NBACK_NUMBER
        global GAME_SPEED
        global FLASH_DELAY
        global GAME_ROUNDS
        global rounds
        global end_round
        global set_end_flg
        global rounds_array
        answer_box=None
        options_image = pygame.image.load('slice1_3.png').convert_alpha()
        analytics_image = pygame.image.load('slice3_3.png').convert_alpha()
        delayed_score_flg=True
        b_button_color=BUTTON_DEFAULT
        l_button_color=BUTTON_DEFAULT
        p_button_color=BUTTON_DEFAULT
        l_indicator_color=WHITE
        p_indicator_color=WHITE
        b_indicator_color=WHITE
        answer_indicator_flg=True
        extended_answers_flg=True
        voice_on_flg=False
        letters_on_flg=True
        #########INITIALIZE SOUNDS########
        pygame.mixer.init()
        start_sound=pygame.mixer.Sound("Start.mp3")
        correct_sound=pygame.mixer.Sound("correct answer.mp3")
        incorrect_sound=pygame.mixer.Sound("incorrect answer.mp3")
        button_sound=correct_sound=pygame.mixer.Sound("Button Click.mp3")


        ######INITIALIZE BUTTONS#######

        # args=[]
        # started=False
        # start_button=render.button_widget(30,80,440,50,"START",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.start_game,args)
        # letter_args=[correct_letter, self.increment_score,self.increment_misses]
        # L_BUTTON_CLICK=self.get_button_colors()[0]
        # letter_button=render.button_widget(340,150,120,50,"LETTER",20,5,BUTTON_DEFAULT,BUTTON_HOVER,L_BUTTON_CLICK,0,render.letter_check,letter_args)
        # #position_button=render.button_widget()
        # position_args=[correct_place, self.increment_score,self.increment_misses]
        # P_BUTTON_CLICK=self.get_button_colors()[1]
        # position_button=render.button_widget(40,150,120,50,"POSITION",20,5,BUTTON_DEFAULT,BUTTON_HOVER,P_BUTTON_CLICK,0,render.position_check,position_args)
        # both_args=[letter_args,position_args]
        # BOTH_BUTTON_CLICK=self.get_button_colors()[2]
        # both_button=render.button_widget(190,150,120,50,"BOTH",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BOTH_BUTTON_CLICK,0,render.check_both,both_args)
        # options_args=[letter_args,position_args]
        # options_button=render.image_button_widget(30,5,50,50,None,20,5,WHITE,BUTTON_HOVER,BOTH_BUTTON_CLICK,0,render.options_button_click,options_args,options_image)
        # analytics_args=[letter_args,position_args]
        # analytics_button=render.image_button_widget(420,5,50,50,None,20,5,WHITE,BUTTON_HOVER,BOTH_BUTTON_CLICK,0,render.check_both,analytics_args,analytics_image)
        Rounds_slider = Slider(screen, 50, 150, 400, 10, min=1, max=100, step=1, initial=GAME_ROUNDS)
        N_slider = Slider(screen, 50, 200, 400, 10, min=1, max=12, step=1, initial=NBACK_NUMBER)
        Speed_slider = Slider(screen, 50, 250, 400, 10, min=70, max=500, step=10, initial=GAME_SPEED)
        Flash_slider = Slider(screen, 50, 300, 400, 10, min=0, max=1, step=.05, initial=FLASH_DELAY)
        answer_indicator_toggle = Toggle(screen, 50, 325, 50, 15,startOn=answer_indicator_flg)
        extended_answer_toggle = Toggle(screen, 50, 360, 50, 15,startOn=extended_answers_flg)
        delayed_possible_toggle = Toggle(screen, 50, 395, 50, 15,startOn=delayed_score_flg)
        voice_toggle = Toggle(screen, 50, 430, 50, 15,startOn=voice_on_flg)
        letter_toggle=Toggle(screen, 50, 465, 50, 15,startOn=letters_on_flg)
        back_args=[self.set_view_name, 'main',N_slider]
        back_button=render.button_widget(100,10,300,50,"<<<  BACK",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.back_button_click,back_args)
        figure = pyc.Figure(screen, 30, 100, 425, 325)

        while True:
            ###SETUP TIME FOR NEXT UPDATE AND SET UPDATE FLAG WHEN IT HAS PASSED###
            current_time=time.time()
            game_update=False
            flash_letter_flg=False
            # answer_indicator_update=False
            if current_time>next_game_update_time:
                next_game_update_time=current_time+(GAME_SPEED/100)
                game_update=True
                next_letter_flash_time=current_time+((GAME_SPEED/100)*FLASH_DELAY)
                # answer_indicator_update=False
                #flash_letter_flg=False
                
            # if current_time>next_correct_answer_time:
            #     next_correct_answer_time=current_time+((GAME_SPEED/100)*CORRECT_ANSWER_DELAY)
            #     answer_indicator_update=True
                
            if current_time>next_letter_flash_time:
                # if current_time>next_game_update_time:
                #     next_letter_flash_time=current_time+((GAME_SPEED/100)*FLASH_DELAY)
                flash_letter_flg=True
                if extended_answers_flg==False:
                    b_button_color=BUTTON_DEFAULT
                    l_button_color=BUTTON_DEFAULT
                    p_button_color=BUTTON_DEFAULT

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if view=='main' and render.started:
                            #position_button=render.button_widget(40,150,120,50,"POSITION",20,5,P_BUTTON_CLICK,BUTTON_HOVER,P_BUTTON_CLICK,0,render.position_check,position_args)
                            render.position_check(position_args)
                            p_button_color=P_BUTTON_CLICK
                    elif event.key == pygame.K_RIGHT:
                        if view=='main' and render.started:
                            #letter_button=render.button_widget(340,150,120,50,"LETTER",20,5,L_BUTTON_CLICK,BUTTON_HOVER,L_BUTTON_CLICK,0,render.letter_check,letter_args)
                            render.letter_check(letter_args)
                            l_button_color=L_BUTTON_CLICK
                    elif event.key == pygame.K_DOWN:
                        if view=='main' and render.started:
                            #both_button=render.button_widget(190,150,120,50,"BOTH",20,5,BOTH_BUTTON_CLICK,BUTTON_HOVER,BOTH_BUTTON_CLICK,0,render.check_both,both_args)
                            render.check_both(both_args)
                            b_button_color=BOTH_BUTTON_CLICK
                    elif event.key == pygame.K_SPACE:
                        if view=='main':
                            render.start_game(args)
            # Clear the screen
            screen.fill(WHITE)
            
            
    ################ Draw your GUI elements here- rendered at 30fpm ########################
            if view=='main':
                #screen.fill(WHITE)
                Rounds_slider.hide()
                N_slider.hide()
                Speed_slider.hide()
                Flash_slider.hide()
                back_button.hide()
                answer_indicator_toggle.hide()
                extended_answer_toggle.hide()
                delayed_possible_toggle.hide()
                voice_toggle.hide()
                letter_toggle.hide()
                Header=render.create_centered_text("N-Back Trainer","header",None,"X",0,BLACK)
                boxes=self.create_grid()
                args=[self.reset_rounds]
                #started=False
                if render.started==False:
                    start_button=render.button_widget(30,80,440,50,"START",20,5,START_BUTTON_DEFAULT,BUTTON_HOVER,START_BUTTON_DEFAULT,0,render.start_game,args)
                else:
                    start_button=render.button_widget(30,80,440,50,"PAUSE",20,5,BUTTON_DEFAULT,BUTTON_HOVER,START_BUTTON_DEFAULT,0,render.start_game,args)
                letter_args=[correct_letter, self.increment_score,self.increment_misses]
                L_BUTTON_CLICK=self.get_button_colors()[0]
                letter_button=render.button_widget(340,150,120,50,"LETTER",20,5,l_button_color,BUTTON_HOVER,L_BUTTON_CLICK,0,render.letter_check,letter_args)
                #position_button=render.button_widget()
                position_args=[correct_place, self.increment_score,self.increment_misses]
                P_BUTTON_CLICK=self.get_button_colors()[1]
                position_button=render.button_widget(40,150,120,50,"POSITION",20,5,p_button_color,BUTTON_HOVER,P_BUTTON_CLICK,0,render.position_check,position_args)
                both_args=[letter_args,position_args]
                BOTH_BUTTON_CLICK=self.get_button_colors()[2]
                both_button=render.button_widget(190,150,120,50,"BOTH",20,5,b_button_color,BUTTON_HOVER,BOTH_BUTTON_CLICK,0,render.check_both,both_args)
                options_args=[self.set_view_name, 'options']
                options_button=render.image_button_widget(30,5,50,50,None,20,5,WHITE,BUTTON_HOVER,BOTH_BUTTON_CLICK,0,render.view_button_click,options_args,options_image)
                analytics_args=[self.set_view_name, 'analytics']
                analytics_button=render.image_button_widget(420,5,50,50,None,20,5,WHITE,BUTTON_HOVER,BOTH_BUTTON_CLICK,0,render.view_button_click,analytics_args,analytics_image)
            if view=='options':
                #screen.fill(WHITE)
                #N_slider = Slider(screen, 50, 200, 400, 10, min=0, max=12, step=1, initial=NBACK_NUMBER)
                Rounds_slider.show()
                N_slider.show()
                Speed_slider.show()
                start_button.hide()
                Flash_slider.show()
                back_button.show()
                letter_toggle.show()
                voice_toggle.show()
                answer_indicator_toggle.show()
                extended_answer_toggle.show()
                delayed_possible_toggle.show()
                NBACK_NUMBER=N_slider.getValue()
                GAME_SPEED=Speed_slider.getValue()
                FLASH_DELAY=Flash_slider.getValue()
                GAME_ROUNDS=Rounds_slider.getValue()
                answer_indicator_flg=answer_indicator_toggle.getValue()
                extended_answers_flg=extended_answer_toggle.getValue()
                delayed_score_flg=delayed_possible_toggle.getValue()
                letters_on_flg=letter_toggle.getValue()
                voice_on_flg=voice_toggle.getValue()
                game_text="Game Rounds: " + str(GAME_ROUNDS)
                game_text_obj=render.create_centered_text(game_text,"options",None,"X",110,BLACK)
                N_text="N Back: " + str(NBACK_NUMBER)
                N_text_obj=render.create_centered_text(N_text,"options",None,"X",160,BLACK)
                speed_text="Speed: " + str(GAME_SPEED/100) +'s'
                speed_text_obj=render.create_centered_text(speed_text,"options",None,"X",210,BLACK)
                flash_text="Blink: " + str('%.3f'%((GAME_SPEED/100)*(1-FLASH_DELAY))) +'s'
                flash_text_obj=render.create_centered_text(flash_text,"options",None,"X",260,BLACK)
                answer_text_obj=render.create_centered_text("Answer Indicators","options",None,"X",315,BLACK)
                extended_answer_text_obj=render.create_centered_text("Extended Answer Period","options",None,"X",345,BLACK)
                delayed_possible_text_obj=render.create_centered_text("Delayed possible correct","options",None,"X",385,BLACK)
                voice_on_text_obj=render.create_centered_text("Voice on","options",None,"X",425,BLACK)
                letters_on_text_obj=render.create_centered_text("Letters Displayed","options",None,"X",465,BLACK)
                # back_args=[self.set_view_name, 'main',N_slider]
                # back_button=render.button_widget(100,10,300,50,"<<<  BACK",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.back_button_click,back_args)
                #slider = Slider(screen, 50, 200, 400, 10, min=0, max=99, step=1)
                position_button.hide()
                letter_button.hide()
                both_button.hide()
            if view=='analytics':
                #screen.fill(WHITE)
                # back_button=render.button_widget(30,80,440,50,"BACK",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BUTTON_CLICK,0,render.view_button_click,back_args)
                back_button.show()
                start_button.hide()
                position_button.hide()
                letter_button.hide()
                both_button.hide()
                figure.line('Score',rounds_array,score_array,'BLACK',line_width=10)
                figure.line('Misses',rounds_array,misses_array,'RED',line_width=10)
                figure.line('Possible',rounds_array,possible_score_array,'BLUE',line_width=10)
                figure.draw()
    ######SLOWER EVENT LOOP THAT STARTS WITH SATRT BUTTON CLICK########
            if view=='main':
                if render.started:
                    #if possible_score<=GAME_ROUNDS:
                    if game_update:
                        can_score=True
                        return_index=self.get_random_index()
                        index=return_index[0]
                        correct_place=return_index[1]
                        return_letter=self.get_random_letter()
                        letter=return_letter[0]
                        letter_flg=return_letter[1]
                        letter_args=[correct_letter,self.increment_score,self.increment_misses]
####Place an if to delete the mp3 before running so it has time to not be in use
                        if voice_on_flg and set_end_flg:
                            mp3_file = "C:\\Users\\Lex\\Documents\\Python\\n_back_training\\text.mp3"
                            if os.path.exists(mp3_file):
                                pygame.mixer.music.unload()
                                os.remove("text.mp3")
                            text_to_speech(letter)
                        if extended_answers_flg:
                            b_button_color=BUTTON_DEFAULT
                            l_button_color=BUTTON_DEFAULT
                            p_button_color=BUTTON_DEFAULT
                        L_BUTTON_CLICK=self.get_button_colors()[0]
                        #letter_button=render.button_widget(340,150,120,50,"LETTER",20,5,BUTTON_DEFAULT,BUTTON_HOVER,L_BUTTON_CLICK,0,render.letter_check,letter_args)
                        #position_args=[correct_place,self.increment_score,self.increment_misses]
                        P_BUTTON_CLICK=self.get_button_colors()[1]
                        #position_button=render.button_widget(40,150,120,50,"POSITION",20,5,BUTTON_DEFAULT,BUTTON_HOVER,P_BUTTON_CLICK,0,render.position_check,position_args)
                        BOTH_BUTTON_CLICK=self.get_button_colors()[2]
                        #both_args=[letter_args,position_args]
                        #print(both_args)
                        #both_button=render.button_widget(190,150,120,50,"BOTH",20,5,BUTTON_DEFAULT,BUTTON_HOVER,BOTH_BUTTON_CLICK,0,render.check_both,both_args)
                        self.get_possible_score()
                        self.create_score_arrays()
                        rounds_array.append(rounds)
                        rounds+=1
                        print(rounds)
                        print(possible_score)
                        if answer_indicator_flg:
                            l_indicator_color=L_BUTTON_CLICK
                            b_indicator_color=BOTH_BUTTON_CLICK
                            p_indicator_color=P_BUTTON_CLICK
                        else:
                            l_indicator_color=WHITE
                            b_indicator_color=WHITE
                            p_indicator_color=WHITE
                        if possible_score>=GAME_ROUNDS and set_end_flg:
                            end_round=rounds+1
                            set_end_flg=False
                        if rounds==end_round:
                            render.started=False
            
                    #if answer_indicator_update:
                        #indicator_color=render.answer_indicator_color_blink(render.correct_letter_answer)
                        #answer_box=render.draw_rectangle(250,140,480,200,indicator_color)
        ######RENDERED BEFORE GAME STARTED AND AT 60FPS###########
                if letters_on_flg:
                    if (flash_letter_flg and render.started) or render.started==False:
                        letter_obj=render.create_centered_text(letter,"letter",boxes[index],"Y",None,BOX_COLOR)
                    else:
                        letter_obj=render.create_centered_text(letter,"letter",boxes[index],"Y",None,BLACK)
                else:
                    if (flash_letter_flg==False and render.started):
                        pygame.draw.rect(screen, BLACK, boxes[index])
                if possible_score==GAME_ROUNDS:
                    Score_text="N="+ str(NBACK_NUMBER) + "  Score: " + str(score) + "/" + str(possible_score) + "  Misses:"+str(misses)
                elif delayed_score_flg==True and len(possible_score_array)>NBACK_NUMBER:
                    Score_text="N="+ str(NBACK_NUMBER) + "  Score: " + str(score) + "/" + str(possible_score_array[-2]) + "  Misses:"+str(misses)
                else:
                    Score_text="N="+ str(NBACK_NUMBER) + "  Score: " + str(score) + "/" + str(possible_score) + "  Misses:"+str(misses)
                Score=render.create_centered_text(Score_text,"score",None,"X",220,BLACK)
                if render.started:
                    l_indicator=render.draw_rectangle(340,200,460,220,l_indicator_color)
                    p_indicator=render.draw_rectangle(40,200,160,220,p_indicator_color)
                    b_indicator=render.draw_rectangle(190,200,310,220,b_indicator_color)
                #Position_flg=render.create_text(10,120,f"Position: {correct_place}","button")
                #Letter_flg=render.create_text(10,140,f"Letter: {letter_flg}","button")
                #render.letter_check(letter_args)
                #letter_button.draw()
                #start_button.draw()
                #position_button.draw()    


            #mouse_pos = pygame.mouse.get_pos()
            #mouse_pressed = pygame.mouse.get_pressed()

            #Prints the widgets#
            widg.update(events)

            # Update the display
            #pygame.display.flip()
            pygame.display.update()

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
        global BOX_COLOR
        x_coords=self.get_grid_positions()[0:3]
        y_coords=self.get_grid_positions()[3:6]
        box_width=((GRID_WIDTH-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
        box_height=((GRID_HEIGHT-(GRID_GAP*(GRID_NUMBER-1)))/GRID_NUMBER)
        boxes=[]
        for x_coord in x_coords:
            for y_coord in y_coords:
                box=render.draw_rectangle(x_coord,y_coord,x_coord+box_width,y_coord+box_height,BOX_COLOR)
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

    def increment_score(self):
        global score
        global can_score
        if can_score:
            score+=1
            can_score=False
        #print("Score Incremented. New Score: ",score)
        return score
    
    def increment_misses(self):
        global can_score
        global misses
        if can_score:
            misses+=1
            can_score=False

    def get_possible_score(self):
        global correct_letter
        global correct_place
        global possible_score
        if correct_letter==1:
            possible_score+=1
        if correct_place==1:
            possible_score+=1
    
    def create_score_arrays(self):
        global possible_score_array
        global possible_score
        global misses_array
        global misses
        global score
        global score_array

        possible_score_array.append(possible_score)
        misses_array.append(misses)
        score_array.append(score)

    def set_view_name(self,screen_name):
        global view
        view=screen_name
    
    def reset_rounds(self):
        global rounds
        global possible_score
        global GAME_ROUNDS
        global possible_score_array
        global end_round
        global set_end_flg
        global score
        global misses
        if rounds==end_round:
            rounds=0
            possible_score=0
            possible_score_array=[]
            end_round=0
            set_end_flg=True
            score=0
            misses=0

def text_to_speech(text):
    language = 'en'
    speech = gTTS(text=text, lang=language, slow=False)
    speech.save("text.mp3")
    pygame.mixer.music.load("text.mp3")
    pygame.mixer.music.play()
    #playsound("text.mp3")
    #while pygame.mixer.music.get_busy():
    #    pygame.time.Clock().tick(10)
    #os.remove("text.mp3")
    #while pygame.mixer.music.get_busy():
       # pygame.time.Clock().tick(10)

# Unload the music to release the file lock
    #pygame.mixer.music.unload()

# Now you can delete the file
    #os.remove("text.mp3")

if __name__ == '__main__':
    NBackGame=NBackGame()
    NBackGame.main()