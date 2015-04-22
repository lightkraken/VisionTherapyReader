from tkinter import *
import tkinter.ttk
from . import cnfg

class Paster(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, padx=6, pady=6)

        self.focus()
        self.parent = args[0]

        self.text_box = Text(self, wrap="word")

        self.scroll = tkinter.ttk.Scrollbar(self, orient=VERTICAL, command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=self.scroll.set)

        self.button_frame = tkinter.ttk.Frame(self)
        self.finished_button = tkinter.ttk.Button(self.button_frame, text="Finished", takefocus=False, command=self.enter_text)
        self.cancel_button = tkinter.ttk.Button(self.button_frame, text="Cancel", takefocus=False, command=self.destroy)
        self.blank = tkinter.ttk.Label(self.button_frame, text="   ")
        self.finished_button.grid(row=0, column=2)
        self.cancel_button.grid(row=0, column=1, padx=(0,6))
        self.blank.grid(row=0, column=0)

        self.text_box.grid(row=0, column=0, sticky="NSEW")
        self.scroll.grid(row=0, column=1, sticky="NS")
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky="E", pady=(9,0))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.geometry('300x300')

        self.paste_menu = Menu(self)
        self.paste_menu.add_command(label="Paste", command=lambda: self.text_box.event_generate("<<Paste>>"))
        self.bind('<3>', lambda e: self.paste_menu.post(e.x_root, e.y_root))

    def enter_text(self):
        text = self.text_box.get("1.0", END)
        cnfg.TEXT = cnfg.text_splitter(text, 3000, " ")
        cnfg.TEXT_INDEX = 0
        self.parent.refresh_all()
        self.destroy()

