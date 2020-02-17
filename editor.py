import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.scrolledtext as ScrolledText

"""
TODO:
- spell check
- encrypt
- config file for settings?
- add keybinding for close?
"""

class MainApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Main Frame settings
        self.parent.title("Text Editor")
        self.parent.rowconfigure(0, minsize=800, weight=1)
        self.parent.columnconfigure(1, minsize=800, weight=1)
        # self.parent.attributes("-fullscreen", True)

        #Components
        self.txt_area = ScrolledText.ScrolledText()
        self.fr_buttons = tk.Frame(self.parent, width="100")
        self.btn_open = tk.Button(self.fr_buttons, text="Open", command=self.open_file)
        self.btn_save = tk.Button(self.fr_buttons, text="Save As...", command=self.save_file)
        self.btn_change = tk.Button(self.fr_buttons, text="Change color", command=self.change_bg)
        self.btn_fullscreen = tk.Button(self.fr_buttons, text="Fullscreen", command=self.toggle_fullscreen)
        self.btn_close = tk.Button(self.fr_buttons, text="Close", command=self.parent.destroy)
        self.btn_hide = tk.Button(self.fr_buttons, text="Hide Menu", command=self.close_menu)
        self.collapse_menu = tk.Frame(self.parent)
        self.menu_icon = tk.PhotoImage(file="menu.png")
        self.btn_show_menu = tk.Button(self.collapse_menu, image=self.menu_icon, text="Show menu", command=self.open_menu)
        #Background color changing menu
        self.current_color = tk.StringVar(self.parent)
        self.current_color.set("Background color")
        self.option = tk.OptionMenu(self.fr_buttons, self.current_color, "black", "white", "blue", "red")

        #Add components
        self.txt_area.grid(row=0, column=1, sticky='nwse')
        self.fr_buttons.grid(row=0, column=0, sticky='ns')
        self.btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        self.option.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        self.btn_change.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
        self.btn_fullscreen.grid(row=4, column=0, sticky='ew', padx=5, pady=5)
        self.btn_close.grid(row=5, column=0, sticky='ew', padx=5, pady=5)
        self.btn_hide.grid(row=6, column=0, sticky='ew', padx=5, pady=5)

    def open_file(self):
        """Open a file for editing."""
        self.filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not self.filepath:
            return
        self.txt_area.delete("1.0", tk.END)
        with open(self.filepath, "r") as input_file:
            text = input_file.read()
            self.txt_area.insert(tk.END, text)
        self.parent.title(f"Text Editor - {self.filepath}")

    def save_file(self):
        """Save the current file as a new file."""
        self.filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not self.filepath:
            return
        with open(self.filepath, "w") as output_file:
            text = self.txt_area.get("1.0", tk.END)
            output_file.write(text)
        self.parent.title(f"Text Editor - {self.filepath}")

    def change_bg(self):
        self.color = self.current_color.get()
        if self.color == "white":
            self.txt_area.config(background=self.color, foreground="black")
        else:
            self.txt_area.config(background=self.color, foreground="white")
            self.fr_buttons.config(background=self.color)

    def toggle_fullscreen(self):
        if self.parent.attributes()[7] == 1:
            self.parent.attributes("-fullscreen", False)
        else:
            self.parent.attributes("-fullscreen", True)

    def close_menu(self):
        self.fr_buttons.grid_forget()
        self.collapse_menu.grid(row=0, column=0, sticky='ns')
        self.btn_show_menu.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

    def open_menu(self):
        self.collapse_menu.grid_forget()
        self.fr_buttons.grid(row=0, column=0, sticky='ns')

if __name__ == "__main__":
    root = tk.Tk()
    MainApp(root)
    root.mainloop()
