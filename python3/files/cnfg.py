from tkinter import *
import tkinter.ttk

def add_two_colors(color1, color2):
    c1r = int(color1[1:3], 16)
    c1g = int(color1[3:5], 16)
    c1b = int(color1[5:], 16)

    c2r = int(color2[1:3], 16)
    c2g = int(color2[3:5], 16)
    c2b = int(color2[5:], 16)

    c3r = c1r + c2r
    if c3r > 255: c3r = 255
    c3g = c1g + c2g
    if c3g > 255: c3g = 255
    c3b = c1b + c2b
    if c3b > 255: c3b = 255

    c3list = []
    c3list.append(hex(c3r)[2:])
    c3list.append(hex(c3g)[2:])
    c3list.append(hex(c3b)[2:])

    for index, item in enumerate(c3list):
        if len(item) == 1:
            c3list[index] = "0" + item

    return ("#" + c3list[0] + c3list[1] + c3list[2]).upper()

#-------------------------------------------------------------------------------

SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0

TEXT = []
TEXT.append("")
TEXT_INDEX = 0

FONT = "Times"
FONT_SIZE = 55
FONT_BOLD = "bold"

BAR_WIDTH = 35
BAR_SPACING = 35

COLOR1 = "#7F007F" #purple                      #bar 1                  #letters 1
COLOR2 = "#007F7F" #teal                        #bar 2                  #letters 2
COLOR3 = "#808080" #gray - 50%                  #letters                #background
COLOR4 = "#000000" #black cancels w/ teal       #background
COLOR5 = COLOR4                                                         #letters visible

COLOR6 = "#FF0000" #red                         #bar 1                  #letters 1
COLOR7 = "#0000FF" #blue                        #bar 2                  #letters 2
COLOR8 = "#000000" #blackish                    #letters                #background
COLOR9 = "#808080" #gray - 50%                  #background
COLOR10 = add_two_colors(COLOR6, COLOR7)                                #letters visible

PALETTE_CHOICE = "Purple & Teal"

PALETTE = []

VIS_COLOR = 0
PATTERN = "Words"
ORDER = "Ordered"

SHOW_OPTIONS = 1

CURRENT_TAB = 0

START_OPTIONS = {}
END_OPTIONS = {}

#-------------------------------------------------------------------------------

def start():
    global START_OPTIONS
    try:
        START_OPTIONS = parse_config('files/config.txt')
        extract_values(START_OPTIONS)
    except:
        START_OPTIONS = create_options_dict()
    update_palette()

def parse_config(filename):
    OPTION_CHAR =  '='
    options = {}
    f = open(filename)
    for line in f:
        # Second, find lines with an option=value:
        if OPTION_CHAR in line:
            # split on option char:
            option, value = line.split(OPTION_CHAR, 1)
            # strip spaces:
            option = option.strip()
            value = value.strip()
            # store in dictionary:
            options[option] = value
    f.close()
    return options

def extract_values(options):
    global FONT
    global FONT_SIZE
    global FONT_BOLD
    global BAR_WIDTH
    global BAR_SPACING
    global COLOR1
    global COLOR2
    global COLOR3
    global COLOR4
    global COLOR5
    global COLOR6
    global COLOR7
    global COLOR8
    global COLOR9
    global COLOR10
    global PALETTE_CHOICE
    global VIS_COLOR
    global PATTERN
    global ORDER
    global SHOW_OPTIONS
    global CURRENT_TAB

    for item in options:
        if item == "font":
            FONT = options[item]
        if item == "font_size":
            FONT_SIZE = int(options[item])
        if item == "font_bold":
            if item == "True":
                FONT_BOLD = "bold"
            if item == "False":
                FONT_BOLD = ""
        if item == "bar_width":
            BAR_WIDTH = int(options[item])
        if item == "bar_spacing":
            BAR_SPACING = int(options[item])
        if item == "color1":
            COLOR1 = options[item]
        if item == "color2":
            COLOR2 = options[item]
        if item == "color3":
            COLOR3 = options[item]
        if item == "color4":
            COLOR4 = options[item]
        if item == "color5":
            COLOR5 = options[item]
        if item == "color6":
            COLOR6 = options[item]
        if item == "color7":
            COLOR7 = options[item]
        if item == "color8":
            COLOR8 = options[item]
        if item == "color9":
            COLOR9 = options[item]
        if item == "color10":
            COLOR10 = options[item]
        if item == "palette_choice":
            PALETTE_CHOICE = options[item]
        if item == "visible_color":
            VIS_COLOR = int(options[item])
        if item == "color_pattern":
            PATTERN = options[item]
        if item == "order":
            ORDER = options[item]
        if item == "show_options":
            SHOW_OPTIONS = int(options[item])
        if item == "current_tab":
            CURRENT_TAB = int(options[item])

def update_palette():
    global PALETTE
    PALETTE = []
    if PALETTE_CHOICE == "Purple & Teal":
        PALETTE.append(COLOR1)
        PALETTE.append(COLOR2)
        PALETTE.append(COLOR3)
        PALETTE.append(COLOR4)
        PALETTE.append(COLOR5)
    elif PALETTE_CHOICE == "Red & Blue":
        PALETTE.append(COLOR6)
        PALETTE.append(COLOR7)
        PALETTE.append(COLOR8)
        PALETTE.append(COLOR9)
        PALETTE.append(COLOR10)

def text_splitter(string, cutlength, cutcharacter):
    stringlist=[]
    if len(string) > cutlength:
        while len(string) > cutlength:
            string += cutcharacter
            i = 1
            if len(string) > cutlength:
                if string[cutlength-1] == cutcharacter:
                    stringlist.append(string[:cutlength].strip())
                    string = string[cutlength:-1]
                else:
                    while string[cutlength+i] != cutcharacter:
                        i += 1
                    stringlist.append(string[:cutlength+i])
                    string = string[cutlength+i+1:-1]
        stringlist.append(string)
    else:
        stringlist.append(string)
    return stringlist

def load_file(filename):
    global TEXT
    global TEXT_INDEX

    fileHandle = open(filename, 'r')
    text = fileHandle.read()
    fileHandle.close()

    TEXT = text_splitter(text, 3000, " ")
    TEXT_INDEX = 0

def create_options_dict():
    options = {}
    options["font"] = FONT
    options["font_size"] = str(FONT_SIZE)
    if FONT_BOLD == "bold":
        options["font_bold"] = "True"
    elif FONT_BOLD == "":
        options["font_bold"] = "False"
    options["bar_width"] = str(BAR_WIDTH)
    options["bar_spacing"] = str(BAR_SPACING)
    options["color1"] = COLOR1
    options["color2"] = COLOR2
    options["color3"] = COLOR3
    options["color4"] = COLOR4
    options["color5"] = COLOR5
    options["color6"] = COLOR6
    options["color7"] = COLOR7
    options["color8"] = COLOR8
    options["color9"] = COLOR9
    options["color10"] = COLOR10
    options["palette_choice"] = PALETTE_CHOICE
    options["visible_color"] = str(VIS_COLOR)
    options["color_pattern"] = PATTERN
    options["order"] = ORDER
    options["show_options"] = str(SHOW_OPTIONS)
    options["current_tab"] = str(CURRENT_TAB)
    return options

class QuitDialogue(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, padx=6, pady=6)

        self.focus()
        self.resizable(0,0)
        self.parent = args[0]

        self.label = tkinter.ttk.Label(self, text="Save current settings?")
        self.save_button = tkinter.ttk.Button(self, text="Save", takefocus=False, command=self.save_new_config)
        self.dont_save_button = tkinter.ttk.Button(self, text="Don't save", takefocus=False, command=self.parent.destroy)
        self.cancel_button = tkinter.ttk.Button(self, text="Cancel", takefocus=False, command=self.destroy)

        self.label.grid(row=0, column=0, columnspan=3, pady=(9,15))
        self.save_button.grid(row=1, column=2)
        self.dont_save_button.grid(row=1, column=1, padx=(0,6))
        self.cancel_button.grid(row=1, column=0, padx=(0,6))

    def save_new_config(self):
        filehandle = open("files/config.txt", "w")
        for key, value in list(END_OPTIONS.items()):
            filehandle.write(key + " = " + value +"\n")
        filehandle.close()
        self.parent.destroy()

start()