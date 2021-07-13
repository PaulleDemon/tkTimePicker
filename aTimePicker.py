import tkinter

from clock import clock
from digitalpicker import spintimepicker

HOURS12 = 0
HOURS24 = 1


class AnalogPicker(tkinter.Frame):

    def __init__(self, parent, type=HOURS12):
        super(AnalogPicker, self).__init__(parent)

        self.type = type

        self.hrs_canvas = tkinter.Canvas(self)
        self.min_canvas = tkinter.Canvas(self)

        self.hours_picker = clock.HoursClock(self.hrs_canvas, type)
        self.minutes_picker = clock.MinutesClock(self.min_canvas)

        self.hours_picker.bind("<<HoursChanged>>", self.toggle)
        self.hours_picker.bind("<<HoursChanged>>", self.setHours)
        self.minutes_picker.bind("<<MinChanged>>", self.toggle)
        self.minutes_picker.bind("<<MinChanged>>", self.setMinutes)

        self.spinPicker = spintimepicker.SpinTimePickerModern(self)
        self.spinPicker.bind("<<Hrs12Clicked>>", self.displayHrs)
        self.spinPicker.bind("<<Hrs24Clicked>>", self.displayHrs)
        self.spinPicker.bind("<<MinClicked>>", self.displayMin)

        self.spinPicker.pack_all(type)

        self.hrs_displayed = True

        self.spinPicker.pack(expand=True, fill='both')
        self.displayHrs()

    def toggle(self, event=None):
        self.hrs_displayed = not self.hrs_displayed

        if not self.hrs_displayed:
            self.displayMin()

    def displayMin(self, event=None):
        self.hrs_canvas.pack_forget()
        self.min_canvas.pack(expand=True, fill='both')

    def displayHrs(self, event=None):
        self.min_canvas.pack_forget()
        self.hrs_canvas.pack(expand=True, fill='both')

    def setMinutes(self, event=None):
        self.spinPicker.setMins(self.minutes_picker.getMinutes())

    def setHours(self, event=None):
        hrs = int(self.hours_picker.getHours())
        print(f"hours: {hrs}")
        if self.type == HOURS12:
            self.spinPicker.set12Hrs(hrs)

        else:
            self.spinPicker.set24Hrs(hrs)


if __name__ == "__main__":
    root = tkinter.Tk()

    time_picker = AnalogPicker(root)
    time_picker.pack(expand=1, fill='both')

    tkinter.Button(root, text="YES").pack()

    root.mainloop()
