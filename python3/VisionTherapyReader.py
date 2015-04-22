from tkinter import *
import tkinter.filedialog
import tkinter.ttk
from files.colorreader import *
from files.barreader import *
from files.ptadjust import *
from files.rbadjust import *
from files.ptcalibrate import *
from files.rbcalibrate import *
from files.paster import *
from files import coder

class Root(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Vision Therapy Reader")
        self.start()

    def start(self):

        # give the config file some info
        cnfg.SCREEN_WIDTH = self.winfo_screenwidth()
        cnfg.SCREEN_HEIGHT = self.winfo_screenheight()

        # 1x1 grid
        # grid grows in all directions
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # content frame
        # placed at 0,0
        # sticky on all sides
        self.content = Content(self)
        self.content.grid(column=0, row=0, sticky="NSEW")

        # menu bar
        self.option_add('*tearOff', FALSE)
        self.menubar = MenuBar(self)
        self.config(menu=self.menubar)

        # key bindings
        self.bind("<Up>", self.up_press)
        self.bind("<Down>", self.down_press)

        # close click binding
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        cnfg.END_OPTIONS = cnfg.create_options_dict()
        if cnfg.START_OPTIONS == cnfg.END_OPTIONS:
            self.destroy()
        else:
            self.quit_dialogue = cnfg.QuitDialogue(self)

    def up_press(self, *args):
        if cnfg.CURRENT_TAB == 0:
            self.content.barreaderframe.barstextframe.canvas.yview_scroll(-1,UNITS)
        elif cnfg.CURRENT_TAB == 1:
            self.content.colorreaderframe.colorstextframe.coloredtext.yview_scroll(-1,UNITS)

    def down_press(self, *args):
        if cnfg.CURRENT_TAB == 0:
            self.content.barreaderframe.barstextframe.canvas.yview_scroll(1,UNITS)
        elif cnfg.CURRENT_TAB == 1:
            self.content.colorreaderframe.colorstextframe.coloredtext.yview_scroll(1,UNITS)

    def restart(self):
        self.content.destroy()
        self.start()

class MenuBar(Menu):
    def __init__(self, *args, **kwargs):
        Menu.__init__(self, *args, **kwargs)

        self.parent = args[0]

        # file
        self.file_menu = Menu(self)
        self.file_menu.add_command(label="Open file...", command=self.on_open)
        self.file_menu.add_command(label="Paste text...", command=self.on_paste)
        self.file_menu.add_command(label="Close file", command=self.on_close)
        self.file_menu.add_command(label="Exit", command=self.parent.on_close)
        self.add_cascade(label="File", menu=self.file_menu)

        # color
        self.color_menu = Menu(self)
        self.color_menu.add_command(label="Calibrate colors...", command=self.calib_menu_start)

        self.advanced_color_submenu = Menu(self)
        self.advanced_color_submenu.add_command(label="Manually adjust colors...", command=self.adjust_menu_start)

        self.color_menu.add_cascade(menu=self.advanced_color_submenu, label="Advanced...")

        self.add_cascade(menu=self.color_menu, label="Colors")

        # view
        self.view_menu = Menu(self)
        self.show_options_var = IntVar(value=cnfg.SHOW_OPTIONS)
        self.view_menu.add_checkbutton(label="Show Options Bar", onvalue=1, offvalue=0, variable=self.show_options_var, command=self.show_options_click)
        self.add_cascade(label="View", menu=self.view_menu)

        # password
        self.password_menu = Menu(self)
        self.password_menu.add_command(label="Enter Config Code...", command=self.enter_password)
        self.password_menu.add_command(label="Create Config Code", command=self.create_password)
        self.add_cascade(menu=self.password_menu, label="Config Code")

    def on_paste(self):
        self.pastey = Paster(self)

    def adjust_menu_start(self):
        self.adjust = AdjustMenu(self)

    def calib_menu_start(self):
        self.calib = CalibrateMenu(self)

    def enter_password(self):
        self.password_decoder = coder.AskPassword(self)

    def create_password(self):
        self.password_creator = coder.RetrievePassWord(self)

    def show_options_click(self):
        cnfg.SHOW_OPTIONS = self.show_options_var.get()
        self.parent.content.barreaderframe.barsbottomoptionsframe.show_options()
        self.parent.content.colorreaderframe.colorsbottomoptionsframe.show_options()

    def calib_purpleteal(self):
        self.calibpt_menu = PTCalibrate(self)

    def calib_redblue(self):
        self.calibrb_menu = RBCalibrate(self)

    def adjust_purpleteal(self):
        self.adjustpt_menu = PTAdjustMenu(self)

    def adjust_redblue(self):
        self.adjustrb_menu = RBAdjustMenu(self)

    def on_open(self):
        dialog = tkinter.filedialog.Open(self, filetypes = [('Text files', '*.txt')])
        openfile = dialog.show()

        if openfile != "":
            cnfg.load_file(openfile)
            self.refresh_all()

    def on_close(self):
        cnfg.TEXT = []
        cnfg.TEXT.append("")
        cnfg.TEXT_INDEX = 0
        self.refresh_all()

    def on_quit(self):
        self.parent.destroy()

    def refresh_all(self):
        self.parent.content.barreaderframe.barstextframe.refresh_text()
        self.parent.content.barreaderframe.barstextframe.create_bars()
        self.parent.content.barreaderframe.barstextframe.refresh_text()
        self.parent.content.barreaderframe.barstextframe.update_scroll_region()

        self.parent.content.colorreaderframe.colorstextframe.create_new_text()
        self.parent.content.colorreaderframe.colorstextframe.refresh_text()

        self.parent.content.update_page_buttons()

class Content(tkinter.ttk.Notebook):
    def __init__(self, *args, **kwargs):
        tkinter.ttk.Notebook.__init__(self, *args, takefocus=False)

        self.parent = args[0]

        # common variables
        self.palette_var = StringVar(value=cnfg.PALETTE_CHOICE)
        self.font_chooser_var = StringVar(value=cnfg.FONT)
        self.font_size_var = IntVar(value=cnfg.FONT_SIZE)
        self.font_bold_var = IntVar()
        if cnfg.FONT_BOLD == "":
            self.font_bold_var.set(0)
        elif cnfg.FONT_BOLD == "bold":
            self.font_bold_var.set(1)

        self.barreaderframe = BarReaderFrame(self)
        self.colorreaderframe = ColorReaderFrame(self)

        self.add(self.barreaderframe, text="Bar reader")
        self.add(self.colorreaderframe, text="Color reader")

        self.bind("<<NotebookTabChanged>>", self.set_current_tab_var)
        self.select(cnfg.CURRENT_TAB)
        self.update_page_buttons()
        self.palette_click()

    def set_current_tab_var(self, *args):
        cnfg.CURRENT_TAB = self.index(self.select())

    def palette_click(self, *args):
        if self.palette_var.get() == " ":
            self.palette_var.set(cnfg.PALETTE_CHOICE)
        cnfg.PALETTE_CHOICE = self.palette_var.get()
        cnfg.update_palette()

        self.parent.focus()

        # bar reader
        self.barreaderframe.barstextframe.canvas.config(background=cnfg.PALETTE[3])
        self.barreaderframe.barstextframe.font_update()

        # color reader
        self.colorreaderframe.colorstextframe.create_new_tags()
        self.colorreaderframe.colorstextframe.refresh_text()

    def font_chooser_click(self, *args):
        if self.font_chooser_var.get() == " ":
            self.font_chooser_var.set(cnfg.FONT)
        cnfg.FONT = self.font_chooser_var.get()

        self.parent.focus()

        # bar reader
        self.barreaderframe.barstextframe.font_update()

        # color reader
        self.colorreaderframe.colorstextframe.refresh_text()

    def font_size_cursor_click(self, *args):
        try:
            self.font_size_previous = self.font_size_var.get()
        except:
            pass

    def font_size_click(self, *args, **kwargs):
        try:
            if self.font_size_var.get() < 8:
                self.font_size_var.set(8)
            elif self.font_size_var.get() > 80:
                self.font_size_var.set(80)
        except:
            self.font_size_var.set(self.font_size_previous)
        cnfg.FONT_SIZE = self.font_size_var.get()
        self.parent.focus()
        self.barreaderframe.barstextframe.font_update()
        self.colorreaderframe.colorstextframe.refresh_text()

    def font_bold_click(self):
        if self.font_bold_var.get() == 0:
            cnfg.FONT_BOLD = ""
        if self.font_bold_var.get() == 1:
            cnfg.FONT_BOLD = "bold"

        # bar reader
        self.barreaderframe.barstextframe.font_update()

        # color reader
        self.colorreaderframe.colorstextframe.refresh_text()

    def on_prev_press(self):
        cnfg.TEXT_INDEX -= 1

        # bar reader
        self.barreaderframe.barstextframe.font_update()

        # color reader
        self.colorreaderframe.colorstextframe.delete_tags()
        self.colorreaderframe.colorstextframe.create_new_tags()
        self.colorreaderframe.colorstextframe.create_new_text()
        self.colorreaderframe.colorstextframe.refresh_text()

        self.update_page_buttons()

    def on_next_press(self):
        cnfg.TEXT_INDEX += 1
        # bar reader
        self.barreaderframe.barstextframe.font_update()

        # color reader
        self.colorreaderframe.colorstextframe.delete_tags()
        self.colorreaderframe.colorstextframe.create_new_tags()
        self.colorreaderframe.colorstextframe.create_new_text()
        self.colorreaderframe.colorstextframe.refresh_text()

        self.update_page_buttons()

    def update_page_buttons(self):
        if len(cnfg.TEXT) == 1:                                                                     #if the text is only one page long
            self.barreaderframe.barsbottomoptionsframe.prevbutton.configure(state=DISABLED)
            self.barreaderframe.barsbottomoptionsframe.nextbutton.configure(state=DISABLED)
            self.colorreaderframe.colorsbottomoptionsframe.prevbutton.configure(state=DISABLED)
            self.colorreaderframe.colorsbottomoptionsframe.nextbutton.configure(state=DISABLED)
        elif len(cnfg.TEXT) > 1:                                                                    #if the text is more than one page...
            if cnfg.TEXT_INDEX == 0:                                                                #and at the beginning
                self.barreaderframe.barsbottomoptionsframe.prevbutton.configure(state=DISABLED)
                self.barreaderframe.barsbottomoptionsframe.nextbutton.configure(state=NORMAL)
                self.colorreaderframe.colorsbottomoptionsframe.prevbutton.configure(state=DISABLED)
                self.colorreaderframe.colorsbottomoptionsframe.nextbutton.configure(state=NORMAL)
            elif cnfg.TEXT_INDEX == len(cnfg.TEXT)-1:                                               #and at the end
                self.barreaderframe.barsbottomoptionsframe.prevbutton.configure(state=NORMAL)
                self.barreaderframe.barsbottomoptionsframe.nextbutton.configure(state=DISABLED)
                self.colorreaderframe.colorsbottomoptionsframe.prevbutton.configure(state=NORMAL)
                self.colorreaderframe.colorsbottomoptionsframe.nextbutton.configure(state=DISABLED)
            else:
                self.barreaderframe.barsbottomoptionsframe.prevbutton.configure(state=NORMAL)       #and in the middle
                self.barreaderframe.barsbottomoptionsframe.nextbutton.configure(state=NORMAL)
                self.colorreaderframe.colorsbottomoptionsframe.prevbutton.configure(state=NORMAL)
                self.colorreaderframe.colorsbottomoptionsframe.nextbutton.configure(state=NORMAL)
        try:
            self.barreaderframe.barstextframe.canvas.yview_moveto(0.0)
        except:
            pass
        self.colorreaderframe.colorsbottomoptionsframe.current_page.set(value="{0} / {1}".format(cnfg.TEXT_INDEX+1, len(cnfg.TEXT)))
        self.barreaderframe.barsbottomoptionsframe.current_page.set(value="{0} / {1}".format(cnfg.TEXT_INDEX+1, len(cnfg.TEXT)))

root = Root()
root.mainloop()