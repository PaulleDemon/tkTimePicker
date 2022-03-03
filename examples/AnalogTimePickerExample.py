import tkinter as tk

from tktimepicker import AnalogPicker, AnalogThemes, constants


def updateTime(time):
    time_lbl.configure(text="{}:{} {}".format(*time)) # remove 3rd flower bracket in case of 24 hrs time


def get_time():

    top = tk.Toplevel(root)

    time_picker = AnalogPicker(top, type=constants.HOURS12)
    time_picker.pack(expand=True, fill="both")

    theme = AnalogThemes(time_picker)
    # theme.setDracula()
    # theme.setNavyBlue()
    theme.setPurple()
    ok_btn = tk.Button(top, text="ok", command=lambda: updateTime(time_picker.time()))
    ok_btn.pack()


root = tk.Tk()

time = ()

time_lbl = tk.Label(root, text="Time:")
time_lbl.pack()

time_btn = tk.Button(root, text="Get Time", command=get_time)
time_btn.pack()

root.mainloop()
