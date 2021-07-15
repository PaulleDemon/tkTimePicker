import tkinter

from timepicker import constants
from timepicker.analogpicker import clock
from timepicker.spinpicker import spintimepicker


class AnalogPicker(tkinter.Frame):

    def __init__(self, parent, type=constants.HOURS12, per_orient=constants.VERTICAL, period=constants.AM):
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

        self.spinPicker.addAll(type)

        self.hrs_displayed = True

        self.spinPicker.pack(expand=True, fill="both")
        self.displayHrs()

    def toggle(self, event=None):
        self.hrs_displayed = not self.hrs_displayed

        if not self.hrs_displayed:
            self.displayMin()

    def displayMin(self, event=None):
        self.hrs_canvas.pack_forget()
        self.min_canvas.pack(expand=True, fill="both")

    def displayHrs(self, event=None):
        self.min_canvas.pack_forget()
        self.hrs_canvas.pack(expand=True, fill="both")

    def setMinutes(self, event=None):
        self.spinPicker.setMins(self.minutes_picker.getMinutes())

    def setHours(self, event=None):
        hrs = int(self.hours_picker.getHours())

        if self.type == constants.HOURS12:
            self.spinPicker.set12Hrs(hrs)

        else:
            self.spinPicker.set24Hrs(hrs)

    def configAnalog(self, canvas_bg="", **kwargs):
        self.hours_picker.configure(**kwargs)
        self.minutes_picker.configure(**kwargs)

        if canvas_bg:
            self.min_canvas.configure(bg=canvas_bg)
            self.hrs_canvas.configure(bg=canvas_bg)

    def configSpin(self, **kwargs):
        self.spinPicker.configureAll(**kwargs)

        for x in ("hovercolor", "hoverbg", "clickedcolor", "clickedbg"):
            if x in kwargs:
                kwargs.pop(x)

        self.spinPicker.configure_seprator(**kwargs)

    def configAnalogHrs(self, canvas_bg="", **kwargs):
        self.hours_picker.configure(**kwargs)

        if canvas_bg:
            self.hrs_canvas.configure(bg=canvas_bg)

    def configAnalogMins(self, canvas_bg="", **kwargs):
        self.minutes_picker.configure(**kwargs)

        if canvas_bg:
            self.min_canvas.configure(bg=canvas_bg)

    def configSpinHrs(self, **kwargs):
        self.spinPicker.configure_12HrsTime(**kwargs)
        self.spinPicker.configure_24HrsTime(**kwargs)

    def configSpinMins(self, **kwargs):
        self.spinPicker.configure_minute(**kwargs)

    def configSeperator(self, **kwargs):
        self.spinPicker.configure_seprator(**kwargs)

    def configurePeriod(self, **kwargs):
        self.spinPicker.configure_period(**kwargs)

    def hours(self) -> int:
        if self.type == constants.HOURS12:
            return self.spinPicker.hours12()

        else:
            return self.spinPicker.hours24()

    def minutes(self) -> int:
        return self.spinPicker.minutes()

    def period(self) -> str:
        return self.spinPicker.period()

    def time(self) -> tuple[int, int, str]:
        return self.hours(), self.minutes(), self.period()


class AnalogThemes:

    def __init__(self, timepicker: AnalogPicker):
        self.time_picker = timepicker

    def setNavyBlue(self):
        self.time_picker.configAnalog(headcolor="#009688", handcolor="#009688", bg="#eeeeee",
                                      clickedcolor="#ffffff", textcolor="#000000", canvas_bg="#ffffff",
                                      alttextwidth=2, bdwidth=0)

        self.time_picker.configSpin(bg="#009688", height=2, fg="#ffffff", font=("Times", 16), hoverbg="#00695f",
                                    hovercolor="#b6cbd1", clickedbg="#00695f", clickedcolor="#ffffff")

        self.time_picker.configSeperator(font=("Times", 18, "bold"), width=1)

    def setDracula(self):
        self.time_picker.configAnalog(headcolor="#863434", handcolor="#863434", bg="#363636",
                                      clickedcolor="#ffffff", textcolor="#ffffff", canvas_bg="#404040",
                                      alttextwidth=2, bdwidth=0)

        self.time_picker.configSpin(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",
                                    hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")

        self.time_picker.configSeperator(font=("Times", 18, "bold"), width=1)

    def setPurple(self):
        self.time_picker.configAnalog(headcolor="#ee333d", handcolor="#ee333d", bg="#71135c",
                                      clickedcolor="#ffffff", textcolor="#ffffff", canvas_bg="#4e0d3a",
                                      alttextwidth=2, bdwidth=0)

        self.time_picker.configSpin(bg="#71135c", height=2, fg="#ffffff", font=("Times", 16), hoverbg="#3d0430",
                                    hovercolor="#ffffff", clickedbg="#ad118c", clickedcolor="#ffffff")
        self.time_picker.configSeperator(font=("Times", 18, "bold"), width=1)
