import re
import tkinter
from tkinter import ttk
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
        self._minutes: Union[tkinter.Spinbox, SpinLabel]
        self._period: ttk.Combobox

    def configure_12HrsTime(self, **kwargs):
        self._12HrsTime.configure(**kwargs)

    def configure_24HrsTime(self, **kwargs):
        self._24HrsTime.configure(**kwargs)

    def configure_minute(self, **kwargs):
        self.minutes.configure(**kwargs)

    def configure_period(self, **kwargs):
        self._period.configure(**kwargs)


class SpinTimePickerOld(_SpinBaseClass):

    def __init__(self, parent, orient=HORIZONTAL):
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

        self._period = ttk.Combobox(self, values=["a.m", "p.m"], textvariable=self.period_var)
        self._period.bind("<<ComboboxSelected>>", lambda a: self._minutes.event_generate("<<ChangedPeriod>>"))

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

    def pack_all(self, hours: int):

        if hours == HOURS12:
            self.hours12()

        elif hours == HOURS24:
            self.hours24()

        else:
            raise ValueError(f"Unknown type '{hours}'. Use either 0/1")

        self.minutes()
        self.period()

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


class SpinTimePickerModern(_SpinBaseClass):

    def __init__(self, parent, orient=HORIZONTAL):
        super(SpinTimePickerModern, self).__init__(parent)

        self.orient = "top" if orient == VERTICAL else "left"

        self.period_var = tkinter.StringVar(self, value="a.m")
        self.period_var.trace("w", self.validatePeriod)

        self._12HrsTime = SpinLabel(master=self, min=1, max=12)
        self._12HrsTime.bind("<<valueChanged>>", lambda a: self._12HrsTime.event_generate("<<Changed12Hrs>>"))
        self._12HrsTime.bind("<Button-1>", lambda a: self.event_generate("<<Hrs12Clicked>>"))

        self._24HrsTime = SpinLabel(master=self, min=0, max=24)
        self._24HrsTime.bind("<<valueChanged>>", lambda a: self._12HrsTime.event_generate("<<Changed24Hrs>>"))
        self._24HrsTime.bind("<Button-1>", lambda a: self.event_generate("<<Hrs24Clicked>>"))

        self._minutes = SpinLabel(master=self, min=0, max=59)
        self._minutes.bind("<<valueChanged>>", lambda a: self._minutes.event_generate("<<ChangedMins>>"))
        self._minutes.bind("<Button-1>", lambda a: self.event_generate("<<MinClicked>>"))

        self._period = ttk.Combobox(self, values=["a.m", "p.m"], textvariable=self.period_var)
        self._period.bind("<<ComboboxSelected>>", lambda a: self._minutes.event_generate("<<ChangedPeriod>>"))

    def hours12(self):
        self._12HrsTime.pack(expand=True, fill='both', side=self.orient)

    def hours24(self):
        self._24HrsTime.pack(expand=True, fill='both', side=self.orient)

    def minutes(self):
        self._minutes.pack(expand=True, fill='both', side=self.orient)

    def period(self):
        self._period.pack(expand=True, fill='both', side='left')

    def pack_all(self, hours):

        if hours == HOURS12:
            self.hours12()

        elif hours == HOURS24:
            self.hours24()

        else:
            raise ValueError(f"Unknown type '{hours}'. Use either 0/1")

        self.minutes()
        self.period()

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

    def set12Hrs(self, val: int):
        self._12HrsTime.setValue(val)

    def set24Hrs(self, val: int):
        self._24HrsTime.setValue(val)

    def setMins(self, val: int):
        self._minutes.setValue(val)


class SpinLabel(tkinter.Label):

    def __init__(self, min=None, max=None, number_lst: list = None, start_val: int = None, *args, **kwargs):
        super(SpinLabel, self).__init__(*args, **kwargs)

        if min is not None and max is not None:
            self.number_lst = range(min, max + 1)

        else:
            self.number_lst = number_lst
        print(self.number_lst)

        if start_val is not None and start_val in self.number_lst:
            self.current_val = start_val

        else:
            self.current_val = self.number_lst[-1]

        self.updateLabel()

        self.previous_key = [self.current_val]

        self.bind("<MouseWheel>", self.wheelEvent)
        self.bind("<Enter>", lambda event: self.focus_set())
        self.bind("<KeyRelease>", self.keyPress)

    def setValue(self, val):
        val = int(val)
        if val in self.number_lst:
            self.current_val = val
            self.updateLabel()

    def updateLabel(self):
        print("UPDATED: ", self.current_val)
        self["text"] = f"{self.current_val}"
        self.event_generate("<<valueChanged>>")

    def value(self) -> int:
        return int(self.current_val)

    def emptyPreviousKey(self):
        self.previous_key = []

    def delayedKey(self, key):
        if len(self.previous_key) >= len(str(self.number_lst[-1])):
            self.previous_key.pop(0)

        self.previous_key.append(key)

        number = int(''.join(map(str, self.previous_key)))

        if number in self.number_lst:
            self.current_val = number

        self.updateLabel()

        self.after(1000, self.emptyPreviousKey)

    def wheelEvent(self, event: tkinter.Event):

        if event.delta > 0:

            if self.current_val < self.number_lst[-1]:
                self.current_val += 1

        else:
            if self.current_val > self.number_lst[0]:
                self.current_val -= 1

        self.updateLabel()

    def keyPress(self, event):

        try:
            number = int(event.char)
            self.delayedKey(number)

        except ValueError:
            pass


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
