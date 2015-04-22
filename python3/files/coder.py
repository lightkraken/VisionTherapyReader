from tkinter import *
import tkinter.ttk
from files import cnfg

class AskPassword(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent, padx=6, pady=6)
        self.resizable(0,0)
        self.parent = parent

        self.focus()

        self.label = tkinter.ttk.Label(self, text="Enter config code:")
        self.entry = tkinter.ttk.Entry(self, width=11)
        self.problem_label = tkinter.ttk.Label(self, text="Invalid config code. Please try again.", foreground="red")
        self.blank_label = tkinter.ttk.Label(self, text=" ")
        self.okbutton = tkinter.ttk.Button(self, text="OK", takefocus=False, command=self.ok_click)
        self.cancelbutton = tkinter.ttk.Button(self, text="Cancel", takefocus=False, command=self.destroy)

        self.label.grid(row=0, column=0, padx=(6,6), pady=(6,0))
        self.entry.grid(row=0, column=1, padx=(0,6), pady=(6,0))
        self.problem_label.grid(row=1, column=0, columnspan=2)
        self.problem_label.grid_remove()
        self.blank_label.grid(row=1, column=0, columnspan=2)
        self.cancelbutton.grid(row=2, column=0)
        self.okbutton.grid(row=2, column=1)

        self.paste_menu = Menu(self)
        self.paste_menu.add_command(label="Paste", command=lambda: self.entry.event_generate("<<Paste>>"))
        self.bind('<3>', lambda e: self.paste_menu.post(e.x_root, e.y_root))

    def ok_click(self):
        self.password = self.entry.get().replace(" ", "")
        if self.validate(self.password) == True:
            self.decode(self.password)
            self.parent.parent.restart()
            self.destroy()
        else:
            self.blank_label.grid_forget()
            self.problem_label.grid()

    def validate(self, n):
        n = n.upper()
        try:
            if len(n) == 9 and \
               0 <= int("0x"+n[0],16)   <= 15 and \
               0 <= int("0x"+n[1],16)   <= 11 and \
               8 <= int(n[2:4])         <= 80 and \
               1 <= int("0x"+n[4:6],16) <= 200 and \
               0 <= int("0x"+n[6:8],16)  <= 200 and \
               int(n[8]) == 0 or int(n[8]) == 1:
                return True
            else:
                return False
        except:
            return False

    def decode(self, n):
        if n[0] == "0" or n[0].lower() == "o":
            cnfg.VIS_COLOR = 0
            cnfg.PATTERN = "Letters"
            cnfg.ORDER = "Ordered"
            cnfg.SHOW_OPTIONS = 0
        elif n[0] == "1":
            cnfg.VIS_COLOR = 0
            cnfg.PATTERN = "Letters"
            cnfg.ORDER = "Ordered"
            cnfg.SHOW_OPTIONS = 1
        elif n[0] == "2":
            cnfg.VIS_COLOR = 0
            cnfg.PATTERN = "Letters"
            cnfg.ORDER = "Random"
            cnfg.SHOW_OPTIONS = 0
        elif n[0] == "3":
            cnfg.VIS_COLOR = 0
            cnfg.PATTERN = "Letters"
            cnfg.ORDER = "Random"
            cnfg.SHOW_OPTIONS = 1
        elif n[0] == "4":
            cnfg.VIS_COLOR = 0
            cnfg.PATTERN = "Words"
            cnfg.ORDER = "Ordered"
            cnfg.SHOW_OPTIONS = 0
        elif n[0] == "5":
            cnfg.VIS_COLOR = 0
            cnfg.PATTERN = "Words"
            cnfg.ORDER = "Ordered"
            cnfg.SHOW_OPTIONS = 1
        elif n[0] == "6":
            cnfg.VIS_COLOR = 0
            cnfg.PATTERN = "Words"
            cnfg.ORDER = "Random"
            cnfg.SHOW_OPTIONS = 0
        elif n[0] == "7":
            cnfg.VIS_COLOR = 0
            cnfg.PATTERN = "Words"
            cnfg.ORDER = "Random"
            cnfg.SHOW_OPTIONS = 1
        elif n[0] == "8":
            cnfg.VIS_COLOR = 1
            cnfg.PATTERN = "Letters"
            cnfg.ORDER = "Ordered"
            cnfg.SHOW_OPTIONS = 0
        elif n[0] == "9":
            cnfg.VIS_COLOR = 1
            cnfg.PATTERN = "Letters"
            cnfg.ORDER = "Ordered"
            cnfg.SHOW_OPTIONS = 1
        elif n[0].lower() == "a":
            cnfg.VIS_COLOR = 1
            cnfg.PATTERN = "Letters"
            cnfg.ORDER = "Random"
            cnfg.SHOW_OPTIONS = 0
        elif n[0].lower() == "b":
            cnfg.VIS_COLOR = 1
            cnfg.PATTERN = "Letters"
            cnfg.ORDER = "Random"
            cnfg.SHOW_OPTIONS = 1
        elif n[0].lower() == "c":
            cnfg.VIS_COLOR = 1
            cnfg.PATTERN = "Words"
            cnfg.ORDER = "Ordered"
            cnfg.SHOW_OPTIONS = 0
        elif n[0].lower() == "d":
            cnfg.VIS_COLOR = 1
            cnfg.PATTERN = "Words"
            cnfg.ORDER = "Ordered"
            cnfg.SHOW_OPTIONS = 1
        elif n[0].lower() == "e":
            cnfg.VIS_COLOR = 1
            cnfg.PATTERN = "Words"
            cnfg.ORDER = "Random"
            cnfg.SHOW_OPTIONS = 0
        elif n[0].lower() == "f":
            cnfg.VIS_COLOR = 1
            cnfg.PATTERN = "Words"
            cnfg.ORDER = "Random"
            cnfg.SHOW_OPTIONS = 1
        #---------------------------------------------------------------------------
        if n[1] == "0" or n[1].lower() == "o":
            cnfg.FONT = "Courier"
            cnfg.FONT_BOLD = ""
            cnfg.PALETTE_CHOICE = "Purple & Teal"
        elif n[1] == "1":
            cnfg.FONT = "Courier"
            cnfg.FONT_BOLD = ""
            cnfg.PALETTE_CHOICE = "Red & Blue"
        elif n[1] == "2":
            cnfg.FONT = "Courier"
            cnfg.FONT_BOLD = "bold"
            cnfg.PALETTE_CHOICE = "Purple & Teal"
        elif n[1] == "3":
            cnfg.FONT = "Courier"
            cnfg.FONT_BOLD = "bold"
            cnfg.PALETTE_CHOICE = "Red & Blue"
        elif n[1] == "4":
            cnfg.FONT = "Helvetica"
            cnfg.FONT_BOLD = ""
            cnfg.PALETTE_CHOICE = "Purple & Teal"
        elif n[1] == "5":
            cnfg.FONT = "Helvetica"
            cnfg.FONT_BOLD = ""
            cnfg.PALETTE_CHOICE = "Red & Blue"
        elif n[1] == "6":
            cnfg.FONT = "Helvetica"
            cnfg.FONT_BOLD = "bold"
            cnfg.PALETTE_CHOICE = "Purple & Teal"
        elif n[1] == "7":
            cnfg.FONT = "Helvetica"
            cnfg.FONT_BOLD = "bold"
            cnfg.PALETTE_CHOICE = "Red & Blue"
        elif n[1] == "8":
            cnfg.FONT = "Times"
            cnfg.FONT_BOLD = ""
            cnfg.PALETTE_CHOICE = "Purple & Teal"
        elif n[1] == "9":
            cnfg.FONT = "Times"
            cnfg.FONT_BOLD = ""
            cnfg.PALETTE_CHOICE = "Red & Blue"
        elif n[1].lower() == "a":
            cnfg.FONT = "Times"
            cnfg.FONT_BOLD = "bold"
            cnfg.PALETTE_CHOICE = "Purple & Teal"
        elif n[1].lower() == "b":
            cnfg.FONT = "Times"
            cnfg.FONT_BOLD = "bold"
            cnfg.PALETTE_CHOICE = "Red & Blue"
        #---------------------------------------------------------------------------
        cnfg.FONT_SIZE = int(n[2:4])
        #---------------------------------------------------------------------------
        cnfg.BAR_WIDTH = int("0x"+n[4:6], 16)
        #---------------------------------------------------------------------------
        cnfg.BAR_SPACING = int("0x"+n[6:8], 16)
        #---------------------------------------------------------------------------
        cnfg.CURRENT_TAB = int(n[8])

class RetrievePassWord(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent, padx=6, pady=6)
        self.resizable(0,0)
        self.parent = parent

        self.focus()

        self.label = tkinter.ttk.Label(self, text="The config code for the\ncurrent configuration is:")
        self.entry = tkinter.ttk.Entry(self, width=11)
        self.entry.insert(0, self.encode())
        self.entry.configure(state="readonly")
        self.button = tkinter.ttk.Button(self, text="OK", command=lambda:self.destroy())

        self.label.grid(column=0, row=0, padx=(6,6), pady=(6,0))
        self.entry.grid(column=1, row=0, padx=(0,6), pady=(6,0))
        self.button.grid(column=0, row=1, columnspan=2, pady=(16,0))

        self.copy_menu = Menu(self)
        self.copy_menu.add_command(label="Copy", command=lambda: self.entry.event_generate("<<Copy>>"))
        self.bind('<3>', lambda e: self.copy_menu.post(e.x_root, e.y_root))

    def encode(self):
        password = []
        if cnfg.VIS_COLOR == 0 and cnfg.PATTERN == "Letters" and cnfg.ORDER == "Ordered" and cnfg.SHOW_OPTIONS == 0:
            password.append("0")
        elif cnfg.VIS_COLOR == 0 and cnfg.PATTERN == "Letters" and cnfg.ORDER == "Ordered" and cnfg.SHOW_OPTIONS == 1:
            password.append("1")
        elif cnfg.VIS_COLOR == 0 and cnfg.PATTERN == "Letters" and cnfg.ORDER == "Random" and cnfg.SHOW_OPTIONS == 0:
            password.append("2")
        elif cnfg.VIS_COLOR == 0 and cnfg.PATTERN == "Letters" and cnfg.ORDER == "Random" and cnfg.SHOW_OPTIONS == 1:
            password.append("3")
        elif cnfg.VIS_COLOR == 0 and cnfg.PATTERN == "Words" and cnfg.ORDER == "Ordered" and cnfg.SHOW_OPTIONS == 0:
            password.append("4")
        elif cnfg.VIS_COLOR == 0 and cnfg.PATTERN == "Words" and cnfg.ORDER == "Ordered" and cnfg.SHOW_OPTIONS == 1:
            password.append("5")
        elif cnfg.VIS_COLOR == 0 and cnfg.PATTERN == "Words" and cnfg.ORDER == "Random" and cnfg.SHOW_OPTIONS == 0:
            password.append("6")
        elif cnfg.VIS_COLOR == 0 and cnfg.PATTERN == "Words" and cnfg.ORDER == "Random" and cnfg.SHOW_OPTIONS == 1:
            password.append("7")
        elif cnfg.VIS_COLOR == 1 and cnfg.PATTERN == "Letters" and cnfg.ORDER == "Ordered" and cnfg.SHOW_OPTIONS == 0:
            password.append("8")
        elif cnfg.VIS_COLOR == 1 and cnfg.PATTERN == "Letters" and cnfg.ORDER == "Ordered" and cnfg.SHOW_OPTIONS == 1:
            password.append("9")
        elif cnfg.VIS_COLOR == 1 and cnfg.PATTERN == "Letters" and cnfg.ORDER == "Random" and cnfg.SHOW_OPTIONS == 0:
            password.append("A")
        elif cnfg.VIS_COLOR == 1 and cnfg.PATTERN == "Letters" and cnfg.ORDER == "Random" and cnfg.SHOW_OPTIONS == 1:
            password.append("B")
        elif cnfg.VIS_COLOR == 1 and cnfg.PATTERN == "Words" and cnfg.ORDER == "Ordered" and cnfg.SHOW_OPTIONS == 0:
            password.append("C")
        elif cnfg.VIS_COLOR == 1 and cnfg.PATTERN == "Words" and cnfg.ORDER == "Ordered" and cnfg.SHOW_OPTIONS == 1:
            password.append("D")
        elif cnfg.VIS_COLOR == 1 and cnfg.PATTERN == "Words" and cnfg.ORDER == "Random" and cnfg.SHOW_OPTIONS == 0:
            password.append("E")
        elif cnfg.VIS_COLOR == 1 and cnfg.PATTERN == "Words" and cnfg.ORDER == "Random" and cnfg.SHOW_OPTIONS == 1:
            password.append("F")
        #---------------------------------------------------------------------------
        if cnfg.FONT == "Courier" and cnfg.FONT_BOLD == "" and cnfg.PALETTE_CHOICE == "Purple & Teal":
            password.append("0")
        elif cnfg.FONT == "Courier" and cnfg.FONT_BOLD == "" and cnfg.PALETTE_CHOICE == "Red & Blue":
            password.append("1")
        elif cnfg.FONT == "Courier" and cnfg.FONT_BOLD == "bold" and cnfg.PALETTE_CHOICE == "Purple & Teal":
            password.append("2")
        elif cnfg.FONT == "Courier" and cnfg.FONT_BOLD == "bold" and cnfg.PALETTE_CHOICE == "Red & Blue":
            password.append("3")
        elif cnfg.FONT == "Helvetica" and cnfg.FONT_BOLD == "" and cnfg.PALETTE_CHOICE == "Purple & Teal":
            password.append("4")
        elif cnfg.FONT == "Helvetica" and cnfg.FONT_BOLD == "" and cnfg.PALETTE_CHOICE == "Red & Blue":
            password.append("5")
        elif cnfg.FONT == "Helvetica" and cnfg.FONT_BOLD == "bold" and cnfg.PALETTE_CHOICE == "Purple & Teal":
            password.append("6")
        elif cnfg.FONT == "Helvetica" and cnfg.FONT_BOLD == "bold" and cnfg.PALETTE_CHOICE == "Red & Blue":
            password.append("7")
        elif cnfg.FONT == "Times" and cnfg.FONT_BOLD == "" and cnfg.PALETTE_CHOICE == "Purple & Teal":
            password.append("8")
        elif cnfg.FONT == "Times" and cnfg.FONT_BOLD == "" and cnfg.PALETTE_CHOICE == "Red & Blue":
            password.append("9")
        elif cnfg.FONT == "Times" and cnfg.FONT_BOLD == "bold" and cnfg.PALETTE_CHOICE == "Purple & Teal":
            password.append("A")
        elif cnfg.FONT == "Times" and cnfg.FONT_BOLD == "bold" and cnfg.PALETTE_CHOICE == "Red & Blue":
            password.append("B")
        #---------------------------------------------------------------------------
        if len(str(cnfg.FONT_SIZE)) == 1:
            password.append("0"+str(cnfg.FONT_SIZE))
        else:
            password.append(str(cnfg.FONT_SIZE))
        #---------------------------------------------------------------------------
        barwidth = hex(cnfg.BAR_WIDTH)[2:].upper()
        if len(barwidth) == 1:
            barwidth = "0" + barwidth
        password.append(barwidth)
        # --------------------------------------------------------------------------
        barspacing = hex(cnfg.BAR_SPACING)[2:].upper()
        if len(barspacing) == 1:
            barspacing = "0" + barspacing
        password.append(barspacing)
        # --------------------------------------------------------------------------
        password.append(str(cnfg.CURRENT_TAB))
        # -------------------------------------------------------------------------
        return "".join(password)