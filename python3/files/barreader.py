from tkinter import *
import tkinter.ttk
from files import cnfg

class BarReaderFrame(tkinter.ttk.Frame):
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
        self.barstextframe = BarsTextFrame(self)
        self.barstextframe.grid(column=0, row=0, sticky="NSEW")

        # bottom options frame
        # placed at 0,1
        self.barsbottomoptionsframe = BarsBottomOptionsFrame(self, padding=3)
        self.barsbottomoptionsframe.grid(column=0, row=1, sticky="NSEW")

class BarsTextFrame(tkinter.ttk.Frame):
    def __init__(self, *args, **kwargs):
        tkinter.ttk.Frame.__init__(self, *args, **kwargs)

        self.parent = args[0]

        # 2x1 grid
        # column 0 width can grow
        # column 1 width cannot grow
        # row height can grow
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

        self.create_canvas()
        self.create_scrollbar()
        self.create_text()
        self.update_scroll_region()

        self.canvas.grid(column=0, row=0, sticky="NSEW")
        self.scroll.grid(column=1, row=0, stick="NS")

        self.bar_list = []
        self.create_bars()
        self.refresh_text()

    def react_to_resize(self, event):
        self.resize_text_region(event)
        self.update_scroll_region()
        self.create_bars()
        self.refresh_text()
        self.update_scroll_region()

    def resize_text_region(self, event):
        self.canvas.itemconfig(self.canvas_text, width=event.width)

    def create_canvas(self):
        self.canvas = Canvas(self, width=cnfg.SCREEN_WIDTH*.6, height=cnfg.SCREEN_HEIGHT*.6, background=cnfg.PALETTE[3])
        self.canvas.bind("<Configure>", self.react_to_resize)
        self.canvas.bind("<Button-1>", lambda *args: self.parent.parent.parent.focus())

    def create_text(self):
        self.canvas_text = self.canvas.create_text(10, 10, anchor="nw")
        self.canvas.itemconfig(self.canvas_text, text=cnfg.TEXT[cnfg.TEXT_INDEX], width=self.canvas.cget("width"))
        self.canvas.itemconfig(self.canvas_text, font=(cnfg.FONT, cnfg.FONT_SIZE, cnfg.FONT_BOLD), fill=cnfg.PALETTE[2])

    def refresh_text(self):
        width = self.canvas.itemcget(self.canvas_text,"width")
        self.canvas.delete(self.canvas_text)
        self.canvas_text = self.canvas.create_text(9, -1, anchor="nw")
        self.canvas.itemconfig(self.canvas_text, text=cnfg.TEXT[cnfg.TEXT_INDEX], width=width)
        self.canvas.itemconfig(self.canvas_text, font=(cnfg.FONT, cnfg.FONT_SIZE, cnfg.FONT_BOLD), fill=cnfg.PALETTE[2])

    def create_scrollbar(self):
        self.scroll = tkinter.ttk.Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)

    def update_scroll_region(self):
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def create_bars(self):
        # delete old bars
        for item in self.bar_list:
            self.canvas.delete(item)

        # create new bars
        framebounds = self.parent.grid_bbox(0,0)
        canvasbounds = self.canvas.bbox(ALL)
        width = cnfg.SCREEN_WIDTH
        if (canvasbounds[3] - canvasbounds[1] + 30) > (framebounds[3] - framebounds[1] + 30):
            height = canvasbounds[3] - canvasbounds[1] + 30
        else:
            height = framebounds[3] - framebounds[1] + 30
        redblue = 1
        fill = ""
        for num in range(0, width, cnfg.BAR_WIDTH+cnfg.BAR_SPACING):
            if redblue % 2 == 0:
                fill = cnfg.PALETTE[1]
            else:
                fill = cnfg.PALETTE[0]
            self.bar_list.append(self.canvas.create_rectangle(num,0,num+cnfg.BAR_WIDTH,height, fill=fill, outline=""))
            redblue += 1

    def font_update(self):
        self.refresh_text()
        self.create_bars()
        self.refresh_text()
        self.update_scroll_region()

class BarsBottomOptionsFrame(tkinter.ttk.Frame):
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

        # palette - COMMON
        self.palette = tkinter.ttk.Combobox(self.palette_options_frame, takefocus=False, state='readonly', values=('Purple & Teal', 'Red & Blue', " ", " "), textvariable=self.parent.parent.palette_var, width=13)
        self.palette.bind('<<ComboboxSelected>>', self.parent.parent.palette_click)
        self.palette.grid(column=0, row=0)

        # bar options frame
        self.bar_options_frame = tkinter.ttk.LabelFrame(self, text="Bar", padding=3)
        self.bar_options_frame.columnconfigure(0, weight=1)
        self.bar_options_frame.columnconfigure(1, weight=1)
        self.bar_options_frame.columnconfigure(2, weight=1)
        self.bar_options_frame.columnconfigure(3, weight=1)
        self.bar_options_frame.rowconfigure(0, weight=0)

        # bar width spinbox
        self.bar_width_var = IntVar(value=cnfg.BAR_WIDTH)
        self.bar_width_label = tkinter.ttk.Label(self.bar_options_frame, text="Width:")
        self.bar_width = Spinbox(self.bar_options_frame, from_=1, to=200, width=5, justify="center", textvariable=self.bar_width_var, takefocus=False, command=self.bar_width_click)
        self.bar_width.bind('<Return>', self.bar_width_click)
        self.bar_width.bind('<Button-1>', self.bar_width_cursor_click)
        self.bar_width_label.grid(column=0, row=0)
        self.bar_width.grid(column=1, row=0, padx=(0,3))

        # bar spacing spinbox
        self.bar_spacing_var = IntVar(value=cnfg.BAR_SPACING)
        self.bar_spacing_label = tkinter.ttk.Label(self.bar_options_frame, text="Spacing:")
        self.bar_spacing = Spinbox(self.bar_options_frame, from_=0, to=200, width=5, justify="center", textvariable=self.bar_spacing_var, takefocus=False, command=self.bar_spacing_click)
        self.bar_spacing.bind('<Return>', self.bar_spacing_click)
        self.bar_spacing.bind('<Button-1>', self.bar_spacing_cursor_click)
        self.bar_spacing_label.grid(column=2, row=0)
        self.bar_spacing.grid(column=3, row=0)

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

        # previous/next buttons - COMMON
        self.current_page = StringVar(value="{0} / {1}".format(cnfg.TEXT_INDEX+1, len(cnfg.TEXT)))
        self.prevbutton = tkinter.ttk.Button(self.prevnextframe, text="<-", width=3, takefocus=False, command=self.parent.parent.on_prev_press)
        self.button_label = tkinter.ttk.Label(self.prevnextframe, textvariable=self.current_page)
        self.nextbutton = tkinter.ttk.Button(self.prevnextframe, text="->", width=3, takefocus=False, command=self.parent.parent.on_next_press)
        self.prevbutton.grid(column=0, row=0)
        self.button_label.grid(column=1, row=0)
        self.nextbutton.grid(column=2, row=0)

        self.palette_options_frame.grid(column=0, row=0, sticky="W")
        self.bar_options_frame.grid(column=1, row=0)
        self.font_options_frame.grid(column=2, row=0)
        self.prevnextframe.grid(column=3, row=0, sticky="E")

        self.show_options()

    def bar_width_cursor_click(self, *args):
        try:
            self.bar_width_previous = self.bar_width_var.get()
        except:
            pass

    def bar_width_click(self, *args):
        try:
            if self.bar_width_var.get() < 1:
                self.bar_width_var.set(1)
            elif self.bar_width_var.get() > 200:
                self.bar_width_var.set(200)
        except:
            self.bar_width_var.set(self.bar_width_previous)
        cnfg.BAR_WIDTH = self.bar_width_var.get()
        self.parent.parent.parent.focus()
        self.parent.barstextframe.font_update()

    def bar_spacing_cursor_click(self, *args):
        try:
            self.bar_spacing_previous = self.bar_spacing_var.get()
        except:
            pass

    def bar_spacing_click(self, *args):
        try:
            if self.bar_spacing_var.get() < 0:
                self.bar_spacing_var.set(0)
            elif self.bar_spacing_var.get() > 200:
                self.bar_spacing_var.set(200)
        except:
            self.bar_spacing_var.set(self.bar_spacing_previous)
        cnfg.BAR_SPACING = self.bar_spacing_var.get()
        self.parent.parent.parent.focus()
        self.parent.barstextframe.font_update()

    def show_options(self):
        if cnfg.SHOW_OPTIONS == 0:
            self.palette_options_frame.grid_remove()
            self.bar_options_frame.grid_remove()
            self.font_options_frame.grid_remove()
            self.prevnextframe.grid(column=0, row=0, sticky="", columnspan=4)
        elif cnfg.SHOW_OPTIONS == 1:
            self.palette_options_frame.grid()
            self.bar_options_frame.grid()
            self.font_options_frame.grid()
            self.prevnextframe.grid(column=3, row=0, sticky="E", columnspan=1)
