import tkinter
from .spinlabel import SpinLabel, LabelGroup, PeriodLabel
from typing import Union


HOURS12 = 0
HOURS24 = 1

VERTICAL = 0
HORIZONTAL = 1


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
        self._period.configPeriod(**kwargs)

    def configure_seprator(self, **kwargs):
        self._seperator.configure(**kwargs)


class SpinTimePickerOld(_SpinBaseClass):

    def __init__(self, parent, orient=HORIZONTAL, period_orient=VERTICAL):
        super(SpinTimePickerOld, self).__init__(parent)

        self.orient = "top" if orient == VERTICAL else "left"

        reg12hrs = self.register(self.validate12hrs)
        reg24hrs = self.register(self.validate24hrs)
        regMin = self.register(self.validateMinutes)

        self.period_var = tkinter.StringVar(self, value="a.m")
        self.period_var.trace("w", self.validatePeriod)

        self._12HrsTime = tkinter.Spinbox(self, increment=1, from_=1, to=12,
                                          validate="all", validatecommand=(reg12hrs, "%P"),
                                          command=lambda a: self._12HrsTime.event_generate("<<Changed12Hrs>>"))

        self._24HrsTime = tkinter.Spinbox(self, increment=1, from_=0, to=24,
                                          validate="all", validatecommand=(reg24hrs, "%P"),
                                          command=lambda a: self._24HrsTime.event_generate("<<Changed24Hrs>>"))

        self._minutes = tkinter.Spinbox(self, increment=1, from_=0, to=59,
                                        validate="all", validatecommand=(regMin, "%P"),
                                        command=lambda a: self._minutes.event_generate("<<ChangedMins>>"))

        self._period = PeriodLabel(self, period_orient)

    def hours12(self):
        self._12HrsTime.pack(expand=True, fill='both', side=self.orient)

    def hours24(self):
        self._24HrsTime.pack(expand=True, fill='both', side=self.orient)

    def minutes(self):
        self._minutes.pack(expand=True, fill='both', side=self.orient)

    def period(self):
        self._period.pack(expand=True, fill='both', side='left')

    def validate12hrs(self, value):
        return value.isdigit() and (0 <= int(value) <= 12) or value == ""

    def validate24hrs(self, value):
        return value.isdigit() and (0 <= int(value) <= 24) or value == ""

    def validateMinutes(self, value):
        return value.isdigit() and (0 <= int(value) <= 59) or value == ""

    def pack_all(self, hours: int, seperator: bool = True):

        if hours == HOURS12:
            self.hours12()

        elif hours == HOURS24:
            self.hours24()

        else:
            raise ValueError(f"Unknown type '{hours}'. Use either 0/1")

        if seperator:
            self._seperator.pack(expand=True, fill='both', side=self.orient)

        self.minutes()
        self.period()


class SpinTimePickerModern(_SpinBaseClass):

    def __init__(self, parent, orient=HORIZONTAL):
        super(SpinTimePickerModern, self).__init__(parent)

        self.hour_type = HOURS12
        self.orient = "top" if orient == VERTICAL else "left"

        self._12HrsTime = SpinLabel(master=self, min=1, max=12)
        self._12HrsTime.bind("<<valueChanged>>", lambda a: self._12HrsTime.event_generate("<<Changed12Hrs>>"))
        self._12HrsTime.bind("<Button-1>", lambda a: self.event_generate("<<Hrs12Clicked>>"))

        self._24HrsTime = SpinLabel(master=self, min=0, max=24)
        self._24HrsTime.bind("<<valueChanged>>", lambda a: self._12HrsTime.event_generate("<<Changed24Hrs>>"))
        self._24HrsTime.bind("<Button-1>", lambda a: self.event_generate("<<Hrs24Clicked>>"))

        self._minutes = SpinLabel(master=self, min=0, max=59)
        self._minutes.bind("<<valueChanged>>", lambda a: self._minutes.event_generate("<<ChangedMins>>"))
        self._minutes.bind("<Button-1>", lambda a: self.event_generate("<<MinClicked>>"))

        self._period = PeriodLabel(master=self)

        self.spinlblGroup = LabelGroup()

    def addHours12(self):
        self._12HrsTime.pack(expand=True, fill='both', side=self.orient)
        self.spinlblGroup.add(self._12HrsTime)

    def addHours24(self):
        self._24HrsTime.pack(expand=True, fill='both', side=self.orient)
        self.spinlblGroup.add(self._24HrsTime)

    def addMinutes(self):
        self._minutes.pack(expand=True, fill='both', side=self.orient)
        self.spinlblGroup.add(self._minutes)

    def addPeriod(self):
        self._period.pack(expand=True, fill='both', side='left')

    def pack_all(self, hours, seperator: bool = True):

        self.hour_type = hours

        if hours == HOURS12:
            self.addHours12()

        elif hours == HOURS24:
            self.addHours24()

        else:
            raise ValueError(f"Unknown type '{hours}'. Use either 0/1")

        if seperator:
            self._seperator.pack(expand=True, fill='both', side=self.orient)

        self.addMinutes()
        self.addPeriod()

        self.spinlblGroup.defaultItem(self._12HrsTime if hours == HOURS12 else self._24HrsTime)

    def set12Hrs(self, val: int):
        self._12HrsTime.setValue(val)

    def set24Hrs(self, val: int):
        self._24HrsTime.setValue(val)

    def setMins(self, val: int):
        self._minutes.setValue(val)

    def configure_12HrsTime(self, **kwargs):
        super(SpinTimePickerModern, self).configure_12HrsTime(**kwargs)
        self.spinlblGroup.defaultItem(self._12HrsTime if self.hour_type == HOURS12 else self._24HrsTime)


if __name__ == "__main__":
    root = tkinter.Tk()

    # time_picker = SpinTimePickerOld(root, orient=VERTICAL)
    # time_picker.hours12()
    # time_picker.configure_12HrsTime(bg='blue')
    # time_picker.minutes()
    # time_picker.period()
    # time_picker.pack()
    # lbl = SpinTimePickerModern(root)
    # lbl.hours12()
    # lbl.minutes()
    # lbl.period()
    # lbl.configure_12HrsTime(bg='red')
    # lbl.pack()

    root.mainloop()
