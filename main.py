import json
import logging
import csv

# Configure logging
logging.basicConfig(
    filename="todo_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}

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

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f)
        logging.info("Saved tasks to %s", self.filename)

    def add_task(self, task, due_date=None, priority="medium"):
        new_task = Task(task, due_date, priority)
        self.tasks.append(new_task)
        logging.info("Added task: '%s' with due date: '%s' and priority: '%s'", task, due_date, priority)

    def list_tasks(self):
        if not self.tasks:
            logging.info("Listed tasks: none found.")
            print("No tasks found.")
            return
        sorted_tasks = sorted(self.tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 2))
        for i, t in enumerate(sorted_tasks, start=1):
            status = "✓" if t.done else "✗"
            due = f" (Due: {t.due_date})" if t.due_date else ""
            priority = t.priority.capitalize()
            print(f"{i}. [{status}] {t.task}{due} [Priority: {priority}]")
        logging.info("Listed %d tasks.", len(sorted_tasks))

    def mark_done(self, task_number):
        sorted_tasks = sorted(self.tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 2))
        if 1 <= task_number <= len(sorted_tasks):
            task_to_mark = sorted_tasks[task_number - 1]
            orig_index = self.tasks.index(task_to_mark)
            self.tasks[orig_index].done = True
            logging.info("Marked task as done: '%s'", task_to_mark.task)
            print(f"Task {task_number} marked as done.")
        else:
            logging.warning("Attempted to mark invalid task number: %d", task_number)
            print("Invalid task number")

    def export_tasks_to_csv(self, filename="tasks_export.csv"):
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

def menu():
    manager = ToDoListManager()
    while True:
        print("\nTo-Do List Menu:")
        print("1. List tasks (sorted by priority)")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Save & Exit")
        print("5. Export tasks to CSV")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            manager.list_tasks()
        elif choice == "2":
            task = input("Enter new task: ").strip()
            if task:
                due_date = input("Enter due date (e.g. 2025-07-01): ").strip()
                due_date = due_date if due_date else None
                priority = input("Enter priority (high, medium, low) [default: medium]: ").strip().lower()
                if priority not in PRIORITY_ORDER:
                    priority = "medium"
                manager.add_task(task, due_date, priority)
                logging.info("Task added via menu.")
                print("Task added.")
            else:
                logging.warning("Attempted to add empty task.")
                print("Empty task not added.")
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
        else:
            logging.warning("Invalid menu choice: %s", choice)
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    menu()
