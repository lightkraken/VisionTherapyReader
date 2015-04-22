from tkinter import *
import tkinter.ttk
import tkinter.colorchooser
from files import cnfg

class AdjustMenu(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, padx=9, pady=9)

        self.focus()

        self.resizable(0,0)
        self.parent = args[0]

        self.instructions_label = tkinter.ttk.Label(self, text="Click on the colors you wish to adjust.", padding=(0,6,0,9))
        self.calibrate_purpteal_button = tkinter.ttk.Button(self, text="Purple & Teal", takefocus=False, command=self.parent.adjust_purpleteal)
        self.calibrate_redblue_button = tkinter.ttk.Button(self, text="Red & Blue", takefocus=False, command=self.parent.adjust_redblue)
        self.finished_button = tkinter.ttk.Button(self, text="Finished", takefocus=False, command=self.destroy)
        self.blank_label = tkinter.ttk.Label(self, text=" ")

        self.instructions_label.grid(row=0, column=0, columnspan=2)
        self.calibrate_purpteal_button.grid(row=1, column=0)
        self.calibrate_redblue_button.grid(row=1, column=1)
        self.blank_label.grid(row=2, column=0, columnspan=2)
        self.finished_button.grid(row=3, column=0, columnspan=2)

class PTAdjustMenu(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.focus()
        self.resizable(0,0)

        self.parent = parent

        self.get_color_values()

        # example frame
        self.example_frame = tkinter.ttk.Frame(self)

        # bar example
        self.bar_example = Canvas(self.example_frame, width=200, height=65, background=self.color4)

        self.bar_list = []
        self.create_bars()
        self.create_bar_text()

        # color example
        self.color_example_frame = tkinter.ttk.Frame(self.example_frame, width=200, height=65)
        self.color_example = Text(self.color_example_frame, background=self.color3, font=("Helvetica", 36, "bold"), cursor="arrow")
        self.create_tags()
        self.color_example.insert("1.0", "ef", "letters2")
        self.color_example.insert("1.0", "cd", "lettersvis")
        self.color_example.insert("1.0", " Ab", "letters1")
        self.color_example.configure(state=DISABLED)
        self.color_example.grid(column=0, row=0)

        self.bar_example.grid(row=0, column=0, pady=(0,2))
        self.color_example_frame.grid_propagate(False)
        self.color_example_frame.grid(row=1, column=0, pady=(2,0))

        # options frame
        self.options_frame = tkinter.ttk.Frame(self, padding=6)

        self.purple_label1 = tkinter.ttk.Label(self.options_frame, text="Bar reader\nColor reader")
        self.purple_label2 = tkinter.ttk.Label(self.options_frame, text="Bar 1\nText 1")
        self.purple_sep = tkinter.ttk.Label(self.options_frame, text=" : \n : ")
        self.purple_button = Button(self.options_frame, background=self.color1, text="    ", command=self.purple_click)

        self.teal_label1 = tkinter.ttk.Label(self.options_frame, text="Bar reader\nColor reader")
        self.teal_label2 = tkinter.ttk.Label(self.options_frame, text="Bar 2\nText 2")
        self.teal_sep = tkinter.ttk.Label(self.options_frame, text=" : \n : ")
        self.teal_button = Button(self.options_frame, background=self.color2, text="    ", command=self.teal_click)

        self.gray_label1 = tkinter.ttk.Label(self.options_frame, text="Bar reader\nColor reader")
        self.gray_label2 = tkinter.ttk.Label(self.options_frame, text="Text\nBackground")
        self.gray_sep = tkinter.ttk.Label(self.options_frame, text=" : \n : ")
        self.gray_button = Button(self.options_frame, background=self.color3, text="    ", command=self.gray_click)

        self.black_label1 = tkinter.ttk.Label(self.options_frame, text="Bar reader\nColor reader")
        self.black_label2 = tkinter.ttk.Label(self.options_frame, text="Background\nAnchor Text")
        self.black_sep = tkinter.ttk.Label(self.options_frame, text=" : \n : ")
        self.black_button = Button(self.options_frame, background=self.color4, text="    ", command=self.black_click)

        self.ok_button = tkinter.ttk.Button(self.options_frame, text="OK", command=self.ok_click)
        self.cancel_button = tkinter.ttk.Button(self.options_frame, text="Cancel", command=self.cancel_click)

        self.purple_button.grid(row=1, column=0, padx=(9,2))
        self.purple_label1.grid(row=1, column=1, sticky="E")
        self.purple_sep.grid(row=1, column=2, sticky="NS")
        self.purple_label2.grid(row=1, column=3, sticky="W")

        self.purple_space = tkinter.ttk.Label(self.options_frame, text=" ", font="Times 3")
        self.purple_space.grid(row=2, column=0)

        self.teal_button.grid(row=1, column=4, padx=(18,2))
        self.teal_label1.grid(row=1, column=5, sticky="E")
        self.teal_sep.grid(row=1, column=6, sticky="NS")
        self.teal_label2.grid(row=1, column=7, sticky="W")

        self.gray_button.grid(row=3, column=0, padx=(9,2))
        self.gray_label1.grid(row=3, column=1, sticky="E")
        self.gray_sep.grid(row=3, column=2, sticky="NS")
        self.gray_label2.grid(row=3, column=3, sticky="W")

        self.black_button.grid(row=3, column=4, padx=(18,2))
        self.black_label1.grid(row=3, column=5, sticky="E")
        self.black_sep.grid(row=3, column=6, sticky="NS")
        self.black_label2.grid(row=3, column=7, sticky="W", padx=(0,9))

        self.cancel_button.grid(row=4, column=4, columnspan=2, pady=(12,0), sticky="E")
        self.ok_button.grid(row=4, column=6, columnspan=2, pady=(12,0))

        self.instructions_label = tkinter.ttk.Label(self.options_frame, text="Click on a color button to choose a new color.")
        self.instructions_label.grid(row=0, column=0, columnspan=8, pady=(6,9))

        self.example_frame.grid(column=0, row=0, padx=(9,0))
        self.options_frame.grid(column=1, row=0)

    def get_color_values(self):
        self.color1 = cnfg.COLOR1
        self.color2 = cnfg.COLOR2
        self.color3 = cnfg.COLOR3
        self.color4 = cnfg.COLOR4

    def set_color_values(self):
        cnfg.COLOR1 = self.color1
        cnfg.COLOR2 = self.color2
        cnfg.COLOR3 = self.color3
        cnfg.COLOR4 = self.color4
        cnfg.COLOR5 = self.color4

    def create_bars(self):
        for item in self.bar_list:
            self.bar_example.delete(item)
        redblue = 0
        fill = ""
        for num in range(0, 200, 20+20):
            if redblue % 2 == 0:
                fill = self.color1
            else:
                fill = self.color2
            self.bar_list.append(self.bar_example.create_rectangle(num,0,num+20, 70, fill=fill, outline=""))
            redblue += 1

    def create_bar_text(self):
        try:
            self.bar_example.delete(self.bar_text)
        except:
            pass
        self.bar_text = self.bar_example.create_text(100, 33, anchor="center")
        self.bar_example.itemconfig(self.bar_text, text="Abcdef")
        self.bar_example.itemconfig(self.bar_text, font=("Helvetica", 36, "bold"), fill=self.color3)

    def create_tags(self):
        self.color_example.tag_configure("letters1", foreground=self.color1)
        self.color_example.tag_configure("letters2", foreground=self.color2)
        self.color_example.tag_configure("lettersvis", foreground=self.color4)

    def refresh_examples(self):
        self.bar_example.configure(background=self.color4)
        self.create_bars()
        self.create_bar_text()
        self.color_example.configure(background=self.color3)
        self.create_tags()

    def purple_click(self):
        (rgb, hx) = tkinter.colorchooser.askcolor(parent=self)
        if hx is not None:
            self.color1 = hx
            self.purple_button.configure(background=self.color1)
            self.refresh_examples()

    def teal_click(self):
        (rgb, hx) = tkinter.colorchooser.askcolor(parent=self)
        if hx is not None:
            self.color2 = hx
            self.teal_button.configure(background=self.color2)
            self.refresh_examples()

    def gray_click(self):
        (rgb, hx) = tkinter.colorchooser.askcolor(parent=self)
        if hx is not None:
            self.color3 = hx
            self.gray_button.configure(background=self.color3)
            self.refresh_examples()

    def black_click(self):
        (rgb, hx) = tkinter.colorchooser.askcolor(parent=self)
        if hx is not None:
            self.color4 = hx
            self.black_button.configure(background=self.color4)
            self.refresh_examples()

    def ok_click(self):
        self.set_color_values()
        self.parent.parent.content.palette_click()
        self.destroy()

    def cancel_click(self):
        self.destroy()