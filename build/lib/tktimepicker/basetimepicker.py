import tkinter
import math

from tktimepicker import constants
from typing import Union
from tktimepicker.spinlabel import SpinLabel, PeriodLabel


class BaseClock:
    # This is the base class for hours class and Minutes class.
    # This will drawn the text and the hand of the clock

    def __init__(self, canvas: tkinter.Canvas, min: int = None, max: int = None, numberlst: list = None,
                      start: int = None, step=None, replace_step: bool = None, **kwargs):

        self._options = {
            "min_size": 200,
            "max_size": 1080,
            "bg": "#ffffff",
            "bdColor": "#000000",
            "bdwidth": 1,
            "textoffset": 20,
            "textfont": ("Times", 14, "normal"),
            "textcolor": "#878787",
            "alttextwidth": 10,
            "defaultPointer": 0,  # which number should it be pointing to in the beginning
            "handthickness": 3,
            "handcolor": "#000000",
            "capstyle": "round",
            "headsize": 10,
            "headcolor": "#000000",
            "headbdwidth": 0,
            "headbdcolor": "#000000",
            "clickedcolor": "#c4c4c4",
            "halo": 5
        }

        if set(kwargs) - set(self._options):
            raise TypeError(f"Got unexpected arguments '{', '.join(set(kwargs) - set(self._options))}'")

        self._options.update(kwargs)

        self._canvas = canvas
        self.clock = self._canvas.create_oval(0, 0, 0, 0, fill=self._options["bg"],
                                              outline=self._options["bdColor"],
                                              width=self._options["bdwidth"])

        self.hand_line = self._canvas.create_line(0, 0, 0, 0,
                                                  fill=self._options["handcolor"],
                                                  width=self._options["handthickness"],
                                                  capstyle=self._options["capstyle"], tag="tkclockhand")

        self.hand_end = self._canvas.create_oval(0, 0, 0, 0, fill=self._options["headcolor"],
                                                 width=self._options["headbdwidth"],
                                                 outline=self._options["headbdcolor"],
                                                 tag="tkclockhand")

        self.start = 0
        self.step = 1
        self.replaceStep: bool = True
        self._current_id = ""

        if any([min, max, numberlst]):
            self.setNumberList(min, max, numberlst, start, step, replace_step)
            self.drawClockText()

        self._canvas.bind("<B1-Motion>", self.movehand)
        self._canvas.bind("<Button-1>", self.movehand)
        self._canvas.bind("<Configure>", self.updateClockRect)

    def drawClockText(self):  # adds texts to the timepickerbase

        self._canvas.delete("tkclocktext")

        for index, char in enumerate(self.numberlst, start=self.start):
            if index % self.step != 0 and self.replaceStep:
                obj = self._canvas.create_oval(0, 0, 5, 5, width=0, tags="tkclocktext", fill=self._options["textcolor"])

            else:
                obj = self._canvas.create_text(0, 0, text=f"{char}", tags="tkclocktext",
                                               font=self._options["textfont"], fill=self._options["textcolor"])

            if self.current_index == char:
                self._current_id = obj
                self._canvas.itemconfig(self._current_id, fill=self._options["clickedcolor"])

    def setPointerIndex(self, index):

        self.current_index = index

        self._canvas.itemconfig("tkclocktext", fill=self._options["textcolor"])

        for char, obj in zip(self.numberlst, self._canvas.find_withtag("tkclocktext")):
            
            if self.current_index == char:
                self._current_id = obj
                self._canvas.itemconfig(self._current_id, fill=self._options["clickedcolor"])
                break

        self.updateHand()

    def setNumberList(self, min: int = None, max: int = None, numberlst: list = None,
                      start: int = None, step=None, replace_step: bool = None):
        """ sets number list, the list using which the numbers will be drawn """
        if step is not None:
            self.step = step if step > 0 else 1

        if replace_step is not None:
            self.replaceStep = replace_step

        if start is not None:
            self.start = start

        if min is not None and max is not None:
            if self.step and not self.replaceStep:
                self.numberlst = range(min, max + 1, step)

            else:
                self.numberlst = range(min, max + 1)

        elif numberlst:
            self.numberlst = numberlst
            if not self.replaceStep:
                for x in range(0, len(self.numberlst), step):
                    self.numberlst.pop(x)

        else:
            raise ValueError("Enter either min, max or provide a list")

        if self._options["defaultPointer"] in self.numberlst:
            self.current_index = self._options["defaultPointer"]

        else:
            self.current_index = self.numberlst[0]

    def updateClockRect(self, event): 
        # helper method to pass event.width and event.height to updateClock to  
        self.updateClock(event.width, event.height)

    def updateClock(self, width=None, height=None):  # updates the size of the circle and moves it to center
        
        if not width:
            width = self._canvas.winfo_width()

        if not height:
            height = self._canvas.winfo_height()

        try:
            # width, height = event.width, event.height
            size = width if width < height else height

            if self._options["min_size"] < size < self._options["max_size"]:
                # doesn't shrink or expand is the size is not b/w min and max size
                centerX, centerY = width / 2, height / 2
                size -= float(self._canvas.itemcget(self.clock, "width")) + 10

                # Since some versions of tkinter doesn't contain `moveto` method we need to do
                # some math to center the timepickerbase or tk.call('moveto')
                clock_coords = self._canvas.coords(self.clock)

                x = clock_coords[0] + (centerX - size/2 - clock_coords[0])
                y = clock_coords[1] + (centerY - size/2 - clock_coords[1])

                self._canvas.coords(self.clock, x, y, size+x, size+y)
                # self._canvas.moveto(self.timepickerbase, centerX - size / 2, centerY - size / 2)

                angle = math.pi * 2 / len(self.numberlst)
                radius = size / 2 - self._options["textoffset"]

                for index, obj in enumerate(self._canvas.find_withtag("tkclocktext"), start=self.start):

                    _angle = angle * index

                    y = centerY + radius * math.sin(_angle)
                    x = centerX + radius * math.cos(_angle)

                    if index % self.step != 0 and self.replaceStep:
                        self._canvas.coords(obj, x - self._options["alttextwidth"],
                                            y - self._options["alttextwidth"],
                                            x + self._options["alttextwidth"],
                                            y + self._options["alttextwidth"])
                        continue

                    self._canvas.coords(obj, x, y)

                self.updateHand()

        except AttributeError:
            raise NameError("`setNumberList` method must be called to initialize the list")

        except TypeError:
            raise NameError("Need to call `drawClockText` method")

    def configure(self, **kwargs):  # background, border-color, border-width

        if set(kwargs) - set(self._options):
            raise TypeError(f"Got unexpected arguments '{', '.join(set(kwargs) - set(self._options))}'")

        self._options.update(kwargs)

        self._canvas.itemconfig(self.clock,
                                fill=self._options["bg"],
                                outline=self._options["bdColor"],
                                width=self._options["bdwidth"])

        for obj in self._canvas.find_withtag("tkclocktext"):
            try:
                self._canvas.itemconfig(obj, font=self._options["textfont"], fill=self._options["textcolor"])

            except tkinter.TclError:
                self._canvas.itemconfig(obj, fill=self._options["textcolor"])

        self._canvas.itemconfig(self.hand_line, fill=self._options["handcolor"],
                                width=self._options["handthickness"],
                                capstyle=self._options["capstyle"])

        self._canvas.itemconfig(self.hand_end, fill=self._options["headcolor"],
                                width=self._options["headbdwidth"],
                                outline=self._options["headbdcolor"],
                                tag="tkclockhand")

        self._canvas.itemconfig(self._current_id, fill=self._options["clickedcolor"])

    def current(self):
        """ returns current value of where its pointing towards"""
        return self.current_index

    def movehand(self, event: tkinter.Event):
        """ moves the hand to closest position of the mouse click """
        _current_id = self._canvas.find_closest(event.x, event.y, halo=self._options["halo"])[0]

        if _current_id in self._canvas.find_withtag("tkclocktext"):
            self._canvas.itemconfig(self._current_id, fill=self._options["textcolor"])
            self._current_id = _current_id
            self._canvas.itemconfig(self._current_id, fill=self._options["clickedcolor"])
            self.updateHand()
            self._canvas.event_generate("<<HandMoved>>")

    def updateHand(self):
        """ updates the hand to closest mouse position """
        item_bbox = self._canvas.bbox(self._current_id)

        clock_coords = self._canvas.coords(self.clock)
        centerX, centerY = (clock_coords[0] + clock_coords[2]) / 2, (clock_coords[1] + clock_coords[3]) / 2

        itemCX, itemCY = (item_bbox[2] + item_bbox[0]) / 2, (item_bbox[3] + item_bbox[1]) / 2

        self._canvas.coords(self.hand_line, centerX, centerY, itemCX, itemCY)

        self._canvas.coords(self.hand_end, itemCX - self._options["headsize"],
                            itemCY - self._options["headsize"],
                            itemCX + self._options["headsize"],
                            itemCY + self._options["headsize"])

        try:
            self.current_index = self._canvas.itemcget(self._current_id, "tkclocktext")

        except tkinter.TclError:
            for obj, number in zip(self._canvas.find_withtag("tkclocktext"), self.numberlst):

                if self._current_id == obj:
                    self.current_index = str(number)

    def bind(self, seq, callback, add=None):
        self._canvas.bind(seq, callback, add)


class SpinBaseClass(tkinter.Frame):  # Base class for SpinTimePickerOld, SpinTimePickerModern

    def __init__(self, parent):
        super(SpinBaseClass, self).__init__(parent)

        self._12HrsTime: Union[tkinter.Spinbox, SpinLabel]
        self._24HrsTime: Union[tkinter.Spinbox, SpinLabel]
        self._separator = tkinter.Label(self, text=":")
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

    def configure_separator(self, **kwargs):
        self._separator.configure(**kwargs)

    def configureAll(self, **kw):
        """ passes the configs to 12 hrs, 24 hrs, minutes and period """
        self.configure_12HrsTime(**kw)
        self.configure_24HrsTime(**kw)
        self.configure_minute(**kw)
        self.configure_period(**kw)


class HoursClock(BaseClock): # A quick class to create a Hours clock

    def __init__(self, canvas: tkinter.Canvas, type: int = constants.HOURS12, *args, **kwargs):
        super(HoursClock, self).__init__(canvas, *args, **kwargs)

        if type == constants.HOURS12:
            self._packHours12()

        elif type == constants.HOURS24:
            self._packHours24()

        else:
            raise TypeError(f"Unknown type {type}, available types 0, 1")

        self.bind("<<HandMoved>>", self.changed)

    def _packHours12(self):
        self.hours = 12
        self.configure(defaultPointer=12)
        self.setNumberList(min=1, max=12, start=-2)
        self.drawClockText()

    def _packHours24(self):
        self.hours = 0
        self.configure(defaultPointer=1)
        self.setNumberList(min=0, max=23, start=-6)
        self.drawClockText()

    def changed(self, event):
        self.hours = self.current()
        self._canvas.event_generate("<<HoursChanged>>")

    def setHours(self, hrs: int):
        
        self.setPointerIndex(hrs)
        # self.current_index = hrs
        # self.drawClockText()
        # self.updateClock()

    def getHours(self):
        return self.hours


class MinutesClock(BaseClock):  # A class to create minutes clock

    def __init__(self, canvas: tkinter.Canvas, step=5, replace_step=True, *args, **kwargs):
        super(MinutesClock, self).__init__(canvas, *args, **kwargs)
        self.initMinutes(step=step, replace_step=replace_step)
        self.minutes = 0
        self.bind("<<HandMoved>>", self.changed)

    def initMinutes(self, step=5, replace_step=True):
        """ initializes minutes """
        self.setNumberList(min=0, max=59, start=-15, step=step, replace_step=replace_step)
        self.drawClockText()
        self.configure(alttextwidth=3)

    def changed(self, event):
        """ generates MinChanged when HandMoved"""
        self.minutes = self.current()
        self._canvas.event_generate("<<MinChanged>>")

    def getMinutes(self):
        return self.minutes

    def setMinutes(self, mins: int):

        self.setPointerIndex(mins)


