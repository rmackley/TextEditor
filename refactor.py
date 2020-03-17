import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.scrolledtext as ScrolledText

"""
TODO:
- spell check
- encrypt
- clean up this code. it's a mess
- config file for settings?
- add keybinding for close?
"""

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Simple Text Editor - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")

def change_bg():
    col = var.get()
    if col == "white":
        txt_edit.config(background=col, foreground="black")
    else:
        txt_edit.config(background=col, foreground="white")
        fr_buttons.config(background=col)


def toggle_fullscreen():
    if window.attributes()[7] == 1:
        window.attributes("-fullscreen", False)
    else:
        window.attributes("-fullscreen", True)

def close_menu():
    fr_buttons.grid_forget()
    collapse_menu.grid(row=0, column=0, sticky='ns')
    show_menu_btn.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

def open_menu():
    collapse_menu.grid_forget()
    fr_buttons.grid(row=0, column=0, sticky='ns')

window = tk.Tk()
window.title("Simple Text Editor")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)
window.attributes("-fullscreen", True)

txt_edit = ScrolledText.ScrolledText()
fr_buttons = tk.Frame(window)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)
btn_change = tk.Button(fr_buttons, text="Change color", command=change_bg)
btn_fullscreen = tk.Button(fr_buttons, text="Fullscreen", command=toggle_fullscreen)
btn_close = tk.Button(fr_buttons, text="Close", command=window.destroy)
btn_hide = tk.Button(fr_buttons, text="Hide Menu", command=close_menu)


var = tk.StringVar(window)
var.set("Background color")
option = tk.OptionMenu(fr_buttons, var, "black", "white", "blue", "red")

btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
option.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
btn_change.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
btn_fullscreen.grid(row=4, column=0, sticky='ew', padx=5, pady=5)
btn_close.grid(row=5, column=0, sticky='ew', padx=5, pady=5)
btn_hide.grid(row=6, column=0, sticky='ew', padx=5, pady=5)
fr_buttons.grid(row=0, column=0, sticky='ns')
txt_edit.grid(row=0, column=1, sticky='nwse')

collapse_menu = tk.Frame(window)
#img from https://www.flaticon.com/authors/those-icons
menu_icon = tk.PhotoImage(file="menu.png")
show_menu_btn = tk.Button(collapse_menu, image=menu_icon, text="Show menu", command=open_menu)


window.mainloop()
