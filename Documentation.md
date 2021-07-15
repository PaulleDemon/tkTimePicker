# Documentation

**structure**
```
timepicker
│
├── analogpicker
│   ├──  baseclock.py [BaseClock class]
│   └── clock.py [HoursClock, MinutesClock]
│
├── spinpicker
│   ├── spinlabel.py [HoverClickLabel, PeriodLabel, SpinLabel, LabelGroup]
│   └── spintimepicker.py [_SpinBaseClass, SpinTimePickerOld, SpinTimePickerModern]
│
├── __init__.py
├── constants.py 
└── clockTimePicker.py [AnalogPicker, AnalogThemes]
```

**BaseClock :**
    The `BaseClock` class is the super class of `HoursClock` and `MinutesClock`. 
This contains all the methods necessary to draw the clock, pointer and text.

The `__init__` method takes the following arguments.
```python
canvas: tkinter.Canvas # must provide a tkinter canvas on which the clock shall be drawn
min: int = None # optional
max: int = None # optional
numberlst: list = None # optional
start: int = None # optional
step=None # optional
replace_step: bool = None # optional
```
* The clock and text shall be drawn over the Canvas that is provided 
  through the canvas parameter.

* The min and max, if provided, will make list containing numbers inclusive of max.

* If min and max, is not provided numberlst will be used. The list can contain 
  numbers as well as alphabets, this can be particularly useful when you want 
  alphabets or special characters to be drawn.

* Change the start parameter to adjust the position at which the text is drawn.

* The step parameter, is used to skip few indexes of the list. 
  Eg: In list`[1, 2, 3, 4]` the `step=2` will remove 2 and 4
    
* The replace_step, will replace the empty indexs with a circle. 

> Note: The `init` method will call `setNumberList` method and then `drawClockText`. If either [min, max] or numberlst is not
provided other parameters will not be considered and `setNumberList` and `drawClockText` will not be called.
Alternatively, You can call the `setNumberList` and then `drawClockText` in the same order.

The available options used to customize the widget are as follows
```python
options = {
            "min_size": 200, # min-size beyond which the clock won't shrink
            "max_size": 1080,  # max-size beyond which the clock won't expand
            "bg": "#ffffff", # The background color of the clock 
            "bdColor": "#000000",  # border color of the clock circle
            "bdwidth": 1, # border width of the clock circle
            "textoffset": 20, # Text offset from the outer clock circle
            "textfont": ("Times", 14, "normal"), # Text font
            "textcolor": "#878787", # Text color
            "alttextwidth": 10, # The alternative text is a circle that will be used if replace_step is set to True
            "defaultPointer": 0,  # which number should it be pointing to in the beginning
            "handthickness": 3, # hand thickness
            "handcolor": "#000000", # hand color
            "capstyle": "round",  # 'round', 'projecting', 'butt' The hand end cap
            "headsize": 10,  # The size of the head
            "headcolor": "#000000", # The color of the head
            "headbdwidth": 0, # head border width
            "headbdcolor": "#000000", # head border color
            "clickedcolor": "#c4c4c4", # changes the font color of the text that is clicked
            "halo": 5 # changes the area of which the closest text will be found increasing this will decrease accuracy 
        }
```
You can use `configure` method of this class to change the options.

**HoursClock**

