import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import colorchooser
import tkinter.scrolledtext as ScrolledText
from functools import partial

"""
TODO:
- spell check
- config file for settings?
- add filename to windows
"""

class MainApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Main Frame settings
        self.parent.title("Text Editor")
        self.parent.rowconfigure(0, minsize=800, weight=1)
        self.parent.columnconfigure(1, minsize=700, weight=1)
        # self.parent.attributes("-fullscreen", True)

        #Components
        self.txt_area = ScrolledText.ScrolledText()
        self.txt_area.config(highlightbackground="black", highlightcolor="#C12216", highlightthickness="2")
        self.second_txt_area = ScrolledText.ScrolledText()
        self.second_txt_area.config(highlightbackground="black", highlightcolor="#C12216", highlightthickness="2")
        self.fr_buttons = tk.Frame(self.parent, width="100", background="#DCDCDC")
        self.btn_open = tk.Button(self.fr_buttons, text="Open", command=partial(self.open_check_window, self.open_file))
        self.btn_save = tk.Button(self.fr_buttons, text="Save As...", command=partial(self.open_check_window, self.save_file))
        self.btn_color = tk.Button(self.fr_buttons, text="Background Color", command=self.change_bg)
        self.btn_fullscreen = tk.Button(self.fr_buttons, text="Fullscreen", command=self.toggle_fullscreen)
        self.btn_hide = tk.Button(self.fr_buttons, text="Hide Menu", command=self.close_menu)
        self.btn_close = tk.Button(self.fr_buttons, text="Close", command=self.quit_program)
        #Collapsed menu
        self.collapse_menu = tk.Frame(self.parent)
        self.menu_icon = tk.PhotoImage(file="menu.png")
        self.btn_show_menu = tk.Button(self.collapse_menu, image=self.menu_icon, text="Show menu", command=self.open_menu)

        #Add components
        self.txt_area.grid(row=0, column=1, sticky='nwse')
        self.second_txt_area.grid(row=0, column=2, sticky='nsew')
        self.fr_buttons.grid(row=0, column=0, sticky='ns')
        self.btn_open.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        self.btn_color.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        self.btn_fullscreen.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
        self.btn_hide.grid(row=4, column=0, sticky='ew', padx=5, pady=5)
        self.btn_close.grid(row=5, column=0, sticky='ew', padx=5, pady=5)


        #Key Bindings
        self.parent.bind("<Control -q>", lambda event: self.quit_program())
        self.parent.bind("<Control -s>", lambda event: self.open_check_window(self.save_file))
        self.parent.bind("<Control -o>", lambda event: self.open_check_window(self.open_file))
        self.parent.bind("<Control -f>", lambda event: self.toggle_fullscreen())

    def quit_program(self):
        self.parent.destroy()

    def open_check_window(self, win_type):
        #Toplevel window to check which window to open in/save from
        self.open_check = tk.Toplevel()
        self.open_check.geometry('300x100')
        self.open_check.title("Which window?")
        self.msg = tk.Message(self.open_check, width=250, text="Which screen would you like to use?")
        self.msg.pack(side=tk.TOP, pady=15)
        self.left_btn = tk.Button(self.open_check, text="Left Window", command=partial(win_type, self.txt_area))
        self.right_btn = tk.Button(self.open_check, text="Right Window", command=partial(win_type, self.second_txt_area))
        self.cancel_btn = tk.Button(self.open_check, text="Cancel", command=self.open_check.destroy)
        self.left_btn.pack(side=tk.LEFT, padx=20)
        self.right_btn.pack(side=tk.LEFT)
        self.cancel_btn.pack(side=tk.LEFT, padx=20)
        self.open_check.mainloop()

    def open_file(self, use_window):
        """Open a file for editing."""
        self.open_check.destroy() #Toplevel window doesn't close itself
        self.filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not self.filepath:
            return
        use_window.delete("1.0", tk.END)
        with open(self.filepath, "r") as input_file:
            text = input_file.read()
            use_window.insert(tk.END, text)
        # self.parent.title(f"Text Editor - {self.filepath}")

    def save_file(self, use_window):
        """Save the current file as a new file."""
        self.open_check.destroy() #Toplevel window doesn't close itself
        self.filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if not self.filepath:
            return
        with open(self.filepath, "w") as output_file:
            text = use_window.get("1.0", tk.END)
            output_file.write(text)
        # self.parent.title(f"Text Editor - {self.filepath}")

    def change_bg(self):
        (rgb, hex) = colorchooser.askcolor()
        fg = "black"
        lum = (rgb[0]*0.299 + rgb[1]*0.587 + rgb[2]*0.114) / 256
        if lum < .5:
            fg = "white"
        else:
            fg = "black"
        self.txt_area.config(background=hex, foreground=fg)
        self.second_txt_area.config(background=hex, foreground=fg)
        self.fr_buttons.config(background=hex)

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
