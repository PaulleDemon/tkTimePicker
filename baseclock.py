import tkinter
import math


class BaseClock:

    def __init__(self, canvas: tkinter.Canvas, min: int = None, max: int = None,
                 step=0, replace_step: bool = True, numberlst: list = [], **kwargs):

        self.options = {
            "min-size": 200,
            "max-size": 1080,
            "bg": "#ffffff",
            "bdColor": "#000000",
            "bdwidth": 1,
            "textoffset": 20,
            "textfont": ("Times", 20, "normal"),
            "textcolor": "#878787",
            "alttextwidth": 10,
            "start": 0,
            "defaultPointer": 0,  # which number should it be pointing to in the beginning
            "handthickness": 3,
            "handcolor": "#000000",
            "capstyle": "round",
            "headsize": 20,
            "headcolor": "#000000"
        }

        if set(kwargs)-set(self.options):
            raise TypeError(f"Got unexpected arguments '{', '.join(set(kwargs)-set(self.options))}'")

        self.options.update(kwargs)

        self.canvas = canvas
        self.clock = self.canvas.create_oval(0, 0, 0, 0, fill=self.options["bg"],
                                             outline=self.options["bdColor"],
                                             width=self.options["bdwidth"])

        self.hand_line = self.canvas.create_line(0, 0, 0, 0,
                                                 fill=self.options["handcolor"],
                                                 width=self.options["handthickness"],
                                                 capstyle=self.options["capstyle"])

        self.hand_end = self.canvas.create_oval(0, 0, 0, 0, fill=self.options["headcolor"])

        if min and max:
            self.numberlst = range(min, max)

        else:
            self.numberlst = numberlst

        if self.options["defaultPointer"] in self.numberlst:
            self.current_index = self.options["defaultPointer"]

        else:
            self.current_index = self.numberlst[0]

        self.current_id = ""

        self.step = step if step > 0 else 1
        self.replaceStep = replace_step

        self.initClockText()

        self.canvas.tag_bind("text", "<Button-1>", self.movehand)
        self.canvas.bind("<Configure>", self.updateClockRect)

    def initClockText(self):  # adds texts to the clock

        for index, char in enumerate(self.numberlst, start=self.options["start"]):

            if index % self.step != 0:
                obj = self.canvas.create_oval(0, 0, 5, 5, width=1, tags="text", fill=self.options["textcolor"])

            else:
                obj = self.canvas.create_text(0, 0, text=f"{char}", tags="text",
                                              font=self.options["textfont"], fill=self.options["textcolor"])

            if self.current_index == char:
                self.current_id = obj

    def updateClockRect(self, event):  # updates the size of the circle and moves it to center
        x, y = 10, 10
        width, height = event.width, event.height
        size = width if width < height else height

        if self.options["min-size"] < size < self.options[
            "max-size"]:  # doesn't shrink or expand is the size is not b/w min and max size
            centerX, centerY = width / 2, height / 2
            size -= float(self.canvas.itemcget(self.clock, "width")) + 10

            self.canvas.coords(self.clock, x, y, size, size)
            self.canvas.moveto(self.clock, centerX - size / 2, centerY - size / 2)

            angle = math.radians(360 / len(self.numberlst))
            radius = size / 2 - self.options["textoffset"]

            for index, obj in enumerate(self.canvas.find_withtag("text"), start=self.options['start']):

                _angle = angle * index

                y = centerY + radius * math.sin(_angle)
                x = centerX + radius * math.cos(_angle)

                if index % self.step != 0:
                    self.canvas.coords(obj, x - self.options["alttextwidth"],
                                       y - self.options["alttextwidth"],
                                       x + self.options["alttextwidth"],
                                       y + self.options["alttextwidth"])
                    continue

                self.canvas.coords(obj, x, y)

            self.updateHand()

    def configure(self, **kwargs):  # background, border-color, border-width

        if set(kwargs)-set(self.options):
            raise TypeError(f"Got unexpected arguments '{', '.join(set(kwargs)-set(self.options))}'")

        self.options.update(kwargs)

        self.canvas.itemconfig(self.clock,
                               fill=self.options['bg'],
                               outline=self.options['bdColor'],
                               width=self.options['bdwidth'])

        for obj in self.canvas.find_withtag("text"):
            try:
                self.canvas.itemconfig(obj, font=self.options["textfont"], fill=self.options["textcolor"])

            except tkinter.TclError:
                self.canvas.itemconfig(obj, fill=self.options["textcolor"])

        self.canvas.itemconfig(self.hand_line, fill=self.options["handcolor"],
                               width=self.options["handthickness"],
                               capstyle=self.options["capstyle"])

        self.canvas.itemconfig(self.hand_line, fill=self.options["headcolor"])

    def current(self):
        return self.current_index

    def movehand(self, event: tkinter.Event):

        self.current_id = self.canvas.find_withtag('current')[0]
        self.updateHand()
        self.canvas.event_generate("<<Changed>>")

    def updateHand(self):

        item_bbox = self.canvas.bbox(self.current_id)

        centerX, centerY = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2

        itemCX, itemCY = (item_bbox[2] + item_bbox[0]) / 2, (item_bbox[3] + item_bbox[1]) / 2

        self.canvas.coords(self.hand_line, centerX, centerY, itemCX, itemCY)

        self.canvas.coords(self.hand_end, itemCX - self.options['headsize'],
                           itemCY - self.options['headsize'],
                           itemCX + self.options['headsize'],
                           itemCY + self.options['headsize'])

        try:
            self.current_index = self.canvas.itemcget(self.current_id, "text")

        except tkinter.TclError:
            for obj, number in zip(self.canvas.find_withtag("text"), self.numberlst):

                if self.current_id == obj:
                    self.current_index = str(number)

    def bind(self, seq, callback):
        self.canvas.bind(seq, callback)


if __name__ == "__main__":
    root = tkinter.Tk()

    canvas1 = tkinter.Canvas(root)
    canvas1['bg'] = 'white'
    canvas1.pack(fill='both', expand=1)

    clock = BaseClock(canvas1, min=1, max=13, step=2, bdwidth=10, textoffset=40, start=-2)
    clock.configure(handthickness=7, textcolor= "blue", textfont=("Times", 30, "bold"), alttextwidth=10)
    clock.bind("<<Changed>>", lambda a: print(clock.current()))
    root.mainloop()
