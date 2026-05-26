from tkinter import *
from tkinter import ttk
from logic import *

def init_window():
    # Setting up the window, and the mainframe which contains everything
    window      = Tk()
    window.title("Work_Tracker")
    mainframe   = ttk.Frame(window)
    mainframe.grid(column=0, row=0, sticky=(N, E, S, W), padx=5, pady=5)

    # Setting widgets and their positioning
    # Row 1
    ttk.Label(mainframe, text="Add new folder for tracking:").grid(column=1, row=1, sticky=(N, W))
    separator_v = ttk.Separator(mainframe, orient="vertical")
    separator_v.grid(column=2, row=1, rowspan=2, sticky=(N, S), padx=5, pady=5)
    ttk.Label(mainframe, text="Add new website for tracking:").grid(column=3, row=1, sticky=(N, W))

    # Row 2
    path_input =    StringVar()
    website_link =  StringVar()
    path_frame =    ttk.Frame(mainframe)
    website_frame = ttk.Frame(mainframe)
    path_frame.grid(    column=1, row=2)
    website_frame.grid( column=3, row=2)
    path_entry =    ttk.Entry(path_frame, width=30, textvariable=path_input)
    path_entry.grid(column=1, row=1, sticky=W)
    ttk.Button(path_frame, text="file", command=lambda: browse_path(path_input)).grid(column=2, row=1, sticky=W)
    ttk.Button(path_frame, text="add", command=lambda: add_tracking("folder", path_input, trackee_display, path_entry)).grid(column=3, row=1, sticky=W)
    website_entry = ttk.Entry(website_frame, width=30, textvariable=website_link)
    website_entry.grid(column=1, row=1, sticky=E)
    ttk.Button(website_frame, text="add", command=lambda: add_tracking("website", website_link, trackee_display, website_entry)).grid(column=2, row=1, sticky=W)

    # Row 3
    separator_h = ttk.Separator(mainframe, orient="horizontal")
    separator_h.grid(column=1, row=3, columnspan=3, sticky=(W, E), padx=5, pady=5)

    # Row 4
    ttk.Label(mainframe, text="Currently Tracking: ").grid(column=1, row=4, sticky=(N, W))
    ttk.Button(mainframe, text="Remove trackee", command=lambda: remove_trackee(trackee_display)).grid(column=3, row=4, sticky=E)

    # Row 5
    trackee_display = Listbox(mainframe, selectmode=EXTENDED)
    trackee_display.grid(column=1, row=5, columnspan=3, sticky=(W, E))
    display_trackees_from_file(trackee_display)

    # Row 6
    ttk.Label(mainframe, text="Current Log").grid(column=1, row=6, sticky=(N, W))
    ttk.Button(mainframe, text="Open File Path", command=open_log_path).grid(column=3, row=6, sticky=E)

    # Row 7
    log_display = Listbox(mainframe, selectmode=EXTENDED)
    log_display.grid(column=1, row=7, columnspan=3, sticky=(W, E))
    display_logs_from_file(log_display)

    # Grid configuration
    mainframe.columnconfigure(2, minsize=25)

    window.mainloop()