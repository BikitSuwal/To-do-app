import json
import logging
import csv

logging.basicConfig(
    filename="todo_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}

class InvalidCommandError(Exception):
    """Custom exception for invalid menu commands."""
    pass

class Task:
    def __init__(self, task, due_date=None, priority="medium", done=False):
        self.task = task
        self.due_date = due_date
        self.priority = priority
        self.done = done

    def to_dict(self):
        return {
            "task": self.task,
            "due_date": self.due_date,
            "priority": self.priority,
            "done": self.done
        }

    @staticmethod
    def from_dict(data):
        return Task(
            task=data.get("task", ""),
            due_date=data.get("due_date"),
            priority=data.get("priority", "medium"),
            done=data.get("done", False)
        )

class ToDoListManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in data]
            logging.info("Loaded tasks from %s", self.filename)
        except FileNotFoundError:
            self.tasks = []
            logging.warning("No tasks file found. Starting with an empty list.")
        except json.JSONDecodeError:
            self.tasks = []
            logging.error("Corrupted tasks file. Starting with an empty list.")

    def save_tasks(self):
        try:
            with open(self.filename, "w") as f:
                json.dump([t.to_dict() for t in self.tasks], f)
            logging.info("Saved tasks to %s", self.filename)
        except (IOError, OSError) as e:
            logging.error("Failed to save tasks: %s", str(e))

    def add_task(self, task, due_date=None, priority="medium"):
        if not task:
            logging.warning("Attempted to add empty task.")
            raise ValueError("Task description cannot be empty.")
        if priority not in PRIORITY_ORDER:
            priority = "medium"
        new_task = Task(task, due_date, priority)
        self.tasks.append(new_task)
        logging.info("Added task: '%s' with due date: '%s' and priority: '%s'", task, due_date, priority)

    def list_tasks(self):
        if not self.tasks:
            logging.info("Listed tasks: none found.")
            print("No tasks found.")
            return
        # Sort tasks by priority and done status for consistent display and selection
        sorted_tasks = sorted(self.tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, PRIORITY_ORDER["medium"]), t.done))
        for i, t in enumerate(sorted_tasks, start=1):
            status = "✓" if t.done else "✗"
            due = f" (Due: {t.due_date})" if t.due_date else ""
            priority = t.priority.capitalize()
            print(f"{i}. [{status}] {t.task}{due} [Priority: {priority}]")
        logging.info("Listed %d tasks.", len(sorted_tasks))

    def mark_done(self, task_number):
        try:
            # Use the same sorting as in list_tasks for consistency
            sorted_tasks = sorted(self.tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, PRIORITY_ORDER["medium"]), t.done))
            if 1 <= task_number <= len(sorted_tasks):
                task_to_mark = sorted_tasks[task_number - 1]
                orig_index = self.tasks.index(task_to_mark)
                self.tasks[orig_index].done = True
                logging.info("Marked task as done: '%s'", task_to_mark.task)
                print(f"Task {task_number} marked as done.")
            else:
                logging.warning("Attempted to mark invalid task number: %d", task_number)
                print("Invalid task number")
        except Exception as e:
            logging.error("Error marking task as done: %s", str(e))
            print("An error occurred while marking the task as done.")

    def export_tasks_to_csv(self, filename="tasks_export.csv"):
        try:
            with open(filename, mode="w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["task", "duedate", "priority", "status"])
                for t in self.tasks:
                    status = "done" if t.done else "not done"
                    writer.writerow([
                        t.task,
                        t.due_date or "",
                        t.priority,
                        status
                    ])
            logging.info("Exported tasks to CSV file: %s", filename)
        except (IOError, OSError) as e:
            logging.error("Failed to export tasks to CSV: %s", str(e))
            print("Failed to export tasks to CSV.")

    def delete_task(self, task_number):
        try:
            # Use the same sorting as in list_tasks for consistency
            sorted_tasks = sorted(self.tasks, key=lambda t: (PRIORITY_ORDER.get(t.priority, PRIORITY_ORDER["medium"]), t.done))
            if 1 <= task_number <= len(sorted_tasks):
                task_to_delete = sorted_tasks[task_number - 1]
                orig_index = self.tasks.index(task_to_delete)
                deleted_task = self.tasks.pop(orig_index)
                logging.info("Deleted task: '%s'", deleted_task.task)
                print(f"Task {task_number} deleted.")
            else:
                logging.warning("Attempted to delete invalid task number: %d", task_number)
                print("Invalid task number")
        except Exception as e:
            logging.error("Error deleting task: %s", str(e))
            print("An error occurred while deleting the task.")

def menu():
    manager = ToDoListManager()
    while True:
        print("\nTo-Do List Menu:")
        print("1. List tasks (sorted by priority)")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Save & Exit")
        print("5. Export tasks to CSV")
        print("6. Delete task")

        try:
            choice = input("Choose an option (1-6): ").strip()
            if choice == "1":
                manager.list_tasks()
            elif choice == "2":
                task = input("Enter new task: ").strip()
                due_date = input("Enter due date (e.g. 2025-07-01): ").strip()
                due_date = due_date if due_date else None
                priority = input("Enter priority (high, medium, low) [default: medium]: ").strip().lower()
                try:
                    manager.add_task(task, due_date, priority)
                    logging.info("Task added via menu.")
                    print("Task added.")
                except ValueError as ve:
                    print(str(ve))
            elif choice == "3":
                manager.list_tasks()
                try:
                    num = int(input("Enter task number to mark done: ").strip())
                    manager.mark_done(num)
                except ValueError:
                    logging.error("Non-integer input for marking task as done.")
                    print("Invalid input, please enter a number.")
            elif choice == "4":
                manager.save_tasks()
                logging.info("User exited and tasks saved.")
                print("Tasks saved. Goodbye!")
                break
            elif choice == "5":
                manager.export_tasks_to_csv()
                print("Tasks exported to tasks_export.csv")
            elif choice == "6":
                manager.list_tasks()
                try:
                    num = int(input("Enter task number to delete: ").strip())
                    manager.delete_task(num)
                except ValueError:
                    logging.error("Non-integer input for deleting task.")
                    print("Invalid input, please enter a number.")
            else:
                logging.error("Invalid menu choice: %s", choice)
                raise InvalidCommandError("Invalid choice. Please select 1-6.")
        except InvalidCommandError as ice:
            print(ice)
        except KeyboardInterrupt:
            print("\nExiting gracefully. Saving tasks...")
            manager.save_tasks()
            break
        except Exception as e:
            logging.error("Unexpected error: %s", str(e))
            print("An unexpected error occurred.")
        finally:
            # Any cleanup if needed in future
            pass

if __name__ == "__main__":
    menu()
