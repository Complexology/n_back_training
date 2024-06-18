import tkinter as tk
from tkinter import Canvas, Tk 
import tkinter.font as tkfont


CANVAS_WIDTH = 500
CANVAS_HEIGHT = 700
TEXT_H1_SIZE=30
TEXT_H1_STYLE='Arial'
TEXT_L_SIZE=80
TEXT_L_STYLE='Arial'
TEXT_B1_SIZE=80
TEXT_B1_STYLE='Arial'
#Ktinker: This sets the root window as tkinter. The root window is the top-level window of the application, which contains all the other widgets (such as buttons, labels, and text entries)
#its needed globally because its referenced for built in functions that update and delete the window
root=Tk()
#this setsup the canvas values and makes canvas a global variable since its outside the main function
canvas = Canvas(root,width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
mouse_x=0
mouse_y=0

#Everything in this file requires TKinter and by setting it up this way you can switch out renders more easily


def bind_func_to_window_close(my_function):
    root.protocol("WM_DELETE_WINDOW",my_function)

def canvas_setup():
    #This makes the canvas widget in the GUI window
    canvas.pack()
    bind_mouse()
    return canvas

def draw_rectangle(upper_x,upper_y,lower_x,lower_y,color):
    #You have to spell out fill,height,font,etc and set it equal to our value with TKinter
    rect_object=canvas.create_rectangle(upper_x,upper_y,lower_x,lower_y,fill=color)
    return rect_object

def draw_circle(upper_x,upper_y,lower_x,lower_y,color):
    circle_object=canvas.create_oval(upper_x,upper_y,lower_x,lower_y,fill=color)
    return circle_object

def obj_move_to(obj_to_move,x,y):
    canvas.moveto(obj_to_move,x,y)
    print(obj_to_move,x,y,"object moved")

def obj_move(obj_to_move,delta_x,delta_y):
    canvas.move(obj_to_move,delta_x,delta_y)

def get_coords(obj_for_coords):
    #This returns the x and y value of the upper left hand corner as an array
    coords=canvas.coords(obj_for_coords)
    print(coords,"coords")
    return coords

def find_overlaps(upper_x,upper_y,lower_x,lower_y):
    overlaps=canvas.find_overlapping(upper_x,upper_y,lower_x,lower_y)
    return overlaps

def delete_object(obj_to_delete):
    canvas.delete(obj_to_delete)


def bind_mouse():
    canvas.bind("<Motion>",update_mouse_coords) #bind mousemotion event to update coordinates function

def create_text(x,y,words,type):
    text_object=canvas.create_text(x,y,text=words,font=get_font(type),justify='center')
    return text_object

def create_letter(x,y,letter,type):
    text_object=tk.Entry(root,justify='center',font=get_font(type),width=2,bg="red",bd=0,relief=tk.FLAT)
    text_object.insert(0,letter)
    text_object.pack(padx=5,pady=5)
    text_object.place(x=x,y=y)
    print(text_object,"letter")
    return text_object

def get_width(object):
    coords=get_coords(object)
    width=coords[2]-coords[0]
    return width

def get_height(object):
    coords=get_coords(object)
    height=coords[3]-coords[1]
    return height

def get_text_width(object):
    text_width = get_font().measure(object)
    return text_width

def get_text_height(object):
    #text_height = get_font().metrics("linespace")
    text_height=object.winfo_width()
    return text_height

def get_font(type):
    if type=='header':
        return tkfont.Font(family=TEXT_H1_STYLE,size=TEXT_H1_SIZE)
    elif type=='letter':
        return tkfont.Font(family=TEXT_L_STYLE,size=TEXT_L_SIZE)
    elif type=='button':
        return tkfont.Font(family=TEXT_B1_STYLE,size=TEXT_B1_SIZE)
    else:
        return tkfont.Font(family=TEXT_H1_STYLE,size=TEXT_H1_SIZE)
    


#This function is strange because you send an event to it so you call it like root.bind('<Motion>', update_mouse_coords) where the motion event is being sent to it and you can now access its variables inside this function
#x and y are in the motion event and we can assignt them to the global values of mouse_x and mouse_y that were instantiated before this
def update_mouse_coords(event):
    global mouse_x, mouse_y
    #this is short hand for mouse_x=event.x and mouse_y=event.y
    mouse_x,mouse_y=event.x,event.y

def setup_mainloop():
    #canvas.mainloop()
    root.mainloop()
    print("setup main loop")

#def set_TK_root():
    #root=Tk()

def update():
    #this redraws the gui and updates all tasks so its slower than just updating idol tasks and it stops the program until finished
    root.update()

def update_idol_tasks():
    #this updates the background tasks like keypresses and mouse movements and doesnt stop the program and is much faster
    root.update_idletasks()

def destroy_canvas():
    #this only closes the GUI window and its children windows and prevents more events from the GUI it does not stop the python code from running
    root.destroy

def set_text_to_center(object,container):
    contatiner_borders=get_coords(container)
    container_height=contatiner_borders[3]-contatiner_borders[1]
    container_width=contatiner_borders[2]-contatiner_borders[0]
    print(object,"test")

    if object.winfo_class()=="Entry":
        root.update_idletasks()
        text_width=object.winfo_width()
        text_height=object.winfo_height()
        print("Entry",text_height,text_width)
    else:
        text_width=get_text_width(object)
        text_height=get_text_height()
        print("text object",text_height,text_width)

    text_start_x=contatiner_borders[0]+(container_width/2)-(text_width/2)
    text_start_y=contatiner_borders[1]+(container_height/2)-(text_height/2)
    print(text_start_x,text_start_y,"top left", text_width,"width",text_height,"height")
    draw_rectangle(text_start_x,text_start_y,text_start_x+2,text_start_y+2,"GREEN")
    draw_rectangle(text_start_x+text_width,text_start_y,text_start_x+text_width+2,text_start_y+2,"GREEN")
    draw_rectangle(text_start_x,text_start_y+text_height,text_start_x+2,text_start_y+text_height+2,"GREEN")
    if object.winfo_class()=="Entry":
        object.place(x=text_start_x,y=text_start_y)
    else:
        obj_move_to(object,text_start_x,text_start_y)

