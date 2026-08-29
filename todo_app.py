import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "task.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-DO List")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.tasks = []

        self.create_widgets()
        self.load_tasks()
        self.refresh_list()

# GUI

def create_widget(self):

    # Title
    title = tk.label(
        self.root,
        text="TO-Do LIST",
        font=("Arial",24,"bold")
    )
    title.pack(pady=20)

    # Input frame
    input_frame = tk.Frame(self.root)
    input_frame.pack(pady=10)

    self.task_entry = tk.Entry(
        input_frame,
        width=40,
        font=("Arial",14)
    )
    self.task_entry.grid(row=0, column=0, padx=10)

    add_button = tk.Button(
        input_frame,
        text="Add Task",
        font=("Arial",11,"bold"),
        command=self.add_task
    )
    add_button.grid(row=0, column=1)

    # Task list
    list_frame =tk.Frame(self.root)
    list_frame.pack(pady=15)

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    self.task_list = tk.Listbox(
        list_frame,
        width=55,
        height=15,
        font=("Arial",13),
        yscrollcommad=scrollbar.set,
        selectmode=tk.SINGLE
    )

    self.task_list.pack(side=tk.LEFT)

    scrollbar.config(command=self.task_list.yview)

    # Buttons
    button_frame = tk.Frame(self.root)
    button_frame.pack(pady=15)

    tk.Button(
        button_frame,
        text="Complete",
        width=12,
        command=self.complete_task
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Edit",
        width=12,
        command=self.edit_task
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Delete",
        width=12,
        command=self.delete_tasks
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        button_frame,
        text="Clear All",
        width=12,
        command=self.clear_task
    ).grid(row=0, column=3, padx=5)

    # Status
    self.status_label = tk.Label(
        self.root,
        text="0 tasks",
        font=("Arial", 11) 
    )
    self.status_label.pack(pady=10)

    # Enter key adds task
    self.task_entry.bind("<Return>", lambda event: self.add_task())


# ADD TASK
def add_task(self):
    task = self.task_entry.get().strip()

    if task == "":
        messagebox.showwarning(
            "Empty Task",
            "Please enter a task."
        )
        return

    self.tasks.append({
        "text": task,
        "completed": False
    })

    self.task_entry.delete(tk.END)

    self.save_tasks()
    self.refresh_list()

# COMPLETE TASK
def complete_task(self):

    selected = self.task_list.curselection()

    if not selected:
        messagebox.showwarning(
            "No Task Selected",
            "please select a task"
        )
        return

    index = selected[0]

    self.task[index]["completed"] = True

    self.save_tasks()
    self.refresh_list()
