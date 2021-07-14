import tkinter

import constants
from .baseclock import BaseClock


class HoursClock(BaseClock):

    def __init__(self, canvas: tkinter.Canvas, type: int = constants.HOURS12):
        super(HoursClock, self).__init__(canvas)

        if type == constants.HOURS12:
            self.hours12()

        elif type == constants.HOURS24:
            self.hours24()

        else:
            raise TypeError(f"Unknown type {type}, available types 0, 1")

        self.bind("<<Changed>>", self.changed)

    def hours12(self):
        self.hours = 12
        self.setNumberList(min=1, max=12, start=-2)
        self.initClockText()
        self.configure(defaultPointer=12)

    def hours24(self):
        self.hours = 0
        self.setNumberList(min=1, max=24, start=-5)
        self.initClockText()
        self.configure(defaultPointer=1)

    def changed(self, event):
        self.hours = self.current()
        self._canvas.event_generate("<<HoursChanged>>")

    def getHours(self):
        return self.hours


class MinutesClock(BaseClock):

    def __init__(self, canvas: tkinter.Canvas):
        super(MinutesClock, self).__init__(canvas)
        self.initMinutes()
        self.minutes = 0
        self.bind("<<Changed>>", self.changed)

    def initMinutes(self):
        self.setNumberList(min=0, max=59, start=-15, step=5, replace_step=True)
        self.initClockText()
        self.configure(alttextwidth=3)

    def changed(self, event):
        self.minutes = self.current()
        self._canvas.event_generate("<<MinChanged>>")

    def getMinutes(self):
        return self.minutes

