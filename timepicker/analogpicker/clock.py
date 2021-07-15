import tkinter

from .. import constants
from .baseclock import BaseClock


class HoursClock(BaseClock):

    def __init__(self, canvas: tkinter.Canvas, type: int = constants.HOURS12, *args, **kwargs):
        super(HoursClock, self).__init__(canvas, *args, **kwargs)

        if type == constants.HOURS12:
            self._packHours12()

        elif type == constants.HOURS24:
            self._packHours24()

        else:
            raise TypeError(f"Unknown type {type}, available types 0, 1")

        self.bind("<<Changed>>", self.changed)

    def _packHours12(self):
        self.hours = 12
        self.setNumberList(min=1, max=12, start=-2)
        self.drawClockText()
        self.configure(defaultPointer=12)

    def _packHours24(self):
        self.hours = 0
        self.setNumberList(min=1, max=24, start=-5)
        self.drawClockText()
        self.configure(defaultPointer=1)

    def changed(self, event):
        self.hours = self.current()
        self._canvas.event_generate("<<HoursChanged>>")

    def getHours(self):
        return self.hours


class MinutesClock(BaseClock):

    def __init__(self, canvas: tkinter.Canvas, *args, **kwargs):
        super(MinutesClock, self).__init__(canvas, *args, **kwargs)
        self.initMinutes()
        self.minutes = 0
        self.bind("<<Changed>>", self.changed)

    def initMinutes(self):
        self.setNumberList(min=0, max=59, start=-15, step=5, replace_step=True)
        self.drawClockText()
        self.configure(alttextwidth=3)

    def changed(self, event):
        self.minutes = self.current()
        self._canvas.event_generate("<<MinChanged>>")

    def getMinutes(self):
        return self.minutes

