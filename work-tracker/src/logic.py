import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # the base directory in this case is src/
DATA_DIR = os.path.join(BASE_DIR, "data")
TRACKEES_FILE = os.path.join(DATA_DIR, "trackee_list.txt")
LOGS_FILE     = os.path.join(DATA_DIR, "logs.csv")

def display_trackees_from_file(listbox):
    # clear and rewrite
    listbox.delete(0, END)
    with open(TRACKEES_FILE) as f:
        for line in f.read().splitlines():
            listbox.insert(END, line)

def display_logs_from_file(listbox):
    # clear and rewrite
    listbox.delete(0, END)
    with open(LOGS_FILE) as f:
        for line in f.read().splitlines():
            listbox.insert(END, line)
    

def browse_path(path_var):
    t_path = filedialog.askdirectory()
    if t_path:
        path_var.set(t_path)

def open_log_path():
    filedialog.askopenfile(initialdir=DATA_DIR)

def add_tracking(input_type, input, listbox, entry):
    inputStr = input.get()
    if inputStr and inputStr not in listbox.get(0, END):
        valid_directory = input_type == "folder" and os.path.isdir(inputStr)
        valid_website = input_type == "website" and (inputStr.startswith("http://") or inputStr.startswith("https://"))
        if valid_directory or valid_website:
            with open(TRACKEES_FILE, "a") as f:
                f.write(inputStr + '\n')
            listbox.insert(END, inputStr)
        else:
            messagebox.showerror("Invalid Entry", "Ensure the directory or website is valid.")
    else:
        pass
    entry.delete(0, END)


def remove_trackee(listbox):
    trackee_indices = listbox.curselection()
    if trackee_indices:
        trackee_names = [listbox.get(i) for i in trackee_indices]
        
        with open(TRACKEES_FILE, "r") as f:
            lines = f.read().splitlines()
    
        lines = [line for line in lines if line not in trackee_names]
        
        with open(TRACKEES_FILE, "w") as f:
            f.write("\n".join(lines))
            if lines:
                f.write("\n")

        for i in reversed(trackee_indices):
            listbox.delete(i)
    else:
        messagebox.showerror("Null Entry", "Ensure a trackee is selected.")