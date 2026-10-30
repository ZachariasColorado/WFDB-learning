from asyncio.windows_events import NULL
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from EEG_VIS_package_COLDEV import main as graphdrawer

import os

window = Tk()
files_to_open = []
listvariable = StringVar()
file_list = Listbox(master=window, height=20,width=50, listvariable=listvariable)



def main():
    window.title("EEG VIS")
    window.geometry("500x500")
    #buttons:
    file_open_button = Button(master=window, height=2, width=30, text="Open Recording File", command=select_file)
    dir_open_button = Button(master=window, height=2, width=30, text="Open Folder of Recordings", command=select_directory)
    #file_list = Listbox(master=window, height=30,width=40, listvariable=listvariable)
    open_graph_button =Button(master=window, height=2, width=30, text="Open Graph", command=open_graph)
    file_open_button.pack()
    dir_open_button.pack()
    file_list.pack()
    open_graph_button.pack()
    window.mainloop()

def select_file():
    filename = askopenfilename(title="open a waveform", initialdir="/", filetypes=[("wave data", "*.dat"),("header file","*.hea"), ("all files","*.*")])
    files_to_open.append(filename.split(".")[0])
    file_list.insert(END, filename.split(".")[0])

def select_directory():
    directory = filedialog.askdirectory(title="Select Folder", initialdir="/")
    contents = os.listdir(directory)
    for file in contents:
        cleanName = directory+"/"+file.split(".")[0]

        if file.endswith(".hea") and not (files_to_open.__contains__(cleanName)):
            files_to_open.append(cleanName)
            file_list.insert(END, cleanName)
        elif file.endswith(".dat") and not (files_to_open.__contains__(file)):
            files_to_open.append(cleanName)
            file_list.insert(END, cleanName)
        else:
            continue

    file_list.pack()

def open_graph():
    graphdrawer.main(files_to_open)
    pass

main()