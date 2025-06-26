# 📝 To-Do List CLI App (with Logging)

A command-line Python application to manage your daily tasks efficiently.  
Features include task creation, marking as done, deletion, CSV export, and robust **logging** using Python's built-in `logging` module.

---

## 🚀 Features

- ✅ Add tasks with due dates and priorities (High, Medium, Low)
- 📋 View tasks sorted by priority
- ✔️ Mark tasks as done
- 🗑️ Delete tasks
- 📤 Export tasks to CSV
- 💾 Persistent storage using JSON
- 🪵 Logging of key actions to `todo_app.log` for monitoring/debugging

---

## 🛠️ Tech Stack

- Python 3.x
- Built-in libraries: `json`, `logging`, `csv`

---

## 📂 Project Structure

```

.
├── tasks.json             # JSON file for storing tasks (auto-created)
├── tasks\_export.csv       # Exported tasks in CSV format (optional)
├── todo\_app.log           # Logs for debugging and tracking actions
├── main\_script.py         # Main script
├── Test_main\_testing      # For automated testing of the program function (adding, removing, listing)
└── README.md              # You're reading this!

````
---

## 🧪 How to Use

### ▶️ Run the App

```Terminal
python main.py
````

### 📋 Menu Options

| Option | Action                             |
| ------ | ---------------------------------- |
| 1      | List all tasks sorted by priority  |
| 2      | Add a new task                     |
| 3      | Mark task as done                  |
| 4      | Save tasks & exit                  |
| 5      | Export tasks to `tasks_export.csv` |
| 6      | Delete a task                      |

---

## 🪵 Logging

The app uses Python's `logging` module to record operations and errors.

* Logs are saved in `todo_app.log`
* Log levels used: `INFO`, `WARNING`, `ERROR`
* Helps in debugging issues like invalid input, file loading problems, and invalid operations

**Example Log Entry:**

```
2025-06-25 15:03:21,734 - INFO - Added task: 'Finish project' with due date: '2025-07-01' and priority: 'high'
```

---

## 📦 Output Examples

### ✅ Task Display:

```
1. [✗] Finish project (Due: 2025-07-01) [Priority: High]
2. [✓] Buy groceries [Priority: Medium]
```

### 📤 Exported CSV:
**Output format:**

| Task           | Due Date   | Priority | Status   |
| -------------- | ---------- | -------- | -------- |
| Finish project | 2025-07-01 | high     | not done |
| Buy groceries  |            | medium   | done     |

---

## 🧩 Future Improvements

* Task editing support
* Tagging or categories
* GUI version (Tkinter or PyQT)
* Notification/reminder system

---

## Warning!!!

* changes may not save if you force close.
* Avoid directly editing `tasks.json`.

---
