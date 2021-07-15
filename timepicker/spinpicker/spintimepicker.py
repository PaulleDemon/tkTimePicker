import tkinter
from tkinter import ttk

from typing import Union

from timepicker import constants
from timepicker.spinpicker.spinlabel import SpinLabel, LabelGroup, PeriodLabel


class _SpinBaseClass(tkinter.Frame):

    def __init__(self, parent):
        super(_SpinBaseClass, self).__init__(parent)

        self._12HrsTime: Union[tkinter.Spinbox, SpinLabel]
        self._24HrsTime: Union[tkinter.Spinbox, SpinLabel]
        self._seperator = tkinter.Label(self, text=":")
        self._minutes: Union[tkinter.Spinbox, SpinLabel]
        self._period: PeriodLabel

    def configure_12HrsTime(self, **kwargs):
        self._12HrsTime.configure(**kwargs)

    def configure_24HrsTime(self, **kwargs):
        self._24HrsTime.configure(**kwargs)

    def configure_minute(self, **kwargs):
        self._minutes.configure(**kwargs)

    def configure_period(self, **kwargs):
        if isinstance(self._period, PeriodLabel):
            self._period.configPeriod(**kwargs)

    def configure_seprator(self, **kwargs):
        self._seperator.configure(**kwargs)

    def configureAll(self, **kw):
        self.configure_12HrsTime(**kw)
        self.configure_24HrsTime(**kw)
        self.configure_minute(**kw)
        self.configure_period(**kw)


class SpinTimePickerOld(_SpinBaseClass):

    def __init__(self, parent, orient=constants.HORIZONTAL, period_orient=constants.VERTICAL):
        super(SpinTimePickerOld, self).__init__(parent)

        self.orient = "top" if orient == constants.VERTICAL else "left"

        reg12hrs = self.register(self.validate12hrs)
        reg24hrs = self.register(self.validate24hrs)
        regMin = self.register(self.validateMinutes)

        self.period_var = tkinter.StringVar(self, value="a.m")
        self.period_var.trace("w", self.validatePeriod)

        self._12HrsTime = tkinter.Spinbox(self, increment=1, from_=1, to=12,
                                          validate="all", validatecommand=(reg12hrs, "%P"),
                                          command=lambda: self._12HrsTime.event_generate("<<Changed12Hrs>>"))

        self._24HrsTime = tkinter.Spinbox(self, increment=1, from_=0, to=24,
                                          validate="all", validatecommand=(reg24hrs, "%P"),
                                          command=lambda: self._24HrsTime.event_generate("<<Changed24Hrs>>"))

        self._minutes = tkinter.Spinbox(self, increment=1, from_=0, to=59,
                                        validate="all", validatecommand=(regMin, "%P"),
                                        command=lambda: self._minutes.event_generate("<<ChangedMins>>"))

        self._period = ttk.Combobox(self, values=["a.m", "p.m"], textvariable=self.period_var)
        self._period.bind("<<ComboboxSelected>>", lambda a: self._minutes.event_generate("<<ChangedPeriod>>"))

    def hours12(self):
            self._12HrsTime.pack(expand=True, fill="both", side=self.orient)

    def hours24(self):
        self._24HrsTime.pack(expand=True, fill="both", side=self.orient)

    def minutes(self):
        self._minutes.pack(expand=True, fill="both", side=self.orient)

    def period(self):
        self._period.pack(expand=True, fill="both", side=self.orient)

    def validate12hrs(self, value):
        return value.isdigit() and (0 <= int(value) <= 12) or value == ""

    def validate24hrs(self, value):
        return value.isdigit() and (0 <= int(value) <= 24) or value == ""

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

    def addAll(self, hours: int, seperator: bool = True):

        if hours == constants.HOURS12:
            self.hours12()

        elif hours == constants.HOURS24:
            self.hours24()

        else:
            raise ValueError(f"Unknown type '{hours}'. Use either 0/1")

        if seperator:
            self._seperator.pack(expand=True, fill='both', side=self.orient)

        self.minutes()
        self.period()


class SpinTimePickerModern(_SpinBaseClass):

    def __init__(self, parent, orient=constants.HORIZONTAL, per_orient=constants.VERTICAL, period=constants.AM):
        super(SpinTimePickerModern, self).__init__(parent)

        self.hour_type = constants.HOURS12
        self.orient = "top" if orient == constants.VERTICAL else "left"

        self._12HrsTime = SpinLabel(master=self, min=1, max=12)
        self._12HrsTime.bind("<<valueChanged>>", lambda a: self._12HrsTime.event_generate("<<Changed12Hrs>>"))
        self._12HrsTime.bind("<Button-1>", lambda a: self.event_generate("<<Hrs12Clicked>>"))

        self._24HrsTime = SpinLabel(master=self, min=0, max=24)
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

    def addAll(self, hours, seperator: bool = True):

        self.hour_type = hours

        if hours == constants.HOURS12:
            self.addHours12()

        elif hours == constants.HOURS24:
            self.addHours24()

        else:
            raise ValueError(f"Unknown type '{hours}'. Use either 0/1")

        if seperator:
            self._seperator.pack(expand=True, fill='both', side=self.orient)

        self.addMinutes()
        self.addPeriod()

        self.spinlblGroup.defaultItem(self._12HrsTime if hours == constants.HOURS12 else self._24HrsTime)

    def set12Hrs(self, val: int):
        self._12HrsTime.setValue(val)

    def set24Hrs(self, val: int):
        self._24HrsTime.setValue(val)

    def setMins(self, val: int):
        self._minutes.setValue(val)

    def configure_12HrsTime(self, **kwargs):
        super(SpinTimePickerModern, self).configure_12HrsTime(**kwargs)
        self.spinlblGroup.defaultItem(self._12HrsTime if self.hour_type == constants.HOURS12 else self._24HrsTime)

    def hours(self):
        if self.hour_type == constants.HOURS12:
            return self.hours12()

        else:
            return self.hours24()

    def hours12(self) -> int:
        return int(self._12HrsTime.value())

    def hours24(self) -> int:
        return int(self._24HrsTime.value())

    def minutes(self) -> int:
        return int(self._minutes.value())

    def period(self) -> str:
        return self._period.period()

    def time(self) -> tuple[int, int, str]:
        return self.hours(), self.minutes(), self.period()


if __name__ == "__main__":
    root = tkinter.Tk()

    canvas = tkinter.Canvas(root)

    time_picker = SpinTimePickerModern(root)
    time_picker.addAll(constants.HOURS12)

    time_picker.pack(expand=1, fill='both')


    root.mainloop()
