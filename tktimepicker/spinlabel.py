import tkinter
from typing import Union
from tktimepicker import constants


class HoverClickLabel(tkinter.Label):

    def __init__(self, *args, **kwargs):
        super(HoverClickLabel, self).__init__(*args, **kwargs)

        self._option = {
            "hovercolor": "#000000",
            "hoverbg": "#ffffff",
            "clickedcolor": "#000000",
            "clickedbg": "#ffffff",
        }

        self.setDefault()

        self._clicked = False

        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)

    def setDefault(self):
        """ sets default background and foreground color """
        self.default_fg = self.cget("fg")
        self.default_bg = self.cget("bg")

    def enter(self, event):
        self.focus_set()
        if not self._clicked:
            self.setDefault()
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

        super(HoverClickLabel, self).configure(cnf, **kw)


class PeriodLabel(tkinter.Frame):

    def __init__(self, master=None, defaultperiod="AM", orient=constants.VERTICAL):
        super(PeriodLabel, self).__init__(master)

        if defaultperiod in [constants.AM, constants.PM]:
            self._current_period = defaultperiod

        else:
            raise ValueError(f"Unknown value {defaultperiod} Use AM/PM")

        self._am = HoverClickLabel(self, text="AM")
        self._pm = HoverClickLabel(self, text="PM")

        self._am.bind("<Button-1>", self.changePeriod)
        self._pm.bind("<Button-1>", self.changePeriod)

        orient = "top" if orient == constants.VERTICAL else "left"

        self._am.pack(expand=True, fill='both', side=orient)
        self._pm.pack(expand=True, fill='both', side=orient)

        self.group = LabelGroup()
        self.group.add(self._am)
        self.group.add(self._pm)
        self.group.defaultItem(self._am if defaultperiod == constants.AM else self._pm)

    def configPeriod(self, **kw):
        self._am.configure(**kw)
        self._pm.configure(**kw)
        self.group.defaultItem(self._am if self._current_period == constants.AM else self._pm)

    def changePeriod(self, event):
        self._current_period = event.widget.cget("text")

    def period(self):
        """ returns period """
        return self._current_period


class SpinLabel(HoverClickLabel):

    def __init__(self, min=None, max=None, number_lst: list = None, start_val: int = None, *args, **kwargs):
        super(SpinLabel, self).__init__(*args, **kwargs)

        if min is not None and max is not None:
            self.number_lst = range(min, max + 1)

        else:
            self.number_lst = number_lst

        if start_val is not None and start_val in self.number_lst:
            self.current_val = start_val

        else:
            self.current_val = self.number_lst[-1]

        self._current_index = self.number_lst.index(self.current_val)
        self.updateLabel()

        self.previous_key = [self.current_val]

        self._clicked = False

        self.bind("<MouseWheel>", self.wheelEvent)
        self.bind("<KeyRelease>", self.keyPress)

    def setValue(self, val):
        val = int(val)
        if val in self.number_lst:
            self.current_val = val
            self._current_index = self.number_lst.index(val)
            self.updateLabel()

    def updateLabel(self):
        self["text"] = f"{self.current_val}"
        self.event_generate("<<valueChanged>>")

    def value(self) -> str:
        return self.current_val

    def emptyPreviousKey(self):
        self.previous_key = []

    def delayedKey(self, key):
        if len(self.previous_key) >= len(str(self.number_lst[-1])):
            self.previous_key.pop(0)

        self.previous_key.append(key)

        number = int(''.join(map(str, self.previous_key)))

        if number in self.number_lst:
            self.current_val = number
            self._current_index = self.number_lst.index(number)

        self.updateLabel()
        self.after(1000, self.emptyPreviousKey)

    def wheelEvent(self, event: tkinter.Event):

        if event.delta > 0:

            if self._current_index < len(self.number_lst)-1:
                self._current_index += 1

            else:
                self._current_index = 0

        else:
            if self._current_index > 0:
                self._current_index -= 1

            else:
                self._current_index = len(self.number_lst)-1

        self.current_val = self.number_lst[self._current_index]
        self.updateLabel()

    def keyPress(self, event):
        """ handles key press for """
        try:
            number = int(event.char)
            self.delayedKey(number)

        except ValueError:
            pass


class LabelGroup:

    def __init__(self):
        self.group = set()
        self.current = None

    def add(self, item: Union[SpinLabel, HoverClickLabel]):
        """ adds the label to the group """
        item.bind("<Button-1>", self.setCurrent, add="+")
        self.group.add(item)

    def defaultItem(self, item: Union[SpinLabel, HoverClickLabel]):
        """ sets default widget """
        item.setDefault()
        self.setCurrent(widget=item)

    def remove(self, item: Union[SpinLabel, HoverClickLabel]):
        """ removes from the group """
        self.group.remove(item)

    def setCurrent(self, event=None, widget=None):
        """ marks clicked label in the group """

        if self.current:
            self.current.resetColor()

        self.current = event.widget if event else widget
        self.current.clicked()
