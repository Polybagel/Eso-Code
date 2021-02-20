"""

    Eso Code

    Created by Polybagel

    Written in python 3.9.1
    

"""

### imports
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from functools import partial
from tkinter import filedialog
import subprocess
import os


import interpreter

### import supported esolangs
from brainfuck import *
import brainfuck


valid_input = False
targetLang = "none"
defaultExt = ""


while not valid_input:
    print("Please select a target language: \n    Brainfuck = bf\n")
    targetLang = input(": ").lower()
    if targetLang == "bf":
        valid_input = True
        defaultExt = brainfuck.defExt
    else:
        print("\nInvalid input! Please try again.\n")

### allowed file formats###
files = [('generic', '*.txt')]

if targetLang == "bf":
    files = brainfuck.files

ex = [('Excecutable file', '*.exe')]

### generates a .bat file containing the generated command to compile the c source with gcc.
def generate_compile_batch(command,setting2):
    f=open("compile.bat","w")
    f.write(command)
    f.close()

    subprocess.call([r'compile.bat'])

    if setting2 == 0: ### don't delete the batch file
        os.remove("compile.bat")

def save_code(code):
    got = code.get("1.0",'end-1c')
    f = filedialog.asksaveasfile(mode='w', filetypes = files, defaultextension=defaultExt)
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = got
    f.write(text2save)
    f.close() # create the c file


"""
    this function is a little more complicated.

    firstly, it asks for the file destination to put the exe.
    next, it generates the gcc command to compile the c source.
    and finally, it generates a .bat file containing the command, because subprocess for some reason did not want to cooperate.

    after all that is done, it removes the c source and batch file, leaving just the exe.
"""
    
def output_code(code,setting1,setting2):
    f = filedialog.asksaveasfile(mode='w', defaultextension=".c")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = code
    f.write(text2save)
    f.close() # create the c file

    ### compile the c program, by first generated the GCC compile command
    command = "gcc \""+f.name+"\" -o \""+f.name[0:len(f.name)-2]+"\""

    generate_compile_batch(command,setting2)

    if setting1 == 0: ### don't delete the C file if the setting is set
        os.remove(f.name)

### boilerplate tkinter code#
root = Tk()

### grab the icon
BF_Icon = PhotoImage(file = 'textures/icon.png')

root.title('Eso Code')

### set the icon
root.iconphoto(False, BF_Icon)

### menu bar functions
def load_code():
    f = filedialog.askopenfile(mode='r', filetypes = files, defaultextension=defaultExt)
    content = f.readlines()

    combined = ""

    for line in content:
        combined+=line

    code.delete(1.0,"end")
    code.insert(1.0, combined)

### reset the scrolled entry text
def new_code():
    code.delete(1.0,"end")

### exit the program
def client_exit():
    exit()

def confirmCompile(c,setting1,setting2):
    code = c.get("1.0",'end-1c')

    generatedC = ""

    if targetLang == "bf":
        generatedC = brainfuck.generate_c_code(code,30000)
    
    output_code(generatedC,setting1,setting2)

### a built in BF interpreter
def interpret_code(c):

    code = c.get("1.0","end-1c")
    
    intwin = Toplevel(root)
    intwin.iconphoto(False, BF_Icon)
    intwin.geometry("400x300")
    intwin.title('Eso Code Internal '+targetLang.upper()+' Interpreter')

    interpretedOutput = ""

    if targetLang == "bf":
        interpretedOutput = interpreter.evaluate(code)

    output = Label(intwin, text=interpretedOutput)
    output.grid(row=0,column=0,padx=5,pady=5)

### retrieve the code from the scrolling entry box, and send it off to get generated into C code.
def compile_code(c):
    filewin = Toplevel(root)
    filewin.iconphoto(False, BF_Icon)
    filewin.geometry("320x120")
    filewin.title('Compile Settings')
    filewin.resizable(False, False)

    keepCcode = IntVar()
    Checkbutton(filewin, text="Don't delete generated C file", variable=keepCcode).grid(row=0, sticky=W, padx=25, pady=10)
    keepBatchfile = IntVar()
    Checkbutton(filewin, text="Don't delete generated .bat compile file", variable=keepBatchfile).grid(row=1, sticky=W, padx=25, pady=3)

    Button(filewin, text='Compile', command = lambda: confirmCompile(c,keepCcode.get(),keepBatchfile.get())).grid(row=3, sticky=S, pady=4)

### display the About window.
def about():
    filewin = Toplevel(root)
    filewin.iconphoto(False, BF_Icon)
    filewin.geometry("320x120")
    filewin.title('About Eso Code')
    filewin.resizable(False, False)
   
    label = Label(filewin, wraplength=250, text="Eso Code is designed to take source code from many popular esolangs, convert it to C code, and compile it into an .exe file using gcc.\n\nCreated by Polybagel")
    label.grid(row=0,column=0,padx=25,pady=10)

def insertMacro(source):

    mac = ""
    
    if targetLang == "bf":
        mac = brainfuck.convertStringToBF(source)
    
    code.insert(END, "\n"+mac)

def generateMacro():
    macroWin = Toplevel(root)
    macroWin.iconphoto(False, BF_Icon)
    macroWin.geometry("400x500")
    macroWin.resizable(False, False)
    macroWin.title('Generate Print String Macro')

    info = Label(macroWin, text="Generates "+targetLang.upper()+" code that prints a string.")
    info.pack(side=TOP,pady=10)

    target = ScrolledText(macroWin)
    target.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=7)

    insert = Button(macroWin, text="Insert Macro", command = lambda: insertMacro(target.get("1.0","end-1c")))
    insert.pack(pady=10)

### display the quick start guide.
def tutorial():
    filewin = Toplevel(root)
    filewin.iconphoto(False, BF_Icon)
    filewin.geometry("320x240")
    filewin.title('Eso Code Quick Start Guide')
    filewin.resizable(False, False)
   
    label = Label(filewin, wraplength=250, text="Upon opening Eso Code, you can simply paste source code from many popular esolangs into the text box.\n\nIf you want to save your code, simply go to File->Save, and select the file destination.\n\nIf you want to compile your code into an exe, go to File->Compile, and choose a file destination for the exe.\n\nTo open a source file, go to File->Open, and select the file to open.")
    label.grid(row=0,column=0,padx=25,pady=10)

### main code
code = ScrolledText(root)
code.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=10)

compile_code = partial(compile_code, code)
interpret_code = partial(interpret_code, code)
save_code = partial(save_code, code)

### menubar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)

### file cascade
filemenu.add_command(label="New", command=new_code)
filemenu.add_command(label="Open", command=load_code)
filemenu.add_command(label="Save", command=save_code)

filemenu.add_separator()

filemenu.add_command(label="Compile", command=compile_code)
filemenu.add_command(label="Interpret", command=interpret_code)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=client_exit)
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)

### macro generator cascade
macros = Menu(menubar, tearoff=0)
macros.add_command(label="Generate Print String", command=generateMacro)
menubar.add_cascade(label="Insert Macro...", menu=macros)

### help cascade
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
helpmenu.add_command(label="Quick Start Guide", command=tutorial)
menubar.add_cascade(label="Help", menu=helpmenu)

### set up the menubar
root.config(menu=menubar)
root.mainloop()


