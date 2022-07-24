# # # # # # # # # # # #
# To-Do List by Maria #
# # # # # # # # # # # #

import sqlite3
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showwarning

# General Program Settings
PROGRAM_NAME = "To-Do List"
LIGHT = "#fdfdfd"
DARK = "#e6e6e6"
BLACK = "black"
TEXT_FG = "#484848"
FONT = "Open Sans"
ENTRY_VALUE = "Task"
TEXT_VALUE = "Description"
TASK_COLOR = "#BEBEBE"

# Program Task Database
connection = sqlite3.connect("tasks.db")
connection.execute('''CREATE TABLE IF NOT EXISTS task_data (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL, color TEXT NOT NULL, status INTEGER NOT NULL)''')
cursor = connection.cursor()


# User-Generated Task
class Task:

    # General Settings
    def __init__(self, frame, id, name, description, color, status):

        # Task Data
        self.id = id
        self.name = " " + name + " "
        self.description = description
        self.color = color
        self.status = status

        # Task Frame
        self.task_frame = Frame(frame, bg=LIGHT, highlightbackground=self.color, highlightthickness=1)

        # Task Name
        font = self.font()
        self.task_name = Label(self.task_frame, text=self.name, font=font, bg=LIGHT, fg=TEXT_FG, padx=10, pady=10)
        self.task_name.grid(row=0, column=0, columnspan=2, sticky='we')

        # Complete Button
        self.complete_button = Button(self.task_frame, text=" Mark As Complete ", bg="#E0E0E0",
                                      activebackground="#D3D3D3",
                                      fg="#404040", activeforeground="#404040", font=(FONT, 12, 'normal'),
                                      borderwidth=0,
                                      relief=SUNKEN, command=self.update)
        self.complete_button.grid(row=1, column=0, padx=(20, 10), pady=(0, 10), sticky='we')

        # Delete Button
        self.delete_button = Button(self.task_frame, text=" Delete ", bg="#E0E0E0", activebackground="#D3D3D3",
                                    fg="#404040", activeforeground="#404040", font=(FONT, 12, 'normal'),
                                    borderwidth=0, relief=SUNKEN, command=self.delete)
        self.delete_button.grid(row=1, column=1, padx=(0, 20), pady=(0, 10), sticky='we')

        # Content Frame
        self.task_content = Frame(self.task_frame, bg=LIGHT)
        self.task_content.grid(row=0, column=2, rowspan=2, padx=(0, 20), pady=0, sticky='nswe')

        # Task Description
        self.task_text = Text(self.task_content, height=4, pady=10, fg=TEXT_FG, bg=LIGHT, font=(FONT, 12, 'normal'),
                              wrap=WORD, highlightthickness=0, relief=FLAT)
        self.task_text.pack(fill=BOTH)
        self.task_text.insert(END, self.description)
        self.task_text.config(state=DISABLED)

        # Render Task
        self.task_frame.pack(fill=X, pady=10)

        # Frame Configuration
        self.task_frame.grid_columnconfigure(2, weight=1)

    # Completion Status
    def font(self):
        return (FONT, 14, "normal", "overstrike") if self.status == 1 else (FONT, 14, "normal")

    # Update Task
    def update(self):

        # Update (Database)
        cursor.execute('UPDATE task_data SET status = ? WHERE id = ?;', (0 if self.status == 1 else 1, self.id))
        connection.commit()

        # Update (GUI)
        self.status = cursor.execute('SELECT DISTINCT status FROM task_data WHERE id = ?;', [self.id]).fetchone()[0]
        self.task_name.config(font=self.font())

    # Delete Task
    def delete(self):

        # Delete (Database)
        cursor.execute('DELETE FROM task_data WHERE id = ?;', [self.id])
        connection.commit()

        # Delete (GUI)
        self.task_frame.pack_forget()
        self.task_frame.destroy()


# Scrollable Task Frame
class ScrollFrame(Frame):

    # General Settings
    def __init__(self, parent):

        # Frame Content
        Frame.__init__(self, parent)
        self.canvas = Canvas(self, borderwidth=0, background="#ffffff", highlightthickness=0)
        self.frame = Frame(self.canvas, background="#ffffff", padx=30, pady=20)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Content Location
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")

        # Content Configuration
        self.frame.bind("<Configure>", self.scroll_region)
        self.canvas.bind('<Configure>', self.auto_resize)

        # Task List
        self.populate_tasks()

        # Scroll Settings
        self.bind('<Enter>', self.scrollable)
        self.bind('<Leave>', self.not_scrollable)

    # Populate Tasks
    def populate_tasks(self):
        for id, name, description, color, status in cursor.execute('SELECT * FROM task_data'):
            Task(self.frame, id, name, description, color, status)

    # Scroll Region
    def scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Auto Resize
    def auto_resize(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    # Enable Scroll
    def scrollable(self, event):
        self.bind_all('<MouseWheel>', self.scroll)

    # Unable Scroll
    def not_scrollable(self, event):
        self.unbind_all('<MouseWheel>')

    # Scroll Settings
    def scroll(self, event):
        self.canvas.update()
        if self.frame.winfo_reqheight() > self.canvas.winfo_screenheight() - 60:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# To-Do List Program
class Program:

    # General Settings
    def __init__(self):

        # Program Window
        self.window = Tk()
        self.window.title(PROGRAM_NAME)
        self.window.state('zoomed')
        self.window.minsize(width=640, height=480)
        self.window.config(bg=LIGHT)

        # Action Frame
        self.action_frame = Frame(self.window, bg=DARK, width=400, padx=30, pady=30)
        self.action_frame.grid(row=0, column=0, sticky='nsw')

        # Action Content
        self.action_content = Frame(self.action_frame, bg=DARK)
        self.action_content.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Program Title
        self.title_label = Label(self.action_content, text=PROGRAM_NAME, font=("Georgia", 28, "bold"), bg=DARK)
        self.title_label.grid(row=0, column=0, columnspan=2, padx=30, pady=(0, 30), sticky='we')

        # Task Entry
        self.task_title = StringVar(self.action_content, value=ENTRY_VALUE)
        self.task_entry = Entry(self.action_content, textvariable=self.task_title, fg=TEXT_FG,
                                font=(FONT, 14, 'normal'), highlightthickness=0, borderwidth=5, relief=FLAT)
        self.task_entry.grid(row=1, column=0, sticky='nswe')

        self.task_entry.bind("<FocusIn>", self.entry_focus_in)
        self.task_entry.bind("<FocusOut>", self.entry_focus_out)

        self.task_text = Text(self.action_content, width=1, height=5, padx=5, pady=5, fg=TEXT_FG,
                              font=(FONT, 14, 'normal'), wrap=WORD, highlightthickness=0, relief=FLAT)
        self.task_text.grid(row=2, column=0, columnspan=2, pady=20, sticky='we')
        self.task_text.insert(END, TEXT_VALUE)

        self.task_text.bind("<FocusIn>", self.text_focus_in)
        self.task_text.bind("<FocusOut>", self.text_focus_out)

        # Color Picker
        self.color = TASK_COLOR
        self.color_picker = Button(self.action_content, text="  Color  ", bg="#C0C0C0", activebackground="#A9A9A9",
                                   font=(FONT, 14, 'normal'), borderwidth=0, relief=SUNKEN, command=self.get_color)
        self.color_picker.grid(row=1, column=1, padx=(15, 0), sticky='nse')

        # Create Button
        self.create_button = Button(self.action_content, text=" Create Task ", bg="#C0C0C0", activebackground="#A9A9A9",
                                    font=(FONT, 14, 'normal'), borderwidth=0, relief=SUNKEN, command=self.create_task)
        self.create_button.grid(row=3, column=0, columnspan=2, sticky='we')

        # List Frame
        self.list_frame = Frame(self.window, bg=LIGHT)
        self.list_frame.grid(row=0, column=1, rowspan=2, sticky='nswe')

        # List Content
        self.scrollframe = ScrollFrame(self.list_frame)
        self.scrollframe.pack(side=TOP, fill=BOTH, expand=True)

        # Window Configuration
        self.window.grid_rowconfigure(0, minsize=100, weight=1)
        self.window.grid_columnconfigure(0, weight=0)
        self.window.grid_columnconfigure(1, weight=1)

        # Run Program
        self.window.mainloop()

    # Create Task
    def create_task(self):

        # User Input
        name = self.task_entry.get().strip()
        description = self.task_text.get("1.0", END).strip()

        # Error Handling
        if name in ["", ENTRY_VALUE] or description in ["", TEXT_VALUE]:

            # Warning Message
            showwarning(title="Warning", message="Please fill all of the fields.")

        else:

            # Task Info
            status = 0
            color = self.color

            # Database Entry
            cursor.execute("INSERT INTO task_data VALUES (:id, :name, :description, :color, :status)", {
                'id': None,
                'name': name,
                'description': description,
                'color': color,
                'status': status})
            connection.commit()

            # Reset Action
            self.color = TASK_COLOR
            self.task_text.delete("1.0", END)
            self.text_focus_out("dummy")
            self.task_entry.delete(0, END)

            # Create Task
            Task(self.scrollframe.frame, cursor.lastrowid, name, description, color, status)

        # Action Focus
        self.task_entry.focus()

    # Entry Focus
    def entry_focus_in(self, _):
        if self.task_entry.get().strip() == ENTRY_VALUE:
            self.task_entry.delete(0, END)
            self.task_entry.config(fg=BLACK)

    # Entry Focus
    def entry_focus_out(self, _):
        if self.task_entry.get().strip() == "":
            self.task_entry.delete(0, END)
            self.task_entry.config(fg=TEXT_FG)
            self.task_entry.insert(0, ENTRY_VALUE)

    # Text Focus
    def text_focus_in(self, _):
        if self.task_text.get("1.0", END).strip() == TEXT_VALUE:
            self.task_text.delete("1.0", END)
            self.task_text.config(fg=BLACK)

    # Text Focus
    def text_focus_out(self, _):
        if self.task_text.get("1.0", END).strip() == "":
            self.task_text.delete("1.0", END)
            self.task_text.config(fg=TEXT_FG)
            self.task_text.insert(END, TEXT_VALUE)

    # Task Color
    def get_color(self):
        colors = askcolor(title="Color Picker")
        self.color = colors[1]


# To-Do List Program
program = Program()
