#to do app feature/task

tasks = []

def add_task(task):
    tasks.append({"task": task, "done": False})

def list_tasks():
    if not tasks:
        print("No tasks found.")
        return
    for i, t in enumerate(tasks, start=1):
        status = "✓" if t["done"] else "✗"
        print(f"{i}. [{status}] {t['task']}")

def mark_done(task_number):
    if 1 <= task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        print(f"Task {task_number} marked as done.")
    else:
        print("Invalid task number")

def menu():
    while True:
        print("\nTo-Do List Menu:")
        print("1. List tasks")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            list_tasks()
        elif choice == "2":
            task = input("Enter new task: ").strip()
            if task:
                add_task(task)
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
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    menu()
