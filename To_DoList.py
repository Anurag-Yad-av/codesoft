from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task = input_field.get()
    if not task:
        messagebox.showinfo('Error', 'Task field is empty.')
    else:
        task_list_data.append(task)
        cursor.execute('INSERT INTO tasks VALUES (?)', (task,))
        update_task_list()
        input_field.delete(0, 'end')

def update_task_list():
    task_listbox.delete(0, 'end')
    for task in task_list_data:
        task_listbox.insert('end', task)

def remove_task():
    try:
        selected_task = task_listbox.get(task_listbox.curselection())
        if selected_task in task_list_data:
            task_list_data.remove(selected_task)
            update_task_list()
            cursor.execute('DELETE FROM tasks WHERE title = ?', (selected_task,))
            conn.commit()
    except:
        messagebox.showinfo('Error', 'No task selected for deletion.')

def remove_all_tasks():
    confirm = messagebox.askyesno('Delete All', 'Are you sure you want to delete all tasks?')
    if confirm:
        task_list_data.clear()
        cursor.execute('DELETE FROM tasks')
        update_task_list()

def exit_app():
    print(task_list_data)
    root.destroy()

def fetch_tasks():
    task_list_data.clear()
    for row in cursor.execute('SELECT title FROM tasks'):
        task_list_data.append(row[0])

if __name__ == "__main__":
    root = Tk()
    root.title("To-Do List")
    root.geometry("665x400+550+250")
    root.resizable(0, 0)
    root.configure(bg="#B5E5CF")

    conn = sql.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

    task_list_data = []

    container = Frame(root, bg="#8EE5EE")
    container.pack(side="top", expand=True, fill="both")

    Label(container, text="TO-DO LIST\nEnter the Task Title:",
          font=("Arial", 14, "bold"),
          bg="#8EE5EE", fg="#FF6103").place(x=20, y=30)

    input_field = Entry(container, font=("Arial", 14), width=42, fg="black", bg="white")
    input_field.place(x=180, y=30)

    Button(container, text="Add", width=15, bg='#04AC0D',
           font=("Arial", 14, "bold"), command=add_task).place(x=18, y=80)

    Button(container, text="Remove", width=15, bg='#D4AC0D',
           font=("Arial", 14, "bold"), command=remove_task).place(x=240, y=80)

    Button(container, text="Delete All", width=15, bg='#D4AC0D',
           font=("Arial", 14, "bold"), command=remove_all_tasks).place(x=460, y=80)

    Button(container, text="Exit", width=52, bg='#D4AC0D',
           font=("Arial", 14, "bold"), command=exit_app).place(x=17, y=330)

    task_listbox = Listbox(container, width=70, height=9, font="bold", selectmode='SINGLE',
                           bg="WHITE", fg="BLACK", selectbackground="#FF8C00", selectforeground="BLACK")
    task_listbox.place(x=17, y=140)

    fetch_tasks()
    update_task_list()
    root.mainloop()

    conn.commit()
    cursor.close()