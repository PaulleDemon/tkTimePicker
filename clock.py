import tkinter
import math


class Clock:

    def __init__(self, canvas: tkinter.Canvas, min: int = None, max: int = None,
                 step=0, replace_step: bool = True, numberlst: list = [], **kwargs):

        self.options = {
            "bg": "#ffffff",
            "bdColor": "#000000",
            "bdwidth": 1,
            "textoffset": 20,
            "textfont": ("Times", 20, "normal"),
            "start": 0,
            "defaultPointer": 0, # which number should it be pointing to in the beginning
            "headsize": 20
        }

        self.options.update(kwargs)

        self.canvas = canvas
        self.clock = self.canvas.create_oval(0, 0, 0, 0, fill=self.options["bg"],
                                             outline=self.options["bdColor"],
                                             width=self.options["bdwidth"])

        self.hand_line = self.canvas.create_line(0, 0, 0, 0, fill='black', width=2)
        self.hand_end = self.canvas.create_oval(0, 0, 0, 0, fill='red')

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

    def initClockText(self):

        for index, char in enumerate(self.numberlst, start=self.options["start"]):

            if index % self.step == 0:
                obj = self.canvas.create_oval(0, 0, 5, 5, width=10, tags="text")

            else:
                obj = self.canvas.create_text(0, 0, text=f"{char}", tags="text", font=self.options["textfont"])

            if self.current_index == char:
                print(char)
                self.current_id = obj

    def updateClockRect(self, event):  # updates the size of the circle and moves it to center
        x, y = 10, 10
        width, height = event.width, event.height
        size = width if width < height else height

        if size > 200:  # doesn't shrink if the size is smaller than 200
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

                if index % self.step == 0:
                    self.canvas.coords(obj, x, y, x + 5, y + 5)
                    continue

                self.canvas.coords(obj, x, y)

            # current_coords = self.canvas.coords(self.current_id)
            item_bbox = self.canvas.bbox(self.current_id)
            itemCX, itemCY = (item_bbox[2] + item_bbox[0]) / 2, (item_bbox[3] + item_bbox[1]) / 2

            print(item_bbox, itemCY, itemCX)

            self.canvas.coords(self.hand_line, centerX, centerY, itemCX, itemCY)

            self.canvas.coords(self.hand_end, itemCX-self.options['headsize'],
                                              itemCY - self.options['headsize'],
                                              itemCX + self.options['headsize'],
                                              itemCY + self.options['headsize'])

    def configure(self, **kwargs):  # background, border-color, border-width
        self.options.update(kwargs)

        self.canvas.itemconfig(self.clock,
                               fill=self.options['bg'],
                               outline=self.options['bdColor'],
                               width=self.options['bdwidth'])

    def movehand(self, event):
        # print(event, self.canvas.find_withtag('current')[0])
        self.current_id = self.canvas.find_withtag('current')[0]

        item_rect = self.canvas.coords(self.current_id)
        item_bbox = self.canvas.bbox(self.current_id)
        hand_coords = self.canvas.coords(self.hand_line)

        # self.canvas.create_rectangle(item_bbox, fill='red')

        itemCX, itemCY = (item_bbox[2] + item_bbox[0]) / 2, (item_bbox[3] + item_bbox[1]) / 2

        self.current_index = self.canvas.itemcget(self.current_id, "text")
        print(item_bbox, itemCX, itemCY)
        self.canvas.coords(self.hand_line, hand_coords[0], hand_coords[1], itemCX, itemCY)

        self.canvas.coords(self.hand_end, itemCX - self.options['headsize'],
                                           itemCY - self.options['headsize'],
                                           itemCX + self.options['headsize'],
                                           itemCY + self.options['headsize'])

if __name__ == "__main__":
    root = tkinter.Tk()

    canvas1 = tkinter.Canvas(root)
    canvas1['bg'] = 'white'
    canvas1.pack(fill='both', expand=1)

    clock = Clock(canvas1, min=1, max=13, step=2, bdwidth=10, textoffset=40, start=-2)
    root.mainloop()
