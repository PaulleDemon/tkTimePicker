import tkinter
import math


class BaseClock:

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

    def drawClockText(self):  # adds texts to the analogpicker

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

    def setNumberList(self, min: int = None, max: int = None, numberlst: list = None,
                      start: int = None, step=None, replace_step: bool = None):

        if step is not None:
            self.step = step if step > 0 else 1

        if replace_step is not  None:
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

    def updateClockRect(self, event):  # updates the size of the circle and moves it to center

        try:
            width, height = event.width, event.height
            size = width if width < height else height

            if self._options["min_size"] < size < self._options["max_size"]:
                # doesn't shrink or expand is the size is not b/w min and max size
                centerX, centerY = width / 2, height / 2
                size -= float(self._canvas.itemcget(self.clock, "width")) + 10

                # Since some versions of tkinter doesn't contain `moveto` method we need to do
                # some math to center the analogpicker or tk.call('moveto')
                clock_coords = self._canvas.coords(self.clock)

                x = clock_coords[0] + (centerX - size/2 - clock_coords[0])
                y = clock_coords[1] + (centerY - size/2 - clock_coords[1])

                self._canvas.coords(self.clock, x, y, size+x, size+y)
                # self._canvas.moveto(self.analogpicker, centerX - size / 2, centerY - size / 2)

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
        return self.current_index

    def movehand(self, event: tkinter.Event):

        _current_id = self._canvas.find_closest(event.x, event.y, halo=self._options["halo"])[0]

        if _current_id in self._canvas.find_withtag("tkclocktext"):
            self._canvas.itemconfig(self._current_id, fill=self._options["textcolor"])
            self._current_id = _current_id
            self._canvas.itemconfig(self._current_id, fill=self._options["clickedcolor"])
            self.updateHand()
            self._canvas.event_generate("<<Changed>>")

    def updateHand(self):

        item_bbox = self._canvas.bbox(self._current_id)

        # centerX, centerY = self._canvas.winfo_width() / 2 - 2, self._canvas.winfo_height() / 2 - 5
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

    def bind(self, seq, callback):
        self._canvas.bind(seq, callback)
