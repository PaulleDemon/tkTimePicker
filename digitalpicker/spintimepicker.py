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
        self._seperator = tkinter.Label(self, text=":")
        self._minutes: Union[tkinter.Spinbox, SpinLabel]
        self._period: ttk.Combobox

    def configure_12HrsTime(self, **kwargs):
        self._12HrsTime.configure(**kwargs)

    def configure_24HrsTime(self, **kwargs):
        self._24HrsTime.configure(**kwargs)

    def configure_minute(self, **kwargs):
        self._minutes.configure(**kwargs)

    def configure_period(self, **kwargs):
        self._period.configure(**kwargs)

    def configure_seprator(self, **kwargs):
        self._seperator.configure(**kwargs)


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


class SpinLabel(tkinter.Label):

    def __init__(self, min=None, max=None, number_lst: list = None, start_val: int = None, *args, **kwargs):
        super(SpinLabel, self).__init__(*args, **kwargs)

        self._option = {
            "hovercolor": "#000000",
            "hoverbg": "#ffffff",
            "clickedcolor": "#000000",
            "clickedbg": "#ffffff"
        }

        self.default_fg = self.cget("fg")
        self.default_bg = self.cget("bg")

        if min is not None and max is not None:
            self.number_lst = range(min, max + 1)

        else:
            self.number_lst = number_lst

        if start_val is not None and start_val in self.number_lst:
            self.current_val = start_val

        else:
            self.current_val = self.number_lst[-1]

        self.updateLabel()

        self.previous_key = [self.current_val]

        self._clicked = False

        self.bind("<MouseWheel>", self.wheelEvent)
        self.bind("<Enter>", self.enter)
        self.bind("<KeyRelease>", self.keyPress)

        self.bind("<Leave>", self.leave)
        # self.bind("<FocusOut>", self.resetColor)

    def enter(self, event):
        if not self._clicked:
            self.default_fg = self.cget("fg")
            self.default_bg = self.cget("bg")

            self["fg"] = self._option["hovercolor"]
            self["bg"] = self._option["hoverbg"]

    def leave(self, event):
        if not self._clicked:
            self.resetColor()

    def clicked(self, event=None):
        self._clicked = True
        self["fg"] = self._option["clickedcolor"]
        self["bg"] = self._option["clickedbg"]

    def resetColor(self, event=None):
        self._clicked = False
        self["fg"] = self.default_fg
        self["bg"] = self.default_bg

    def configure(self, cnf=None, **kw):
        remove_lst = list()
        for key, value in kw.copy().items():
            if key in self._option.keys():
                self._option[key] = value
                remove_lst.append(key)

        for x in remove_lst:
            kw.pop(x)

        super(SpinLabel, self).configure(cnf, **kw)

    def setValue(self, val):
        val = int(val)
        if val in self.number_lst:
            self.current_val = val
            self.updateLabel()

    def updateLabel(self):
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


class SpinLblGroup:

    def __init__(self):
        self.group = set()
        self.current = None

    def add(self, item: SpinLabel):
        item.bind("<Button-1>", self.setCurrent, add="+")
        self.group.add(item)

    def defaultItem(self, item: SpinLabel):
        item.event_generate("<Button-1>")

    def remove(self, item: SpinLabel):
        self.group.remove(item)

    def setCurrent(self, event):
        if self.current:
            self.current.resetColor()

        self.current = event.widget
        self.current.clicked()


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

        # self._period = ttk.Combobox(self, values=["a.m", "p.m"], textvariable=self.period_var)
        # self._period.bind("<<ComboboxSelected>>", lambda a: self._minutes.event_generate("<<ChangedPeriod>>"))

        self.spinlblGroup = SpinLblGroup()

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

    # def config



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
