from Tkinter import *
import ttk
from files import cnfg

class RBCalibrate(Toplevel):
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, padx=6, pady=6)

        self.focus()
        self.resizable(0,0)

        self.parent = args[0]

        self.get_color_values()

        self.black_frame = BlackCalibFrame(self)
        self.red_frame = RedCalibFrame(self)

        self.red_frame.grid(row=0, column=0)
        self.red_frame.grid_remove()
        self.black_frame.grid(row=0, column=0)

    def cancel_click(self):
        self.destroy()

    def get_color_values(self):
        self.red = "#FF0000"
        self.blue = "#0000FF"
        self.gray = "#7F7F7F"
        self.black = "#7F7F7F"

    def set_color_values(self):
        cnfg.COLOR6 = self.red_frame.newred
        cnfg.COLOR7 = self.blue
        cnfg.COLOR8 = self.black_frame.newblack
        cnfg.COLOR9 = self.gray
        cnfg.COLOR10 = cnfg.add_two_colors(cnfg.COLOR6, cnfg.COLOR7)

class BlackCalibFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.parent = args[0]
        self.newblack = self.parent.black

        # lens label
        self.lens_label = ttk.Label(self, text="Look through the RED lens", font="Helvetica 16 bold", background="red")

        # canvas example and slider
        self.adjuster_frame = ttk.Frame(self)
        self.canvas_example = Canvas(self.adjuster_frame, width=400, height=130, background=self.parent.blue)
        self.create_canvas_text()
        self.scale_var = IntVar(value=128)
        self.scale = ttk.Scale(self.adjuster_frame, orient=HORIZONTAL, length=400, from_=0.0, to=128.0, variable=self.scale_var, command=self.scale_change)
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
        self.parent.red_frame.grid()

    def scale_change(self, *args):
        rgb = hex(self.scale_var.get())
        if len(rgb) == 3:
            rgb = "0" + rgb[2:]
        else:
            rgb = rgb[2:]
        self.newblack = "#" + rgb + rgb + rgb
        self.canvas_example.itemconfig(self.canvas_text, fill=self.newblack)
        self.parent.red_frame.canvas_example.configure(background=self.newblack)

    def create_canvas_text(self):
        try:
            self.canvas_example.delete(self.bar_text)
        except:
            pass
        self.canvas_text = self.canvas_example.create_text(200, 66, anchor="center")
        self.canvas_example.itemconfig(self.canvas_text, text="Abcdef")
        self.canvas_example.itemconfig(self.canvas_text, font=("Helvetica", 72, "bold"), fill=self.parent.black)

class RedCalibFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        self.parent = args[0]
        self.newred = self.parent.red

        self.r = "FF"
        self.gb = "80"

        # lens label
        self.lens_label = ttk.Label(self, text="Look through the BLUE /GREEN lens", font="Helvetica 16 bold", background="#3232FF")

        # canvas example and slider
        self.adjuster_frame = ttk.Frame(self)
        self.canvas_example = Canvas(self.adjuster_frame, width=400, height=130, background=self.parent.black_frame.newblack)
        self.create_canvas_text()
        self.scale_var = IntVar(value=383)
        self.scale = ttk.Scale(self.adjuster_frame, orient=HORIZONTAL, length=400, from_=0.0, to=383.0, variable=self.scale_var, command=self.scale_change)
        self.canvas_example.grid(row=0, column=0, padx=(10,10), pady=(10,0))
        self.scale.grid(row=2, column=0, pady=(3,0))
        self.scale_change()

        # intstructions label
        self.instructions_label = ttk.Label(self, wraplength=400, text="Adjust the slider until the letters disappear. Press 'Finish' when finished.")

        # ghost image problems
#        self.red_ghost_var = IntVar(value=0)
#        self.red_ghost_checkbutton = ttk.Checkbutton(self, text="Help! The letters won't disappear because of a red ghost image.", takefocus=False, var=self.red_ghost_var, command=self.red_ghost_click)
#        self.optional_instructions_frame = ttk.Frame(self)
#        self.optional_instructions_label = ttk.Label(self.optional_instructions_frame, wraplength=300, text=("Adjust the above slider until the letters are as close to inivisble as possible. "
#            + "Then use the slider below to reduce the color content of the letters until they are as close to invisible as possible. Repeat these two steps until the letters disappear."))
#        self.optional_slider_var = IntVar(value=0)
#        self.optional_slider = ttk.Scale(self.optional_instructions_frame, orient=HORIZONTAL, length=300, from_=127.0, to=0.0, variable=self.optional_slider_var, command=self.options_scale_change)
#        self.optional_instructions_label.grid(row=0, column=0)
#        self.optional_slider.grid(row=1, column=0)

        # button
        self.button_frame = ttk.Frame(self)
        self.finish_button = ttk.Button(self.button_frame, text="Finish", takefocus=False, command=self.finish_click)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", takefocus=False, command=self.parent.cancel_click)
        self.cancel_button.grid(row=0, column=0, padx=(0,6))
        self.finish_button.grid(row=0, column=1)

        self.lens_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=(20,0), pady=(5,0))
        self.adjuster_frame.grid(row=1, column=0, columnspan=2)
        self.instructions_label.grid(row=2, column=0, columnspan=2, pady=(3,6))
#        self.red_ghost_checkbutton.grid(row=3, column=0, columnspan=2)
#        self.optional_instructions_frame.grid(row=4, column=0, columnspan=2)
#        self.optional_instructions_frame.grid_remove()
        self.button_frame.grid(row=5, column=1, sticky="E", padx=7, pady=(5,3))



#    def red_ghost_click(self):
#        if self.red_ghost_var.get() == 0:
#            self.optional_instructions_frame.grid_remove()
#        elif self.red_ghost_var.get() == 1:
#            self.optional_instructions_frame.grid()

    def finish_click(self):
        self.parent.set_color_values()
        self.parent.parent.parent.content.palette_click()
        self.parent.destroy()

    def scale_change(self, *args):
        if self.scale_var.get() <= 255:
            self.r = hex(self.scale_var.get())
            if len(self.r) == 3:
                self.r = "0" + self.r[2:]
            else:
                self.r = self.r[2:]
            self.newred = "#" + self.r + self.gb + self.gb
            self.canvas_example.itemconfig(self.canvas_text, fill=self.newred)
        elif self.scale_var.get() > 255:
            self.gb = hex(self.scale_var.get()-256)
            if len(self.gb) == 3:
                self.gb = "0" + self.gb[2:]
            else:
                self.gb = self.gb[2:]
            self.newred = "#" + self.r + self.gb + self.gb
            self.canvas_example.itemconfig(self.canvas_text, fill=self.newred)

        try:
            if self.scale_var.get() > 255:
                self.optional_slider_var.set(int(self.gb,16))
        except:
            pass

#    def options_scale_change(self, *args):
#        self.gb = hex(self.optional_slider_var.get())
#        if len(self.gb) == 3:
#            self.gb = "0" + self.gb[2:]
#        else:
#            self.gb = self.gb[2:]
#        self.newred = "#" + self.r + self.gb + self.gb
#        self.canvas_example.itemconfig(self.canvas_text, fill=self.newred)
#
#        if self.scale_var.get() > 255:
#            self.scale_var.set(int(self.gb,16)+255)

    def create_canvas_text(self):
        try:
            self.canvas_example.delete(self.bar_text)
        except:
            pass
        self.canvas_text = self.canvas_example.create_text(200, 66, anchor="center")
        self.canvas_example.itemconfig(self.canvas_text, text="Abcdef")
        self.canvas_example.itemconfig(self.canvas_text, font=("Helvetica", 72, "bold"), fill=self.parent.red)