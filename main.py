import json
tasks = []
def load_tasks(filename="tasks.json"):
    global tasks
    try:
        with open(filename, "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []

def save_tasks(filename="tasks.json"):
    with open(filename, "w") as f:
        json.dump(tasks, f)

PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3}

def load_tasks(filename="tasks.json"):
    global tasks
    try:
        with open(filename, "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []

def save_tasks(filename="tasks.json"):
    with open(filename, "w") as f:
        json.dump(tasks, f)

def add_task(task, due_date=None, priority="medium"):
    tasks.append({"task": task, "done": False, "due_date": due_date, "priority": priority})

def list_tasks():
    if not tasks:
        print("No tasks found.")
        return
    # Sort tasks by priority (high, medium, low)
    sorted_tasks = sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.get("priority", "medium"), 2))
    for i, t in enumerate(sorted_tasks, start=1):
        status = "✓" if t["done"] else "✗"
        due = f" (Due: {t['due_date']})" if t.get("due_date") else ""
        priority = t.get("priority", "medium").capitalize()
        print(f"{i}. [{status}] {t['task']}{due} [Priority: {priority}]")

def mark_done(task_number):
    # Mark done in the sorted list, so get the sorted index
    sorted_tasks = sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.get("priority", "medium"), 2))
    if 1 <= task_number <= len(sorted_tasks):
        # Find the original index in the tasks list
        task_to_mark = sorted_tasks[task_number - 1]
        orig_index = tasks.index(task_to_mark)
        tasks[orig_index]["done"] = True
        print(f"Task {task_number} marked as done.")
    else:
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
                print("Task added.")
            else:
                print("Empty task not added.")
        elif choice == "3":
            list_tasks()
            try:
                num = int(input("Enter task number to mark done: ").strip())
                mark_done(num)
            except ValueError:
                print("Invalid input, please enter a number.")
        elif choice == "4":
            save_tasks()
            print("Tasks saved. Goodbye!")
            save_tasks()
            print("Tasks saved.")
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    menu()
