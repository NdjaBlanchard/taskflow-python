import sys
import os

# Adding parent path for task_manager and taskflow directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import TaskManager from task_manager
from task_manager.tasks import TaskManager

def show_menu():
    """Displays the main menu."""
    print("\nTask Manager - Menu")
    print("1. Add a task")
    print("2. Mark a task as completed")
    print("3. Update a task")
    print("4. Delete a task")
    print("5. Show all tasks")
    print("6. Filter tasks (by priority or status)")
    print("7. Quit")
    
def add_task(manager):
    """Adding a new task"""
    title = input("Task title: ")
    description = input("Task description: ")
    priority = int(input("Task priority (0 = low, 1 = medium, 2 = high): "))
    task_id = manager.add_task(title, description, priority)
    print(f"Task added successfully! ID: {task_id}")
    
def mark_as_completed(manager):
    """Mark a task as completed."""
    task_id = input("ID of task to mark as completed: ")
    try:
        manager.mark_as_completed(task_id)
        print("Task marked as completed.")
    except Exception as e:
        print(f"Error : {e}")
        
def update_task(manager):
    """Updates an existing task."""
    task_id = input("ID of the to be updated: ")
    title = input("New title (leave empty so as not to change): ")
    description = input("New description (leave empty so as not to change): ")
    priority = input("New priority (leave empty so as not to change): ")
    
    try:
        priority = int(priority) if priority else None
        manager.update_task(task_id, title=title if title else None, description = description if description else None, priority=priority)
    except Exception as e:
        print(f"Error: {e}")


def delete_task(manager):
    """Deletes a task."""
    task_id = input("ID of task to be deleted: ")
    try:
        manager.delete_task(task_id)
        print("Task successfully deleted.")
    except Exception as e:
        print(f"Error : {e}")


def list_tasks(manager):
    """Display all tasks"""
    tasks = manager.list_tasks()
    if tasks:
        print("\nTasks :")
        for task in tasks:
            print(f"ID: {task['id']}, Title: {task['title']}, Description: {task['description']}, Priority: {task['priority']}, Completed: {task['completed']}")
    else:
        print("No task found.")


def filter_tasks(manager):
    """Filter tasks by status or priority."""
    completed = input("Filter by status (1 = completed, 0 = not completed, leave blank to ignore): ")
    priority = input("Filter by priority (leave blanck to ignore): ")
    
    try:
        completed = bool(int(completed)) if completed else None
        priority = int(priority) if priority else None
        
        tasks = manager.list_tasks(completed=completed, priority=priority)
        if tasks:
            print("\Filtered tasks: ")
            for task in tasks:
                 print(f"ID: {task['id']}, Title: {task['title']}, Priority: {task['priority']}, Completed: {task['completed']}")
        else:
            print("\nNo task found with these criteria.")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """CLI application's main entry point."""
    manager = TaskManager()

    while True:
        show_menu()
        choice = input("Choose an option : ")

        if choice == "1":
            add_task(manager)
        elif choice == "2":
            mark_as_completed(manager)
        elif choice == "3":
            update_task(manager)
        elif choice == "4":
            delete_task(manager)
        elif choice == "5":
            list_tasks(manager)
        elif choice == "6":
            filter_tasks(manager)
        elif choice == "7":
            print("GoodBye !")
            sys.exit()
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()