import tkinter as tk

def on_click(event):
    button_text = event.widget.cget("text")
    if button_text == "=":
        try:
            result = str(eval(display.get()))
            display_var.set(result)
        except Exception:
            display_var.set("Error")
    elif button_text == "C":
        display_var.set("")
    else:
        display_var.set(display_var.get() + button_text)

# Initialize main window
window = tk.Tk()
window.geometry("300x400")
window.title("Simple Calculator")

# Entry field for displaying input and results
display_var = tk.StringVar()
display = tk.Entry(window, textvar=display_var, font="Arial 20")
display.pack(fill=tk.BOTH, ipadx=8, pady=10, padx=10)

# Frame to hold all buttons
button_container = tk.Frame(window)
button_container.pack()

# Button layout
button_labels = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"]
]

# Creating button rows
for label_row in button_labels:
    row_frame = tk.Frame(button_container)
    row_frame.pack(expand=True, fill='both')
    for label in label_row:
        button = tk.Button(row_frame, text=label, font="Arial 15", height=2, width=4)
        button.pack(side='left', expand=True, fill='both', padx=2, pady=2)
        button.bind("<Button-1>", on_click)

window.mainloop()