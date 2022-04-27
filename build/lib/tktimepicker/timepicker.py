import tkinter

from typing import Tuple
from tkinter import ttk
from tktimepicker import basetimepicker
from tktimepicker import constants
from tktimepicker.spinlabel import SpinLabel, LabelGroup, PeriodLabel


class AnalogPicker(tkinter.Frame):  # Creates the fully functional clock timepicker

    def __init__(self, parent, type=constants.HOURS12, per_orient=constants.VERTICAL, period=constants.AM):
        super(AnalogPicker, self).__init__(parent)
        self.type = type

        self.hrs_canvas = tkinter.Canvas(self)
        self.min_canvas = tkinter.Canvas(self)

        self.hours_picker = basetimepicker.HoursClock(self.hrs_canvas, type)
        self.minutes_picker = basetimepicker.MinutesClock(self.min_canvas)

        self.hours_picker.bind("<<HoursChanged>>", self.setSpinHours)
        self.minutes_picker.bind("<<MinChanged>>", self.setSpinMinutes)

        self.spinPicker = SpinTimePickerModern(self, per_orient=per_orient, period=period)
        self.spinPicker.bind("<<Hrs12Clicked>>", self.displayHrs)
        self.spinPicker.bind("<<Hrs24Clicked>>", self.displayHrs)
        self.spinPicker.bind("<<MinClicked>>", self.displayMin)

        self.spinPicker.addAll(type)

        self.hrs_displayed = True

        self.spinPicker.pack(expand=True, fill="both")
        self.displayHrs()

    def toggle(self, event=None):  # not used
        self.hrs_displayed = not self.hrs_displayed

        if not self.hrs_displayed:
            self.displayMin()

    def displayMin(self, event=None):
        self.hrs_canvas.pack_forget()
        self.min_canvas.pack(expand=True, fill="both")

    def displayHrs(self, event=None):
        self.min_canvas.pack_forget()
        self.hrs_canvas.pack(expand=True, fill="both")

    def setHours(self, hrs: int):
        self.hours_picker.setHours(hrs)
        
        if self.type == constants.HOURS12:
            self.spinPicker.set12Hrs(hrs)

        else:
            self.spinPicker.set24Hrs(hrs)

    def setMinutes(self, mins: int):
        self.minutes_picker.setMinutes(mins)
        self.spinPicker.setMins(mins)

    def setSpinMinutes(self, event=None):
        self.spinPicker.setMins(self.minutes_picker.getMinutes())

    def setSpinHours(self, event=None):
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

        self.spinPicker.configure_separator(**kwargs)

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

    def configSeparator(self, **kwargs):
        self.spinPicker.configure_separator(**kwargs)

    def configurePeriod(self, **kwargs):
        self.spinPicker.configure_period(**kwargs)

    def hours(self) -> int:
        """ returns hours in 12 hours clock if set to 12 hours else hours in 24 hour clock will be returned """
        if self.type == constants.HOURS12:
            return self.spinPicker.hours12()

        else:
            return self.spinPicker.hours24()

    def minutes(self) -> int:
        """ returns minutes """
        return self.spinPicker.minutes()

    def period(self) -> str:
        """ returns period """
        return self.spinPicker.period()

    def time(self) -> Tuple[int, int, str]:
        """ returns hours, minutes and period """
        return self.hours(), self.minutes(), self.period()


class SpinTimePickerOld(basetimepicker.SpinBaseClass):

    def __init__(self, parent, orient=constants.HORIZONTAL):
        super(SpinTimePickerOld, self).__init__(parent)

        self.hour_type = constants.HOURS12
        self.orient = "top" if orient == constants.VERTICAL else "left"

        reg12hrs = self.register(self.validate12hrs)
        reg24hrs = self.register(self.validate24hrs)
        regMin = self.register(self.validateMinutes)

        self.period_var = tkinter.StringVar(self, value="a.m")
        self.period_var.trace("w", self.validatePeriod)

        self._12HrsTime = tkinter.Spinbox(self, increment=1, from_=1, to=12,
                                          validate="all", validatecommand=(reg12hrs, "%P"),
                                          command=lambda: self._12HrsTime.event_generate("<<Changed12Hrs>>"))

        self._24HrsTime = tkinter.Spinbox(self, increment=1, from_=0, to=23,
                                          validate="all", validatecommand=(reg24hrs, "%P"),
                                          command=lambda: self._24HrsTime.event_generate("<<Changed24Hrs>>"))

        self._minutes = tkinter.Spinbox(self, increment=1, from_=0, to=59,
                                        validate="all", validatecommand=(regMin, "%P"),
                                        command=lambda: self._minutes.event_generate("<<ChangedMins>>"))

        self._period = ttk.Combobox(self, values=["a.m", "p.m"], textvariable=self.period_var)
        self._period.bind("<<ComboboxSelected>>", lambda a: self._minutes.event_generate("<<ChangedPeriod>>"))

    def addHours12(self):
        self._12HrsTime.pack(expand=True, fill="both", side=self.orient)

    def addHours24(self):
        self._24HrsTime.pack(expand=True, fill="both", side=self.orient)

    def addMinutes(self):
        self._minutes.pack(expand=True, fill="both", side=self.orient)

    def addPeriod(self):
        self._period.pack(expand=True, fill="both", side=self.orient)

    def validate12hrs(self, value):
        return value.isdigit() and (0 <= int(value) <= 12) or value == ""

    def validate24hrs(self, value):
        return value.isdigit() and (0 <= int(value) <= 23) or value == ""

    def validateMinutes(self, value):
        return value.isdigit() and (0 <= int(value) <= 59) or value == ""

    def validatePeriod(self, *value):

        period_value = self.period_var.get()

        if period_value.lower() == "a":
            self.period_var.set("a.m")

        elif period_value.lower() == "p":
            self.period_var.set("p.m")

        elif period_value in ["a.m", "p.m"]:
            pass

        else:
            self.period_var.set("")

        self._period.icursor("end")

    def addAll(self, hours: int, separator: bool = True):

        if hours == constants.HOURS12:
            self.addHours12()

        elif hours == constants.HOURS24:
            self.addHours24()

        else:
            raise ValueError(f"Unknown type '{hours}'. Use either 0/1")

        self.hour_type = hours

        if separator:
            self._separator.pack(expand=True, fill='both', side=self.orient)

        self.addMinutes()

        if hours == constants.HOURS12:
            self.addPeriod()

    def hours(self) -> int:
        """ returns hours in 12 hours clock if set to 12 hours else hours in 24 hour clock will be returned """
        if self.hour_type == constants.HOURS12:
            return self.hours12()

        else:
            return self.hours24()

    def hours12(self) -> int:
        """ returns hours in 12 hours clock """
        return int(self._12HrsTime.get())

    def hours24(self) -> int:
        """ returns hours in 24 hours clock """
        return int(self._24HrsTime.get())

    def minutes(self) -> int:
        """ returns minutes """
        return int(self._minutes.get())

    def period(self) -> str:
        """ returns period """
        return self._period.get()

    def time(self) -> Tuple[int, int, str]:
        """ returns hours minutes and period """
        return self.hours(), self.minutes(), self.period()


class SpinTimePickerModern(basetimepicker.SpinBaseClass):

    def __init__(self, parent, orient=constants.HORIZONTAL, per_orient=constants.VERTICAL, period=constants.AM):
        super(SpinTimePickerModern, self).__init__(parent)

        self.hour_type = constants.HOURS12
        self.orient = "top" if orient == constants.VERTICAL else "left"

        self._12HrsTime = SpinLabel(master=self, min=1, max=12)
        self._12HrsTime.bind("<<valueChanged>>", lambda a: self._12HrsTime.event_generate("<<Changed12Hrs>>"))
        self._12HrsTime.bind("<Button-1>", lambda a: self.event_generate("<<Hrs12Clicked>>"))

        self._24HrsTime = SpinLabel(master=self, min=0, max=23)
        self._24HrsTime.bind("<<valueChanged>>", lambda a: self._12HrsTime.event_generate("<<Changed24Hrs>>"))
        self._24HrsTime.bind("<Button-1>", lambda a: self.event_generate("<<Hrs24Clicked>>"))

        self._minutes = SpinLabel(master=self, min=0, max=59)
        self._minutes.bind("<<valueChanged>>", lambda a: self._minutes.event_generate("<<ChangedMins>>"))
        self._minutes.bind("<Button-1>", lambda a: self.event_generate("<<MinClicked>>"))

        self._period = PeriodLabel(self, period, per_orient)

        self.spinlblGroup = LabelGroup()

    def addHours12(self):
        self._12HrsTime.pack(expand=True, fill="both", side=self.orient)
        self.spinlblGroup.add(self._12HrsTime)

    def addHours24(self):
        self._24HrsTime.pack(expand=True, fill="both", side=self.orient)
        self.spinlblGroup.add(self._24HrsTime)

    def addMinutes(self):
        self._minutes.pack(expand=True, fill="both", side=self.orient)
        self.spinlblGroup.add(self._minutes)

    def addPeriod(self):
        self._period.pack(expand=True, fill="both", side=self.orient)

    def addAll(self, hours, separator: bool = True):

        self.hour_type = hours

        if hours == constants.HOURS12:
            self.addHours12()

        elif hours == constants.HOURS24:
            self.addHours24()

        else:
            raise ValueError(f"Unknown type '{hours}'. Use either 0/1")

        if separator:
            self._separator.pack(expand=True, fill='both', side=self.orient)

        self.addMinutes()

        if hours == constants.HOURS12:
            self.addPeriod()

        self.spinlblGroup.defaultItem(self._12HrsTime if hours == constants.HOURS12 else self._24HrsTime)

    def set12Hrs(self, val: int):
        """ returns hours in 12 hours clock """
        self._12HrsTime.setValue(val)

    def set24Hrs(self, val: int):
        """ returns hours in 24 hours clock """
        self._24HrsTime.setValue(val)

    def setMins(self, val: int):
        """ sets minutes value """
        self._minutes.setValue(val)

    def configure_12HrsTime(self, **kwargs):
        super(SpinTimePickerModern, self).configure_12HrsTime(**kwargs)
        self.spinlblGroup.defaultItem(self._12HrsTime)

    def configure_24HrsTime(self, **kwargs):
        super(SpinTimePickerModern, self).configure_24HrsTime(**kwargs)
        self.spinlblGroup.defaultItem(self._24HrsTime)

    def hours(self):
        """ returns hours in 12 hours clock if set to 12 hours else hours in 24 hour clock will be returned """

        if self.hour_type == constants.HOURS12:
            return self.hours12()

        else:
            return self.hours24()

    def hours12(self) -> int:
        return int(self._12HrsTime.value())

    def hours24(self) -> int:
        """ returns hours in 24 hours clock """
        return int(self._24HrsTime.value())

    def minutes(self) -> int:
        """ returns minutes """
        return int(self._minutes.value())

    def period(self) -> str:
        """ returns period AM/PM"""
        return self._period.period()

    def time(self) -> Tuple[int, int, str]:
        """ returns hours, minutes and period"""
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

        self.time_picker.configSeparator(font=("Times", 18, "bold"), width=1)

    def setDracula(self):
        self.time_picker.configAnalog(headcolor="#863434", handcolor="#863434", bg="#363636",
                                      clickedcolor="#ffffff", textcolor="#ffffff", canvas_bg="#404040",
                                      alttextwidth=2, bdwidth=0)

        self.time_picker.configSpin(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",
                                    hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")

        self.time_picker.configSeparator(font=("Times", 18, "bold"), width=1)

    def setPurple(self):
        self.time_picker.configAnalog(headcolor="#ee333d", handcolor="#ee333d", bg="#71135c",
                                      clickedcolor="#ffffff", textcolor="#ffffff", canvas_bg="#4e0d3a",
                                      alttextwidth=2, bdwidth=0)

        self.time_picker.configSpin(bg="#71135c", height=2, fg="#ffffff", font=("Times", 16), hoverbg="#3d0430",
                                    hovercolor="#ffffff", clickedbg="#ad118c", clickedcolor="#ffffff")
        self.time_picker.configSeparator(font=("Times", 18, "bold"), width=1)
