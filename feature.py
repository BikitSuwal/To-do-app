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

def add_task(task, due_date=None):
    tasks.append({"task": task, "done": False, "due_date": due_date})

def list_tasks():
    if not tasks:
        print("No tasks found.")
        return
    for i, t in enumerate(tasks, start=1):
        status = "✓" if t["done"] else "✗"
        due = f" (Due: {t['due_date']})" if t.get("due_date") else ""
        print(f"{i}. [{status}] {t['task']}{due}")

def mark_done(task_number):
    if 1 <= task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        print(f"Task {task_number} marked as done.")
    else:
        print("Invalid task number")

def menu():
    load_tasks()
    while True:
        print("\nTo-Do List Menu:")
        print("1. List tasks")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Save & Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            list_tasks()
        elif choice == "2":
            task = input("Enter new task: ").strip()
            if task:
                due_date = input("Enter due date (optional, e.g. 2025-07-01): ").strip()
                due_date = due_date if due_date else None
                add_task(task, due_date)
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
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    menu()
