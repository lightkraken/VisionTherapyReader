from Tkinter import *
import ttk
import tkColorChooser
from files import cnfg

class RBAdjustMenu(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.focus()
        self.resizable(0,0)

        self.parent = parent

        self.get_color_values()

        # example frame
        self.example_frame = ttk.Frame(self)

        # bar example
        self.bar_example = Canvas(self.example_frame, width=200, height=65, background=self.color9)

        self.bar_list = []
        self.create_bars()
        self.create_bar_text()

        # color example
        self.color_example_frame = ttk.Frame(self.example_frame, width=200, height=65)
        self.color_example = Text(self.color_example_frame, background=self.color8, font=("Helvetica", 36, "bold"), cursor="arrow")
        self.create_tags()
        self.color_example.insert("1.0", "ef", "letters2")
        self.color_example.insert("1.0", "cd", "lettersvis")
        self.color_example.insert("1.0", " Ab", "letters1")
        self.color_example.configure(state=DISABLED)
        self.color_example.grid(column=0, row=0)

        self.bar_example.grid(row=0, column=0, pady=(0,5))
        self.color_example_frame.grid_propagate(False)
        self.color_example_frame.grid(row=1, column=0, pady=(5,0))

        # options frame
        self.options_frame = ttk.Frame(self, padding=6)

        self.red_label1 = ttk.Label(self.options_frame, text="Bar reader\nColor reader")
        self.red_label2 = ttk.Label(self.options_frame, text="Bar 1\nText 1")
        self.red_sep = ttk.Label(self.options_frame, text=" : \n : ")
        self.red_button = Button(self.options_frame, background=self.color6, text="    ", command=self.red_click)

        self.blue_label1 = ttk.Label(self.options_frame, text="Bar reader\nColor reader")
        self.blue_label2 = ttk.Label(self.options_frame, text="Bar 2\nText 2")
        self.blue_sep = ttk.Label(self.options_frame, text=" : \n : ")
        self.blue_button = Button(self.options_frame, background=self.color7, text="    ", command=self.blue_click)

        self.black_label1 = ttk.Label(self.options_frame, text="Bar reader\nColor reader")
        self.black_label2 = ttk.Label(self.options_frame, text="Text\nBackground")
        self.black_sep = ttk.Label(self.options_frame, text=" : \n : ")
        self.black_button = Button(self.options_frame, background=self.color8, text="    ", command=self.black_click)

        self.gray_label1 = ttk.Label(self.options_frame, text="Bar reader\nColor reader")
        self.gray_label2 = ttk.Label(self.options_frame, text="Background\n ")
        self.gray_sep = ttk.Label(self.options_frame, text=" : \n : ")
        self.gray_button = Button(self.options_frame, background=self.color9, text="    ", command=self.gray_click)

        self.pink_label1 = ttk.Label(self.options_frame, text="Bar reader\nColor reader")
        self.pink_label2 = ttk.Label(self.options_frame, text=" \nAnchor Text")
        self.pink_sep = ttk.Label(self.options_frame, text=" : \n : ")
        self.pink_button = Button(self.options_frame, background=self.color10, text="    ", command=self.pink_click)

        self.ok_button = ttk.Button(self.options_frame, text="OK", command=self.ok_click)
        self.cancel_button = ttk.Button(self.options_frame, text="Cancel", command=self.cancel_click)

        self.red_button.grid(row=1, column=0, padx=(9,2))
        self.red_label1.grid(row=1, column=1, sticky="E")
        self.red_sep.grid(row=1, column=2, sticky="NS")
        self.red_label2.grid(row=1, column=3, sticky="W")

        self.red_space = ttk.Label(self.options_frame, text=" ", font="Times 3")
        self.red_space.grid(row=2, column=0)

        self.blue_button.grid(row=1, column=4, padx=(18,2))
        self.blue_label1.grid(row=1, column=5, sticky="E")
        self.blue_sep.grid(row=1, column=6, sticky="NS")
        self.blue_label2.grid(row=1, column=7, sticky="W")

        self.black_button.grid(row=3, column=0, padx=(9,2))
        self.black_label1.grid(row=3, column=1, sticky="E")
        self.black_sep.grid(row=3, column=2, sticky="NS")
        self.black_label2.grid(row=3, column=3, sticky="W")

        self.gray_button.grid(row=3, column=4, padx=(18,2))
        self.gray_label1.grid(row=3, column=5, sticky="E")
        self.gray_sep.grid(row=3, column=6, sticky="NS")
        self.gray_label2.grid(row=3, column=7, sticky="W", padx=(0,9))

        self.gray_space = ttk.Label(self.options_frame, text=" ", font="Times 3")
        self.gray_space.grid(row=4, column=0)

        self.pink_button.grid(row=5, column=0, padx=(9,2))
        self.pink_label1.grid(row=5, column=1, sticky="E")
        self.pink_sep.grid(row=5, column=2, sticky="NS")
        self.pink_label2.grid(row=5, column=3, sticky="W")

        self.cancel_button.grid(row=6, column=4, columnspan=2, pady=(12,0), sticky="E")
        self.ok_button.grid(row=6, column=6, columnspan=2, pady=(12,0))

        self.instructions_label = ttk.Label(self.options_frame, text="Click on a color button to choose a new color.")
        self.instructions_label.grid(row=0, column=0, columnspan=8, pady=(6,9))

        self.example_frame.grid(column=0, row=0, padx=(9,0))
        self.options_frame.grid(column=1, row=0)

    def get_color_values(self):
        self.color6 = cnfg.COLOR6
        self.color7 = cnfg.COLOR7
        self.color8 = cnfg.COLOR8
        self.color9 = cnfg.COLOR9
        self.color10 = cnfg.COLOR10

    def set_color_values(self):
        cnfg.COLOR6 = self.color6
        cnfg.COLOR7 = self.color7
        cnfg.COLOR8 = self.color8
        cnfg.COLOR9 = self.color9
        cnfg.COLOR10 = self.color10

    def create_bars(self):
        for item in self.bar_list:
            self.bar_example.delete(item)
        redblue = 0
        fill = ""
        for num in range(0, 200, 20+20):
            if redblue % 2 == 0:
                fill = self.color6
            else:
                fill = self.color7
            self.bar_list.append(self.bar_example.create_rectangle(num,0,num+20, 70, fill=fill, outline=""))
            redblue += 1

    def create_bar_text(self):
        try:
            self.bar_example.delete(self.bar_text)
        except:
            pass
        self.bar_text = self.bar_example.create_text(100, 33, anchor="center")
        self.bar_example.itemconfig(self.bar_text, text="Abcdef")
        self.bar_example.itemconfig(self.bar_text, font=("Helvetica", 36, "bold"), fill=self.color8)

    def create_tags(self):
        self.color_example.tag_configure("letters1", foreground=self.color6)
        self.color_example.tag_configure("letters2", foreground=self.color7)
        self.color_example.tag_configure("lettersvis", foreground=self.color10)

    def refresh_examples(self):
        self.bar_example.configure(background=self.color9)
        self.create_bars()
        self.create_bar_text()
        self.color_example.configure(background=self.color8)
        self.create_tags()

    def red_click(self):
        (rgb, hx) = tkColorChooser.askcolor(parent=self)
        if hx is not None:
            self.color6 = hx
            self.red_button.configure(background=self.color6)
            self.refresh_examples()

    def blue_click(self):
        (rgb, hx) = tkColorChooser.askcolor(parent=self)
        if hx is not None:
            self.color7 = hx
            self.blue_button.configure(background=self.color7)
            self.refresh_examples()

    def black_click(self):
        (rgb, hx) = tkColorChooser.askcolor(parent=self)
        if hx is not None:
            self.color8 = hx
            self.black_button.configure(background=self.color8)
            self.refresh_examples()

    def gray_click(self):
        (rgb, hx) = tkColorChooser.askcolor(parent=self)
        if hx is not None:
            self.color9 = hx
            self.gray_button.configure(background=self.color9)
            self.refresh_examples()

    def pink_click(self):
        (rgb, hx) = tkColorChooser.askcolor(parent=self)
        if hx is not None:
            self.color10 = hx
            self.pink_button.configure(background=self.color10)
            self.refresh_examples()

    def ok_click(self):
        self.set_color_values()
        self.parent.parent.content.palette_click()
        self.destroy()

    def cancel_click(self):
        self.destroy()