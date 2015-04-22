import random
from tkinter import *
import tkinter.ttk
from files import cnfg

class ColorReaderFrame(tkinter.ttk.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.ttk.Frame.__init__(self, *args, **kwargs)

        self.parent = args[0]

        # 1x2 grid
        # column width can grow in all cells
        # row 0 height cannot grow
        # row 1 height can grow
        # row 2 heigh cannot grow
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # text frame
        # placed at 0,0
        self.colorstextframe = ColorsTextFrame(self)
        self.colorstextframe.grid(column=0, row=0, sticky="NSEW")

        # bottom options frame
        # placed at 0,1
        self.colorsbottomoptionsframe = ColorsBottomOptionsFrame(self, padding=2)
        self.colorsbottomoptionsframe.grid(column=0, row=1, sticky="NSEW")

class ColorsTextFrame(tkinter.ttk.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.ttk.Frame.__init__(self, *args, **kwargs)

        self.parent = args[0]
        self.coloredtext = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self.coloredtext = Text(self, cursor='arrow')
        self.coloredtext.bind("<Button-1>", self.text_clicked)
        self.create_new_text()
        self.refresh_text()
        self.create_scrollbar()

        self.coloredtext.grid(column=0, row=0, sticky="NSEW")
        self.scroll.grid(column=1, row=0, sticky="NS")
        self.parent.parent.parent.geometry('{0}x{1}'.format(int(cnfg.SCREEN_WIDTH*.6), int(cnfg.SCREEN_HEIGHT*.6)))

    def text_clicked(self, *args):
        self.parent.parent.parent.focus()
        return("break")

    def create_scrollbar(self):
        self.scroll = tkinter.ttk.Scrollbar(self, orient=VERTICAL, command=self.coloredtext.yview)
        self.coloredtext.configure(yscrollcommand=self.scroll.set)

    def create_new_tags(self):
        self.coloredtext.tag_configure("letters1", foreground=cnfg.PALETTE[0])
        self.coloredtext.tag_configure("letters2", foreground=cnfg.PALETTE[1])
        self.coloredtext.tag_configure("lettersvis", foreground=cnfg.PALETTE[4])

    def create_new_text(self):
        self.coloredtext.configure(state='normal')
        self.coloredtext.delete('1.0', 'end')
        self.delete_tags()
        self.create_new_tags()
        self.coloredtext.configure(wrap="word")

        if cnfg.PATTERN == "Words":
            splitted = cnfg.TEXT[cnfg.TEXT_INDEX].split(" ")
            splitted_copy = []
            for item in splitted:
                if "\n" in item:
                    more_split = item.split("\n")
                    splitted_copy.append(more_split[0]+"\n")
                    for thang in more_split[1:-1]:
                        splitted_copy.append(thang+"\n")
                    splitted_copy.append(more_split[-1])
                else:
                    splitted_copy.append(item)

            if cnfg.VIS_COLOR == 0:
                if cnfg.ORDER == "Ordered":
                    i = 1
                    for item in reversed(splitted_copy):
                        if item == "\n":
                            tag = ""
                            item2append = item
                        elif i % 2 == 0:
                            tag = 'letters1'
                            i += 1
                            item2append = item+" "
                        else:
                            tag = 'letters2'
                            i += 1
                            item2append = item+" "
                        self.coloredtext.insert('1.0', item2append, tag)
                elif cnfg.ORDER == "Random":
                    for item in reversed(splitted_copy):
                        if item == "\n":
                            tag = ""
                            item2append = item
                        else:
                            tag = random.choice(['letters1', 'letters2'])
                            item2append = item+" "
                        self.coloredtext.insert('1.0', item2append, tag)
            elif cnfg.VIS_COLOR == 1:
                if cnfg.ORDER == "Ordered":
                    i = 1
                    for item in reversed(splitted_copy):
                        if item == "\n":
                            tag = ""
                            self.coloredtext.insert('1.0', item, tag)
                        else:
                            if i == 1:
                                tag = 'letters1'
                            elif i == 2:
                                tag = 'lettersvis'
                            elif i == 3:
                                tag = 'letters2'
                            elif i == 4:
                                tag = 'lettersvis'
                            i += 1
                            if i > 4: i = 1
                            self.coloredtext.insert('1.0', item+" ", tag)
                elif cnfg.ORDER == "Random":
                    for item in reversed(splitted_copy):
                        if item == "\n":
                            tag = ""
                            item2append = item
                        else:
                            tag = random.choice(['letters1', 'letters2', 'lettersvis'])
                            item2append = item+" "
                        self.coloredtext.insert('1.0', item2append, tag)

        elif cnfg.PATTERN == "Letters":
            self.coloredtext.insert('1.0', cnfg.TEXT[cnfg.TEXT_INDEX])

            if cnfg.VIS_COLOR == 0:
                if cnfg.ORDER == "Ordered":
                    i = 1
                    for line in range(1, int(self.coloredtext.index('end-1c').split('.')[0])+1):                      # for every line in the text
                        for char in range(0, int(self.coloredtext.index(str(line)+".end").split('.')[1])+1):          # for every char in the line
                            charlie = self.coloredtext.get("{0}.{1}".format(line,char))
                            if charlie == " " or charlie == "\n" or charlie == "\t":
                                pass
                            else:
                                if i % 2 == 0:
                                    self.coloredtext.tag_add("letters1", "{0}.{1}".format(line,char))
                                else:
                                    self.coloredtext.tag_add("letters2", "{0}.{1}".format(line,char))
                                i += 1
                elif cnfg.ORDER == "Random":
                    for line in range(1, int(self.coloredtext.index('end-1c').split('.')[0])+1):                      # for every line in the text
                        for char in range(0, int(self.coloredtext.index(str(line)+".end").split('.')[1])+1):          # for every char in the line
                            rand_color = random.randint(1,2)
                            if rand_color == 1:
                                self.coloredtext.tag_add("letters1", "{0}.{1}".format(line,char))
                            elif rand_color == 2:
                                self.coloredtext.tag_add("letters2", "{0}.{1}".format(line,char))
            elif cnfg.VIS_COLOR == 1:
                if cnfg.ORDER == "Ordered":
                    i = 1
                    for line in range(1, int(self.coloredtext.index('end-1c').split('.')[0])+1):                      # for every line in the text
                        for char in range(0, int(self.coloredtext.index(str(line)+".end").split('.')[1])+1):          # for every char in the line
                            charlie = self.coloredtext.get("{0}.{1}".format(line,char))
                            if charlie == " " or charlie == "\n" or charlie == "\t":
                                pass
                            else:
                                if i == 1:
                                    self.coloredtext.tag_add("letters1", "{0}.{1}".format(line,char))
                                elif i == 2:
                                    self.coloredtext.tag_add("lettersvis", "{0}.{1}".format(line,char))
                                elif i == 3:
                                    self.coloredtext.tag_add("letters2", "{0}.{1}".format(line,char))
                                elif i == 4:
                                    self.coloredtext.tag_add("lettersvis", "{0}.{1}".format(line,char))
                                i += 1
                                if i > 4: i = 1
                elif cnfg.ORDER == "Random":
                    for line in range(1, int(self.coloredtext.index('end-1c').split('.')[0])+1):                      # for every line in the text
                        for char in range(0, int(self.coloredtext.index(str(line)+".end").split('.')[1])+1):          # for every char in the line
                            rand_color = random.randint(1,3)
                            if rand_color == 1:
                                self.coloredtext.tag_add("letters1", "{0}.{1}".format(line,char))
                            elif rand_color == 2:
                                self.coloredtext.tag_add("letters2", "{0}.{1}".format(line,char))
                            elif rand_color == 3:
                                self.coloredtext.tag_add("lettersvis", "{0}.{1}".format(line,char))
        self.coloredtext.configure(state="disabled")

    def delete_tags(self):
        self.coloredtext.tag_delete("letters1", "letters2", "letters3")

    def refresh_text(self):
        self.coloredtext.configure(font=(cnfg.FONT, cnfg.FONT_SIZE, cnfg.FONT_BOLD))
        self.coloredtext.configure(background=cnfg.PALETTE[2])


class ColorsBottomOptionsFrame(tkinter.ttk.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.ttk.Frame.__init__(self, *args, **kwargs)

        self.parent = args[0]

        # 4x1 grid
        # column width can grow
        # row height cannot grow
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=0)

        # palette options frame
        self.palette_options_frame = tkinter.ttk.LabelFrame(self, text="Colors", padding=3)
        self.palette_options_frame.columnconfigure(0, weight=1)
        self.palette_options_frame.rowconfigure(0, weight=0)

        # palette
        self.palette = tkinter.ttk.Combobox(self.palette_options_frame, takefocus=False, state='readonly', values=('Purple & Teal', 'Red & Blue', ' ', ' '), textvariable=self.parent.parent.palette_var, width=13)
        self.palette.bind('<<ComboboxSelected>>', self.parent.parent.palette_click)
        self.palette.grid(column=0, row=0)

        # color pattern frame
        self.color_pattern_frame = tkinter.ttk.LabelFrame(self, text="Color pattern", padding=3)
        self.color_pattern_frame.columnconfigure(0, weight=1)
        self.color_pattern_frame.columnconfigure(1, weight=1)
        self.color_pattern_frame.columnconfigure(2, weight=1)
        self.color_pattern_frame.rowconfigure(0, weight=0)

        # colored item
        self.color_item_var = StringVar(value=cnfg.PATTERN)
        self.color_item = tkinter.ttk.Combobox(self.color_pattern_frame, textvariable=self.color_item_var, takefocus=False, state='readonly', values=('Words','Letters', ' ', ' '), width=7)
        self.color_item.bind('<<ComboboxSelected>>', self.color_item_chooser_click)
        self.color_item.grid(column=0, row=0, padx=(0,3))

        # color order
        self.color_order_var = StringVar(value=cnfg.ORDER)
        self.color_order = tkinter.ttk.Combobox(self.color_pattern_frame, textvariable=self.color_order_var, takefocus=False, state='readonly', values=('Ordered','Random', " ", ' '), width=8)
        self.color_order.bind('<<ComboboxSelected>>', self.color_order_chooser_click)
        self.color_order.grid(column=1, row=0, padx=(0,3))

        # anchor color
        self.anchor_option_var = IntVar(value=cnfg.VIS_COLOR)
        self.anchor_option = tkinter.ttk.Checkbutton(self.color_pattern_frame, variable=self.anchor_option_var, takefocus=False, text='Anchor color', command=self.anchor_color_click)
        self.anchor_option.grid(column=2, row=0)

        # font options frame
        self.font_options_frame = tkinter.ttk.LabelFrame(self, text="Font", padding=3)
        self.font_options_frame.columnconfigure(0, weight=1)
        self.font_options_frame.columnconfigure(1, weight=1)
        self.font_options_frame.columnconfigure(2, weight=1)
        self.font_options_frame.rowconfigure(0, weight=0)

        # font combobox
        self.font_chooser = tkinter.ttk.Combobox(self.font_options_frame, textvariable=self.parent.parent.font_chooser_var, takefocus=False, values=('Courier', 'Helvetica', 'Times', ' '), width=9, state="readonly")
        self.font_chooser.bind('<<ComboboxSelected>>', self.parent.parent.font_chooser_click)
        self.font_chooser.grid(column=0, row=0, padx=(0,3))

        # font size spinbox
        self.font_size = Spinbox(self.font_options_frame, from_=8, to=80, width=3, justify="center", textvariable=self.parent.parent.font_size_var, command=self.parent.parent.font_size_click, takefocus=False)
        self.font_size.bind('<Return>', self.parent.parent.font_size_click)
        self.font_size.bind('<Button-1>', self.parent.parent.font_size_cursor_click)
        self.font_size.grid(column=1, row=0, padx=(0,3))

        # font bold checkbutton
        self.font_bold = tkinter.ttk.Checkbutton(self.font_options_frame, text="Bold", variable=self.parent.parent.font_bold_var, command=self.parent.parent.font_bold_click, takefocus=False)
        self.font_bold.grid(column=2, row=0)

        # previous/next page frame
        self.prevnextframe = tkinter.ttk.LabelFrame(self, padding=3, text="Page")
        self.prevnextframe.columnconfigure(0, weight=1)
        self.prevnextframe.columnconfigure(1, weight=1)
        self.prevnextframe.rowconfigure(0, weight=0)

        # previous/next buttons
        self.current_page = StringVar(value="{0} / {1}".format(cnfg.TEXT_INDEX+1, len(cnfg.TEXT)))
        self.prevbutton = tkinter.ttk.Button(self.prevnextframe, text="<-", width=3, takefocus=False, command=self.parent.parent.on_prev_press)
        self.button_label = tkinter.ttk.Label(self.prevnextframe, textvariable=self.current_page)
        self.nextbutton = tkinter.ttk.Button(self.prevnextframe, text="->", width=3, takefocus=False, command=self.parent.parent.on_next_press)
        self.prevbutton.grid(column=0, row=0)
        self.button_label.grid(column=1, row=0)
        self.nextbutton.grid(column=2, row=0)

        self.palette_options_frame.grid(column=0, row=0, sticky="W")
        self.color_pattern_frame.grid(column=1, row=0)
        self.font_options_frame.grid(column=2, row=0)
        self.prevnextframe.grid(column=3, row=0, sticky="E")

        self.show_options()

    def show_options(self):
        if cnfg.SHOW_OPTIONS == 0:
            self.palette_options_frame.grid_remove()
            self.color_pattern_frame.grid_remove()
            self.font_options_frame.grid_remove()
            self.prevnextframe.grid(column=0, row=0, sticky="", columnspan=4)
        elif cnfg.SHOW_OPTIONS == 1:
            self.palette_options_frame.grid()
            self.color_pattern_frame.grid()
            self.font_options_frame.grid()
            self.prevnextframe.grid(column=3, row=0, sticky="E", columnspan=1)

    def color_item_chooser_click(self, *args):
        if self.color_item_var.get() == " ":
            self.color_item_var.set(cnfg.PATTERN)
        cnfg.PATTERN = self.color_item_var.get()
        self.parent.colorstextframe.create_new_text()
        self.parent.parent.focus()

    def color_order_chooser_click(self, *args):
        if self.color_order_var.get() == " ":
            self.color_order_var.set(cnfg.ORDER)
        cnfg.ORDER = self.color_order_var.get()
        self.parent.colorstextframe.create_new_text()
        self.parent.parent.focus()

    def anchor_color_click(self):
        cnfg.VIS_COLOR = self.anchor_option_var.get()
        self.parent.colorstextframe.create_new_text()