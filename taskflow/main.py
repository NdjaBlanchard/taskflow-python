import sys
import os

# Adding parent path for task_manager and taskflow directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import TaskManager from task_manager
from task_manager.tasks import TaskManager

# Initializing the task manager

manager = TaskManager()

# Adding tasks
task_id_1 = manager.add_task("Go shopping", "Buy milk, eggs and bread.", priority=2)
task_id_2 = manager.add_task("Read a book", "Read 'Python for Data Analysis'.", priority=1)
task_id_3 = manager.add_task("Go to the gym", "Doing a workout.", priority=3)

# Listing all the tasks
print("All the tasks")

for task in manager.list_tasks():
    print(task)
    
# Display only unfinished tasks
print("\nUncompleted tasks :")
for task in manager.list_tasks(completed=False):
    print(task)

# Display tasks with a specific priority (example: priority 2)
print("Tasks with priority 2:")
for task in manager.list_tasks(priority=2):
    print(task)

# Mark a task as completed
manager.mark_as_completed(task_id_1)

# Afficher les tâches après mise à jour
print("\nTâches après mise à jour :")
for task in manager.list_tasks():
    print(task)

# Supprimer une tâche
manager.delete_task(task_id_3)

# Viewing updated tasks
print("\nRemaining Tasks after deleting :")
for task in manager.list_tasks():
    print(task)