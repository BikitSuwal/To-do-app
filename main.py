import json
import logging

# Configure logging
logging.basicConfig(
    filename="todo_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

tasks = []
PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}

def load_tasks(filename="tasks.json"):
    global tasks
    try:
        with open(filename, "r") as f:
            tasks = json.load(f)
        logging.info("Loaded tasks from %s", filename)
    except FileNotFoundError:
        tasks = []
        logging.warning("No tasks file found. Starting with an empty list.")

def save_tasks(filename="tasks.json"):
    with open(filename, "w") as f:
        json.dump(tasks, f)
    logging.info("Saved tasks to %s", filename)

def add_task(task, due_date=None, priority="medium"):
    tasks.append({"task": task, "done": False, "due_date": due_date, "priority": priority})
    logging.info("Added task: '%s' with due date: '%s' and priority: '%s'", task, due_date, priority)

def list_tasks():
    if not tasks:
        logging.info("Listed tasks: none found.")
        print("No tasks found.")
        return
    sorted_tasks = sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.get("priority", "medium"), 2))
    for i, t in enumerate(sorted_tasks, start=1):
        status = "✓" if t["done"] else "✗"
        due = f" (Due: {t['due_date']})" if t.get("due_date") else ""
        priority = t.get("priority", "medium").capitalize()
        print(f"{i}. [{status}] {t['task']}{due} [Priority: {priority}]")
    logging.info("Listed %d tasks.", len(sorted_tasks))

def mark_done(task_number):
    sorted_tasks = sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.get("priority", "medium"), 2))
    if 1 <= task_number <= len(sorted_tasks):
        task_to_mark = sorted_tasks[task_number - 1]
        orig_index = tasks.index(task_to_mark)
        tasks[orig_index]["done"] = True
        logging.info("Marked task as done: '%s'", task_to_mark["task"])
        print(f"Task {task_number} marked as done.")
    else:
        logging.warning("Attempted to mark invalid task number: %d", task_number)
        print("Invalid task number")

def menu():
    load_tasks()
    while True:
        print("\nTo-Do List Menu:")
        print("1. List tasks (sorted by priority)")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Save & Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            list_tasks()
        elif choice == "2":
            task = input("Enter new task: ").strip()
            if task:
                due_date = input("Enter due date (e.g. 2025-07-01): ").strip()
                due_date = due_date if due_date else None
                priority = input("Enter priority (high, medium, low) [default: medium]: ").strip().lower()
                if priority not in PRIORITY_ORDER:
                    priority = "medium"
                add_task(task, due_date, priority)
                logging.info("Task added via menu.")
                print("Task added.")
            else:
                logging.warning("Attempted to add empty task.")
                print("Empty task not added.")
        elif choice == "3":
            list_tasks()
            try:
                num = int(input("Enter task number to mark done: ").strip())
                mark_done(num)
            except ValueError:
                logging.error("Non-integer input for marking task as done.")
                print("Invalid input, please enter a number.")
        elif choice == "4":
            save_tasks()
            logging.info("User exited and tasks saved.")
            print("Tasks saved. Goodbye!")
            break
        else:
            logging.warning("Invalid menu choice: %s", choice)
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    menu()
