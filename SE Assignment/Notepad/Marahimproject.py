from tkinter import *
from tkinter import messagebox as mb
from tkinter import font
from tkinter import filedialog
from tkinter import dialog
from tkinter.filedialog import askopenfilename,asksaveasfilename
import os

background_color = "grey40"
# font_variable = StringVar()


# functions for the menu bar 
#opening file function
def open_file():

    #making it global so it can be changed in the whole program
    global file 

    #using the tkinter built in ask open file name dailog and giving it the default extension .txt 
    #filetypes as all files will be *.* so we can write the name before and after the .
    #and text document has only one format that is before . we can write name and after . its .txt format
    file = askopenfilename(defaultextension=".txt",filetypes=[("All Files", "*.*"),("Text Documents", "*.txt")])

    #if no file is opened in the dialog then the file will be none
    if file == "":
        file = None

    # if file is opened in the dialog then do the following
    else:

        #change the title of the window to this
        notepad.title(os.path.basename(file) + " - Notepad")

        #delete the text in the textarea till the end
        text_area.delete(1.0,END)

        #open file in r mode
        f = open(file,"r")

        #insert the data in the file in the textarea
        text_area.insert(1.0,f.read())

        #close the file
        f.close()

#function for saving the file
def save_file():

    #make the file variable global
    global file 

    #if file is none before then
    if file == None:

        #open the tkinter save file dialog with intialfile as untitled.txt and default extension as .txt and filetype
        #all file as *.* and text document type as *.txt
        file = asksaveasfilename(initialfile="untitled.txt",defaultextension=".txt",filetypes=[("All Files", "*.*"),("Text Documents", "*.txt")])
        #if no file is saved in the dailog then
        if file == None:
            #make file none
            file = None
        else:
            #open the file in w mode
            f = open(file,"w")

            #write the text area content in the file 
            f.write(text_area.get(1.0,END))

            #close the file
            f.close()

            #make the title of the window as the filename and something
            notepad.title(os.path.basename(file) + " - Notepad")
            print("File Saved")
    else:
        #open the file in w mode
        f = open(file,"w")
        #write the text area content in the file 
        f.write(text_area.get(1.0,END))
        #close the file
        f.close()

def new_file():
    global file
    notepad.title("Untitled - Notepad")
    file = None
    text_area.delete(1.0,END)

def font_function():
    font_box = mb.askokcancel("Fonts","Choose the fonts")

#Class for notepad
class my_gui(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Marahim Azal - Notepad")
        self.geometry("800x600")
        self.wm_iconbitmap("notepad_edit_icon.ico")
    



if __name__=="__main__":
    notepad = my_gui()
    notepad.configure(background=background_color,highlightbackground="grey70")
    font_list_var = []
    for item in  font.families():
        font_list_var.append(item)

    #Text area
    text_area = Text(notepad,font="Arial 14",background=background_color,fg="white")
    text_area.pack(expand=True,fill=BOTH)

    #file
    file = None

    #Menu_bar
    menu_bar = Menu(notepad,background=background_color)
    #file menu in menu bar
    file_menu = Menu(menu_bar,tearoff=0)
    file_menu.add_command(label ="New",command=new_file,activebackground=background_color)
    file_menu.add_command(label ="Open",command=open_file,activebackground=background_color)
    file_menu.add_command(label ="Save",command=save_file,activebackground=background_color)

    file_menu.add_separator()

    file_menu.add_command(label="Exit",command=lambda : notepad.destroy(),activebackground=background_color)
    menu_bar.add_cascade(label="File",menu=file_menu,background=background_color,activebackground=background_color)


    #Edit menu in menu bar
    edit_menu = Menu(menu_bar,tearoff=0)
    edit_menu.add_command(label="Cut",command=lambda:text_area.event_generate(("<<Cut>>")),activebackground=background_color)
    edit_menu.add_command(label="Copy",command=lambda:text_area.event_generate(("<<Copy>>")),activebackground=background_color)
    edit_menu.add_command(label="Paste",command=lambda:text_area.event_generate(("<<Paste>>")),activebackground=background_color)
    edit_menu.add_command(label="Fonts",command=font_function,activebackground=background_color)
    menu_bar.add_cascade(label="Edit",menu=edit_menu,background=background_color,activebackground=background_color)


    #Help mneu in menu bar
    help_menu = Menu(menu_bar,tearoff=0)
    help_menu.add_command(label="About",command=lambda:mb.showinfo("About","This notepad is created by Muhammad Jalal and its in early development phase so many functionalities will be added later "),activebackground=background_color)
    menu_bar.add_cascade(label="Help",menu=help_menu,activebackground=background_color)


    #Scroll feature 
    scroll = Scrollbar(text_area,cursor="arrow",background="grey70",activebackground="grey70",highlightbackground="grey70",highlightcolor="grey70")
    scroll.pack(side=RIGHT,fill=Y)
    scroll.config(command=text_area.yview)
    text_area.config(yscrollcommand=scroll.set)
    
    #Cofiguring the menu bar in the notepad window
    notepad.config(menu=menu_bar)

    #running the main loop
    notepad.mainloop()