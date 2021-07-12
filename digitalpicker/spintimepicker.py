import re
import tkinter
from tkinter import ttk

HOURS12 = 0
HOURS24 = 1


class SpinTimePickerOld(tkinter.Frame):

    def __init__(self, parent):
        super(SpinTimePickerOld, self).__init__(parent)

        reg12hrs = self.register(self.validate12hrs)
        reg24hrs = self.register(self.validate24hrs)
        regMin = self.register(self.validateMinutes)
        regPeriod = self.register(self.validatePeriod)

        self.period_var = tkinter.StringVar(self, value="a.m")
        self.period_var.trace("w", self.validatePeriod)

        self._12HrsTime = tkinter.Spinbox(self, increment=1, from_=1, to=12,
                                          validate="all", validatecommand=(reg12hrs, "%P"))
        self._24HrsTime = tkinter.Spinbox(self, increment=1, from_=0, to=24,
                                          validate="all", validatecommand=(reg24hrs, "%P"))
        self._minutes = tkinter.Spinbox(self, increment=1, from_=0, to=59,
                                        validate="all", validatecommand=(regMin, "%P"))

        self._period = ttk.Combobox(self, values=["a.m", "p.m"], textvariable=self.period_var)


    def hours12(self):
        self._12HrsTime.pack(expand=True, fill='both')

    def hours24(self):
        self._24HrsTime.pack(expand=True, fill='both')

    def minutes(self):
        self._minutes.pack(expand=True, fill='both')

    def period(self):
        self._period.pack(expand=True, fill='both')

    def validate12hrs(self, value):
        return value.isdigit() and (0 <= int(value) <= 12) or value == ""

    def validate24hrs(self, value):
        return value.isdigit() and (0 <= int(value) <= 24) or value == ""

    def validateMinutes(self, value):
        return value.isdigit() and (0 <= int(value) <= 59) or value == ""

    def validatePeriod(self, *value):
        print("yes", value)

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

        # print(repr(value), bool(re.match("am\s", value)))
        # return bool(re.match("^$|^[AaPp]{0,1}[.]{0,1}[Mm]{0,1}$", value))


if __name__ == "__main__":
    root = tkinter.Tk()

    time_picker = SpinTimePickerOld(root)
    time_picker.hours12()
    time_picker.minutes()
    time_picker.period()
    time_picker.pack()
    root.mainloop()
