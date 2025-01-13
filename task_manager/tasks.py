from .utils import generate_id
from .database import get_connection

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