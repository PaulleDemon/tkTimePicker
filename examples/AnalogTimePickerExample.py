import tkinter as tk
from timepicker import clockTimePicker


def updateTime(time):
    time_lbl.configure(text="{}:{} {}".format(*time))


def get_time():

    top = tk.Toplevel(root)

    time_picker = clockTimePicker.AnalogPicker(top)
    time_picker.pack(expand=True, fill="both")

    theme = clockTimePicker.AnalogThemes(time_picker)
    theme.setDracula()
    # theme.setNavyBlue()
    # theme.setPurple()
    ok_btn = tk.Button(top, text="ok", command=lambda: updateTime(time_picker.time()))
    ok_btn.pack()


root = tk.Tk()

time = ()

time_lbl = tk.Label(root, text="Time:")
time_lbl.pack()

time_btn = tk.Button(root, text="Get Time", command=get_time)
time_btn.pack()

root.mainloop()
