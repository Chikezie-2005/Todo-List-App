import tkinter as tk
from tkinter import messagebox
import json
import os


FILE_NAME = "tasks.json"


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.tasks = []

        self.create_widgets()
        self.load_tasks()
        self.refresh_list()

    # -----------------------------
    # GUI
    # -----------------------------
    def create_widgets(self):

        # Title
        title = tk.Label(
            self.root,
            text="TO-DO LIST",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)

        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(
            input_frame,
            width=40,
            font=("Arial", 14)
        )
        self.task_entry.grid(row=0, column=0, padx=10)

        add_button = tk.Button(
            input_frame,
            text="Add Task",
            font=("Arial", 11, "bold"),
            command=self.add_task
        )
        add_button.grid(row=0, column=1)

        # Task list
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=15)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_list = tk.Listbox(
            list_frame,
            width=55,
            height=15,
            font=("Arial", 13),
            yscrollcommand=scrollbar.set,
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
            command=self.delete_task
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="Clear All",
            width=12,
            command=self.clear_tasks
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

    # -----------------------------
    # Add task
    # -----------------------------
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

        self.task_entry.delete(0, tk.END)

        self.save_tasks()
        self.refresh_list()

    # -----------------------------
    # Complete task
    # -----------------------------
    def complete_task(self):

        selected = self.task_list.curselection()

        if not selected:
            messagebox.showwarning(
                "No Task Selected",
                "Please select a task."
            )
            return

        index = selected[0]

        self.tasks[index]["completed"] = True

        self.save_tasks()
        self.refresh_list()

    # -----------------------------
    # Edit task
    # -----------------------------
    def edit_task(self):

        selected = self.task_list.curselection()

        if not selected:
            messagebox.showwarning(
                "No Task Selected",
                "Please select a task."
            )
            return

        index = selected[0]

        current_task = self.tasks[index]["text"]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")
        edit_window.geometry("400x150")
        edit_window.resizable(False, False)

        tk.Label(
            edit_window,
            text="Edit Task",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        entry = tk.Entry(
            edit_window,
            width=40,
            font=("Arial", 12)
        )
        entry.pack()

        entry.insert(0, current_task)
        entry.focus()

        def save_edit():

            new_task = entry.get().strip()

            if new_task == "":
                messagebox.showwarning(
                    "Empty Task",
                    "Task cannot be empty."
                )
                return

            self.tasks[index]["text"] = new_task

            self.save_tasks()
            self.refresh_list()

            edit_window.destroy()

        tk.Button(
            edit_window,
            text="Save",
            width=12,
            command=save_edit
        ).pack(pady=10)

    # -----------------------------
    # Delete task
    # -----------------------------
    def delete_task(self):

        selected = self.task_list.curselection()

        if not selected:
            messagebox.showwarning(
                "No Task Selected",
                "Please select a task."
            )
            return

        index = selected[0]

        confirm = messagebox.askyesno(
            "Delete Task",
            "Are you sure you want to delete this task?"
        )

        if confirm:

            self.tasks.pop(index)

            self.save_tasks()
            self.refresh_list()

    # -----------------------------
    # Clear all tasks
    # -----------------------------
    def clear_tasks(self):

        if not self.tasks:
            return

        confirm = messagebox.askyesno(
            "Clear All",
            "Are you sure you want to delete all tasks?"
        )

        if confirm:

            self.tasks.clear()

            self.save_tasks()
            self.refresh_list()

    # -----------------------------
    # Refresh list
    # -----------------------------
    def refresh_list(self):

        self.task_list.delete(0, tk.END)

        for task in self.tasks:

            if task["completed"]:
                display_text = "✓ " + task["text"]
            else:
                display_text = "☐ " + task["text"]

            self.task_list.insert(
                tk.END,
                display_text
            )

        count = len(self.tasks)

        completed = sum(
            task["completed"]
            for task in self.tasks
        )

        self.status_label.config(
            text=f"{count} tasks | {completed} completed"
        )

    # -----------------------------
    # Save tasks
    # -----------------------------
    def save_tasks(self):

        try:

            with open(FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(
                    self.tasks,
                    file,
                    indent=4
                )

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                f"Could not save tasks:\n{error}"
            )

    # -----------------------------
    # Load tasks
    # -----------------------------
    def load_tasks(self):

        if not os.path.exists(FILE_NAME):
            return

        try:

            with open(FILE_NAME, "r", encoding="utf-8") as file:
                self.tasks = json.load(file)

        except Exception as error:

            messagebox.showerror(
                "Load Error",
                f"Could not load tasks:\n{error}"
            )


# -----------------------------
# Start application
# -----------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = TodoApp(root)

    root.mainloop()