import sys
import os

# Adding parent path for task_manager and taskflow directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from task_manager import TaskManager

class TaskManagerGUI:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("800x600")

        self.setup_ui()

    def setup_ui(self):
        """Configure the main UI layout."""
        # Title Label
        tk.Label(self.root, text="Task Manager", font=("Helvetica", 16, "bold")).pack(pady=10)

        # Task List
        self.tree = ttk.Treeview(self.root, columns=("Title", "Description", "Priority", "Completed"), show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Completed", text="Completed")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Edit Task", command=self.edit_task).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Mark as Completed", command=self.mark_completed).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Refresh List", command=self.load_tasks).grid(row=0, column=4, padx=5)

        # Import/Export Buttons
        tk.Button(button_frame, text="Export Tasks", command=self.export_tasks).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Import Tasks", command=self.import_tasks).grid(row=1, column=1, padx=5, pady=5)

        # Load initial tasks
        self.load_tasks()

    def load_tasks(self):
        """Load tasks into the TreeView."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        tasks = self.manager.list_tasks()
        for task in tasks:
            self.tree.insert("", tk.END, values=(
                task["title"],
                task["description"],
                task["priority"],
                "Yes" if task["completed"] else "No"
            ))

    def add_task(self):
        """Open a dialog to add a new task."""
        self.open_task_dialog("Add Task", self.save_new_task)

    def save_new_task(self, title, description, priority):
        """Save a new task to the database."""
        self.manager.add_task(title, description, priority)
        self.load_tasks()

    def edit_task(self):
        """Open a dialog to edit the selected task."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task to edit.")
            return

        task_values = self.tree.item(selected[0])["values"]
        self.open_task_dialog("Edit Task", self.save_edited_task, task_values)

    def save_edited_task(self, title, description, priority):
        """Save changes to an existing task."""
        selected = self.tree.selection()
        task_values = self.tree.item(selected[0])["values"]
        task_id = self.manager.list_tasks()[self.tree.index(selected[0])]["id"]

        self.manager.update_task(task_id, title=title, description=description, priority=priority)

        self.load_tasks()

    def mark_completed(self):
        """Mark the selected task as completed."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task to mark as completed.")
            return

        task_id = self.manager.list_tasks()[self.tree.index(selected[0])]["id"]
        self.manager.mark_as_completed(task_id)
        self.load_tasks()

    def delete_task(self):
        """Delete the selected task."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a task to delete.")
            return

        task_id = self.manager.list_tasks()[self.tree.index(selected[0])]["id"]
        self.manager.delete_task(task_id)
        self.load_tasks()

    def export_tasks(self):
        """Export tasks to JSON or CSV."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return

        file_format = "json" if file_path.endswith(".json") else "csv"
        try:
            self.manager.export_tasks(file_path, file_format)
            messagebox.showinfo("Success", f"Tasks exported successfully to {file_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error while exporting tasks: {e}")

    def import_tasks(self):
        """Import tasks from JSON or CSV."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")]
        )
        if not file_path:
            return

        file_format = "json" if file_path.endswith(".json") else "csv"
        try:
            self.manager.import_tasks(file_path, file_format)
            messagebox.showinfo("Success", f"Tasks imported successfully from {file_path}.")
            self.load_tasks()
        except Exception as e:
            messagebox.showerror("Error", f"Error while importing tasks: {e}")

    def open_task_dialog(self, title, save_callback, task_values=None):
        """Open a dialog to add or edit a task."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)

        tk.Label(dialog, text="Title:").grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        title_entry = tk.Entry(dialog, width=40)
        title_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(dialog, text="Description:").grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
        description_entry = tk.Entry(dialog, width=40)
        description_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(dialog, text="Priority:").grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)
        priority_entry = ttk.Combobox(dialog, values=[0, 1, 2], state="readonly")
        priority_entry.grid(row=2, column=1, pady=5, padx=5)



        if task_values:
            title_entry.insert(0, task_values[0])
            description_entry.insert(0, task_values[1])
            priority_entry.set(task_values[2])
          

        def on_save():
            title = title_entry.get()
            description = description_entry.get()
            priority = int(priority_entry.get())

            save_callback(title, description, priority)
            dialog.destroy()

        tk.Button(dialog, text="Save", command=on_save).grid(row=4, column=1, pady=10, sticky=tk.E)
     
root = tk.Tk()   
tm = TaskManagerGUI(root)
tm.root.mainloop()