from Tkinter import *
import ttk
from files import cnfg


class CalibrateMenu(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, padx=9, pady=9)

        self.focus()

        self.resizable(0,0)
        self.parent = args[0]

        self.instructions_label = ttk.Label(self, text="Click on the colors you wish to calibrate.", padding=(0,6,0,9))
        self.calibrate_purpteal_button = ttk.Button(self, text="Purple & Teal", takefocus=False, command=self.parent.calib_purpleteal)
        self.calibrate_redblue_button = ttk.Button(self, text="Red & Blue", takefocus=False, command=self.parent.calib_redblue)
        self.finished_button = ttk.Button(self, text="Finished", takefocus=False, command=self.destroy)
        self.blank_label = ttk.Label(self, text=" ")

        self.instructions_label.grid(row=0, column=0, columnspan=2)
        self.calibrate_purpteal_button.grid(row=1, column=0)
        self.calibrate_redblue_button.grid(row=1, column=1)
        self.blank_label.grid(row=2, column=0, columnspan=2)
        self.finished_button.grid(row=3, column=0, columnspan=2)

class PTCalibrate(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, padx=6, pady=6)

        self.focus()
        self.resizable(0,0)

        self.parent = args[0]

        self.get_color_values()

        self.purple_frame = PurpleCalibFrame(self)
        self.teal_frame = TealCalibFrame(self)
        self.black_frame = BlackCalibFrame(self)

        self.teal_frame.grid(row=0, column=0)
        self.teal_frame.grid_remove()
        self.black_frame.grid(row=0, column=0)
        self.black_frame.grid_remove()
        self.purple_frame.grid(row=0, column=0)

    def cancel_click(self):
        self.destroy()

    def get_color_values(self):
        self.magenta = "#FF00FF"
        self.teal = "#00FFFF"
        self.gray = "#7F7F7F"
        self.black = "#000000"

    def set_color_values(self):
        cnfg.COLOR1 = self.purple_frame.newpurple
        cnfg.COLOR2 = self.teal_frame.newteal
        cnfg.COLOR3 = self.gray
        cnfg.COLOR4 = self.black_frame.newblack

class PurpleCalibFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.parent = args[0]
        self.newpurple = self.parent.magenta

        # lens label
        self.lens_label = ttk.Label(self, text="Look through the RED lens", font="Helvetica 16 bold", background="red")

        # canvas example and slider
        self.adjuster_frame = ttk.Frame(self)
        self.canvas_example = Canvas(self.adjuster_frame, width=400, height=130, background=self.parent.gray)
        self.create_canvas_text()
        self.scale_var = IntVar(value=255)
        self.scale = ttk.Scale(self.adjuster_frame, orient=HORIZONTAL, length=400, from_=0.0, to=255.0, variable=self.scale_var, command=self.scale_change)
        self.canvas_example.grid(row=0, column=0, padx=(10,10), pady=(10,0))
        self.scale.grid(row=2, column=0, pady=(3,0))

        # intstructions label
        self.instructions_label = ttk.Label(self, wraplength=400, text="Adjust the slider until the letters disappear. Press 'Next' when finished.")

        # buttons
        self.button_frame = ttk.Frame(self)
        self.next_button = ttk.Button(self.button_frame, text="Next", takefocus=False, command=self.next_click)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", takefocus=False, command=self.parent.cancel_click)
        self.cancel_button.grid(row=0, column=0, padx=(0,6))
        self.next_button.grid(row=0, column=1)

        self.lens_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=(20,0), pady=(5,0))
        self.adjuster_frame.grid(row=1, column=0, columnspan=2)
        self.instructions_label.grid(row=2, column=0, columnspan=2, pady=(3,6))
        self.button_frame.grid(row=3, column=1, sticky="E", padx=7, pady=(5,3))

    def next_click(self):
        self.grid_remove()
        self.parent.teal_frame.grid()

    def scale_change(self, *args):
        rb = hex(self.scale_var.get())
        if len(rb) == 3:
            rb = "0" + rb[2:]
        else:
            rb = rb[2:]
        self.newpurple = "#" + rb + "00" + rb
        self.canvas_example.itemconfig(self.canvas_text, fill=self.newpurple)

    def create_canvas_text(self):
        try:
            self.canvas_example.delete(self.bar_text)
        except:
            pass
        self.canvas_text = self.canvas_example.create_text(200, 66, anchor="center")
        self.canvas_example.itemconfig(self.canvas_text, text="Abcdef")
        self.canvas_example.itemconfig(self.canvas_text, font=("Helvetica", 72, "bold"), fill=self.parent.magenta)

class TealCalibFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.parent = args[0]
        self.newteal = self.parent.teal

        # lens label
        self.lens_label = ttk.Label(self, text="Look through the BLUE /GREEN lens", font="Helvetica 16 bold", background="#3232FF")

        # canvas example and slider
        self.adjuster_frame = ttk.Frame(self)
        self.canvas_example = Canvas(self.adjuster_frame, width=400, height=130, background=self.parent.gray)
        self.create_canvas_text()
        self.scale_var = IntVar(value=255)
        self.scale = ttk.Scale(self.adjuster_frame, orient=HORIZONTAL, length=400, from_=0.0, to=255.0, variable=self.scale_var, command=self.scale_change)
        self.canvas_example.grid(row=0, column=0, padx=(10,10), pady=(10,0))
        self.scale.grid(row=2, column=0, pady=(3,0))

        # intstructions label
        self.instructions_label = ttk.Label(self, wraplength=400, text="Adjust the slider until the letters disappear. Press 'Next' when finished.")

        # buttons
        self.button_frame = ttk.Frame(self)
        self.next_button = ttk.Button(self.button_frame, text="Next", takefocus=False, command=self.next_click)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", takefocus=False, command=self.parent.cancel_click)
        self.cancel_button.grid(row=0, column=0, padx=(0,6))
        self.next_button.grid(row=0, column=1)

        self.lens_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=(20,0), pady=(5,0))
        self.adjuster_frame.grid(row=1, column=0, columnspan=2)
        self.instructions_label.grid(row=2, column=0, columnspan=2, pady=(3,6))
        self.button_frame.grid(row=3, column=1, sticky="E", padx=7, pady=(5,3))

    def next_click(self):
        self.grid_remove()
        self.parent.black_frame.grid()

    def scale_change(self, *args):
        gb = hex(self.scale_var.get())
        if len(gb) == 3:
            gb = "0" + gb[2:]
        else:
            gb = gb[2:]
        self.newteal = "#" + "00" + gb + gb
        self.canvas_example.itemconfig(self.canvas_text, fill=self.newteal)
        self.parent.black_frame.canvas_example.configure(background=self.newteal)

    def create_canvas_text(self):
        try:
            self.canvas_example.delete(self.bar_text)
        except:
            pass
        self.canvas_text = self.canvas_example.create_text(200, 66, anchor="center")
        self.canvas_example.itemconfig(self.canvas_text, text="Abcdef")
        self.canvas_example.itemconfig(self.canvas_text, font=("Helvetica", 72, "bold"), fill=self.parent.teal)

class BlackCalibFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.parent = args[0]
        self.newblack = "#FFFFFF"

        # lens label
        self.lens_label = ttk.Label(self, text="Look through the RED lens", font="Helvetica 16 bold", background="red")

        # canvas example and slider
        self.adjuster_frame = ttk.Frame(self)
        self.canvas_example = Canvas(self.adjuster_frame, width=400, height=130, background=self.parent.teal_frame.newteal)
        self.create_canvas_text()
        self.scale_var = IntVar(value=255)
        self.scale = ttk.Scale(self.adjuster_frame, orient=HORIZONTAL, length=400, from_=0.0, to=255.0, variable=self.scale_var, command=self.scale_change)
        self.canvas_example.grid(row=0, column=0, padx=(10,10), pady=(10,0))
        self.scale.grid(row=2, column=0, pady=(3,0))

        # intstructions label
        self.instructions_label = ttk.Label(self, wraplength=400, text="Adjust the slider until the letters disappear. Press 'Finish' when finished.")

        # buttons
        self.button_frame = ttk.Frame(self)
        self.finish_button = ttk.Button(self.button_frame, text="Finish", takefocus=False, command=self.finish_click)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", takefocus=False, command=self.parent.cancel_click)
        self.cancel_button.grid(row=0, column=0, padx=(0,6))
        self.finish_button.grid(row=0, column=1)

        self.lens_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=(20,0), pady=(5,0))
        self.adjuster_frame.grid(row=1, column=0, columnspan=2)
        self.instructions_label.grid(row=2, column=0, columnspan=2, pady=(3,6))
        self.button_frame.grid(row=3, column=1, sticky="E", padx=7, pady=(5,3))

    def finish_click(self):
        self.parent.set_color_values()
        self.parent.parent.parent.content.palette_click()
        self.parent.destroy()

    def scale_change(self, *args):
        rgb = hex(self.scale_var.get())
        if len(rgb) == 3:
            rgb = "0" + rgb[2:]
        else:
            rgb = rgb[2:]
        self.newblack = "#" + rgb + rgb + rgb
        self.canvas_example.itemconfig(self.canvas_text, fill=self.newblack)

    def create_canvas_text(self):
        try:
            self.canvas_example.delete(self.bar_text)
        except:
            pass
        self.canvas_text = self.canvas_example.create_text(200, 66, anchor="center")
        self.canvas_example.itemconfig(self.canvas_text, text="Abcdef")
        self.canvas_example.itemconfig(self.canvas_text, font=("Helvetica", 72, "bold"), fill="white")