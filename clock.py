import tkinter
import math


class Clock:

    def __init__(self, canvas: tkinter.Canvas, min: int=None, max: int=None, numberlst: list=[],**kwargs):
        options = {
                    "bg": "#ffffff",
                    "bdColor": "#000000",
                    "bdwidth": 1,
                    "textoffset": 20
                   }
        options.update(kwargs)

        self.canvas = canvas
        self.clock = self.canvas.create_oval(0, 0, 0, 0, fill=options["bg"],
                                                outline=options["bdColor"],
                                                width=options["bdwidth"])

        self.text_offset = options["textoffset"]

        if min and max:
            self.numberlst = range(min, max)

        else:
            self.numberlst = numberlst

        self.canvas.bind("<Configure>", self.updateClockRect)

    def updateClockRect(self, event):  # updates the size of the circle and moves it to center
        x, y = 10, 10
        width, height = event.width, event.height
        size = width if width < height else height

        if size > 200: # doesn't shrink if the size is smaller than 200
            centerX, centerY = width/2, height/2
            size -= float(self.canvas.itemcget(self.clock, "width"))+10

            self.canvas.coords(self.clock, x, y, size, size)
            self.canvas.moveto(self.clock, centerX-size/2, centerY-size/2)

            angle = math.radians(360 / len(self.numberlst))
            radius = size/2 - self.text_offset

            self.canvas.delete("text")

            for index, char in enumerate(self.numberlst, start=-5):
                _angle = angle * index

                y = centerY + radius * math.sin(_angle)
                x = centerX+ radius * math.cos(_angle)
                print(_angle)
                self.canvas.create_text(x, y, text=f"{char}", tags=("text"))

    def configure(self, bg="", bdcolor="", bdwidth=None): # background, border-color, border-width

        if not bg:
            bg = self.canvas.itemcget(self.clock, "fill")

        if not bdcolor:
            bdcolor = self.canvas.itemcget(self.clock, "outline")

        if not bdwidth:
            bdwidth = self.canvas.itemcget(self.clock, "width")

        self.canvas.itemconfig(self.clock, fill=bg, outline=bdcolor, width=bdwidth)


if __name__ == "__main__":
    root = tkinter.Tk()

    canvas1 = tkinter.Canvas(root)
    canvas1['bg'] = 'white'
    canvas1.pack(fill='both', expand=1)

    clock = Clock(canvas1, min=1, max=12, bdwidth=10, textoffset=40)
    root.mainloop()
