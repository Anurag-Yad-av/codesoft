import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

# Ensure the database and table exist
with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
    db.commit()

class PasswordApp:
    def __init__(self, window):
        self.window = window
        self.username_var = StringVar()
        self.length_var = IntVar()
        self.password_var = StringVar()

        window.title('Password Generator')
        window.geometry('660x500')
        window.config(bg='#FF8000')
        window.resizable(False, False)

        Label(text=":PASSWORD GENERATOR:", fg='darkblue', bg='#FF8000',
              font='arial 20 bold underline').grid(row=0, column=1)

        Label(text="", bg='#FF8000').grid(row=1, column=0, columnspan=2)

        Label(text="Enter User Name:", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=2, column=0)
        self.username_input = Entry(textvariable=self.username_var, font='times 15', bd=6, relief='ridge')
        self.username_input.grid(row=2, column=1)
        self.username_input.focus_set()

        Label(text="", bg='#FF8000').grid(row=3, column=0)

        Label(text="Enter Password Length:", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=4, column=0)
        self.length_input = Entry(textvariable=self.length_var, font='times 15', bd=6, relief='ridge')
        self.length_input.grid(row=4, column=1)

        Label(text="", bg='#FF8000').grid(row=5, column=0)

        Label(text="Generated Password:", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=6, column=0)
        self.password_display = Entry(textvariable=self.password_var, font='times 15', bd=6,
                                      relief='ridge', fg='#DC143C')
        self.password_display.grid(row=6, column=1)

        Label(text="", bg='#FF8000').grid(row=7, column=0)

        Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1,
               font='Verdana 15 bold', fg='#68228B', bg='#BCEE68',
               command=self.generate_password).grid(row=8, column=1)

        Label(text="", bg='#FF8000').grid(row=9, column=0)

        Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1,
               font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0',
               command=self.accept_entry).grid(row=10, column=1)

        Label(text="", bg='#FF8000').grid(row=11, column=0)

        Button(text="RESET", bd=3, relief='solid', padx=1, pady=1,
               font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0',
               command=self.reset_fields).grid(row=12, column=1)

    def generate_password(self):
        upper = list(string.ascii_uppercase)
        lower = list(string.ascii_lowercase)
        symbols = list("@#%&()\"?!")
        digits = list(string.digits)

        username = self.username_input.get()
        length_input = self.length_input.get()

        if not username:
            messagebox.showerror("Error", "Name cannot be empty")
            return
        if not username.isalpha():
            messagebox.showerror("Error", "Name must be letters only")
            self.username_input.delete(0, END)
            return

        try:
            length = int(length_input)
            if length < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters long")
                return
        except ValueError:
            messagebox.showerror("Error", "Password length must be a number")
            return

        self.password_display.delete(0, END)

        num_upper = random.randint(1, length - 3)
        num_lower = random.randint(1, length - 2 - num_upper)
        num_sym = random.randint(1, length - 1 - num_upper - num_lower)
        num_digit = length - num_upper - num_lower - num_sym

        password_parts = (
            random.sample(upper, num_upper) +
            random.sample(lower, num_lower) +
            random.sample(symbols, num_sym) +
            random.sample(digits, num_digit)
        )
        random.shuffle(password_parts)
        final_password = "".join(password_parts)
        self.password_display.insert(0, final_password)

    def accept_entry(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE Username = ?", [self.username_var.get()])

            if cursor.fetchall():
                messagebox.showerror("Username Exists", "Please use another username")
            else:
                cursor.execute("INSERT INTO users(Username, GeneratedPassword) VALUES(?, ?)",
                               (self.username_var.get(), self.password_var.get()))
                db.commit()
                messagebox.showinfo("Success!", "Password saved successfully")

    def reset_fields(self):
        self.username_input.delete(0, END)
        self.length_input.delete(0, END)
        self.password_display.delete(0, END)

if __name__ == '__main__':
    root = Tk()
    PasswordApp(root)
    root.mainloop()