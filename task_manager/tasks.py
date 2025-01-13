import os
import sys

# Adding parent path for task_manager and taskflow directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from task_manager.utils import generate_id
from task_manager.database import get_connection
import json
import csv


class TaskManager:
    def __init__(self):
        """Initializing a TasK Manager."""
        self.conn = get_connection()
        
    def add_task(self, title, description, priority=0):
        """
        Adding a new task
        The default priority is 0 (low priority).
        """
        task_id = generate_id()
        
        with self.conn:
            self.conn.execute( "INSERT INTO tasks (id, title, priority, description) VALUES (?, ?, ?, ?)",
                (task_id, title, priority, description))
        
        return task_id
    
    def mark_as_completed(self, task_id):
        """Marking a task as completed"""
        with self.conn:
            self.conn.execute(
                "UPDATE tasks SET completed = 1 WHERE id = ?",
                (task_id,)
            )
        
    def update_task(self, task_id, title=None, priority=None, description=None):
        """Updates the title, the priority and/or description of a task."""
        if not title and not description and not priority:
            return  # If no field is provided, do nothing

        fields = []
        values = []

        if title:
            fields.append("title = ?")
            values.append(title)

        if priority:
            fields.append("priority = ?")
            values.append(priority)

        if description:
            fields.append("description = ?")
            values.append(description)
        
        query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
        values.append(task_id)

        with self.conn:
            self.conn.execute(query, tuple(values))

    def delete_task(self, task_id):
        """Deletes a task from the database."""
        with self.conn:
            self.conn.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )
            
    def list_tasks(self, completed=None, priority=None):
        """
        Returns all tasks with filter options:
        - `completed`: True (completed), False (not completed), or None (all tasks).
        - priority`: Filters by a specific priority.
        """
        cursor = self.conn.cursor()
        query = "SELECT id, title, description, priority, completed FROM tasks WHERE 1=1"
        params = []

        if completed is not None:
            query += " AND completed = ?"
            params.append(1 if completed else 0)

        if priority is not None:
            query += " AND priority = ?"
            params.append(priority)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "priority": row[3],
                "completed": bool(row[4])
            }
            for row in rows
        ]
        
    def export_tasks(self, file_path, file_format="json"):
        """
         Exports tasks to a JSON or CSV file.
        :param file_path: Path of file to be exported.
        :param file_format: File format ("json" or "csv").
        """
        
        tasks = self.list_tasks()
        if file_format == "json":
            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(tasks, json_file, ensure_ascii=False, indent=4)
        elif file_format == "csv":
            with open(file_path, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["id", "title", "description", "priority", "completed"])
                writer.writeheader()
                writer.writerows(tasks)
        else:
            raise ValueError("Format non pris en charge. Utilisez 'json' ou 'csv'.")

    def import_tasks(self, file_path, file_format="json"):
        """
        Imports tasks from a JSON or CSV file.
        :param file_path: Path of file to be imported.
        :param file_format: File format (“json” or “csv”).
        """
        
        if file_format == "json":
            
            with open(file_path, "r", encoding="utf-8") as json_file:
                tasks = json.load(json_file)
                
        elif file_format == "csv":
        
            with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
                    reader = csv.DictReader(csv_file)
                    tasks = [row for row in reader]
        
        else:
            raise ValueError("Format not supported. Use 'json' or 'csv'")
        
        # Add each task to the database
        for task in tasks:
                      
            task_id =  self.add_task(
                title=task["title"],
                description=task["description"],
                priority=task["priority"]
            )
            
            if task["completed"] == "True" or task["completed"] is True:
                self.mark_as_completed(task_id)
                
    def list_tasks_sorted(self, sort_by="priority"):
        """
        Returns all sorted tasks.
        :param sort_by: Sort criteria ("priority", "completed", "title").
        """
        tasks = self.list_tasks()
        if sort_by == "priority":
            return sorted(tasks, key=lambda x: x["priority"], reverse=True)
        elif sort_by == "completed":
            return sorted(tasks, key=lambda x: x["completed"])
        elif sort_by == "title":
            return sorted(tasks, key=lambda x: x["title"].lower())
        else:
            raise ValueError("Invalid sort criteria. Use 'priority', 'completed' or 'title'.")