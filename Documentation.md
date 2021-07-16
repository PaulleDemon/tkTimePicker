# Documentation

### Structure
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

### AnalogPicker:
    
This class provides the complete clock timepicker as shown in the image in the [readme.md](readme.md) file .

The `__init__` method takes the following arguments 
```python 
type=constants.HOURS12 # type of clock Hours24 will draw a 24 hours clock
per_orient=constants.VERTICAL # period orientation constants.HORIZONTAL will align AM and PM horizontally
period=constants.AM  # Specifies the default period
```

| Methods          |               Arguments                                                       |   Description                                         |
| -----------      | -----------                                                                   |-------                                                |
| configAnalog     | Check The below [base class options](#options)                                | configures both the minutes and hours clock           | 
| configAnalogHrs  | Check The below [base class options](#options)                                | configures the hours clock                            |
| configAnalogMins | Check The below [base class options](#options)                                | configures the minutes clock                          | 
| configSpin       | -                                                                             |                                                       |
| configSpinHrs    | -                                                                             |                                                       |
| configSpinMins   | -                                                                             |                                                       |
| configSeperator  | -                                                                             |                                                       |
| configurePeriod  | -                                                                             |                                                       |   
| hours            | -                                                                             |   returns Hours                                       |
| minutes          | -                                                                             |   returns Minutes                                     |
| period           | -                                                                             |   returns Period                                      |
| time             | -                                                                             |   return a tuple containing hours, minutes and period |


### <a id="base"></a> BaseClock :
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

<a id="options"></a>
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

**Method :**

| Methods          |               Arguments                                                       |   Description                                  |
| -----------      | -----------                                                                   |-------                                         |
| setNumberList    | min[int], max[int], numberlst[list], start[int], step[int], replace_step[bool]| Used to set up the clock characters            | 
| drawClockText    | -                                                                             | draws the clock characters on the canvas       |
| configure        | refer to the above options                                                    | Used to customize the widget                   | 
| current          | -                                                                             | Gets the current value the hand is pointing to |

**Events :**

`<<HandMoved>>` - This event is generated whenever the hand(pointer) is moved.

### HoursClock:

sets up hour clock based on the type provided. `constants.HOURS12` will set up 12 hours clock and 
`constants.HOURS24` will setup 24 hours clock.

**Options :** canvas: tkinter.Canvas, type: int = constants.HOURS12

**Methods :**
`getHours` -This takes no arguments and returns the current hour it is pointing to.

**Events :**
`<<HoursChanged>>` - This event is generated when hours is changed.

### MinutesClock:

Draws the minutes clock. By default it will replace numbers with oval to reduce cluttering. You can change with that 
with the below options.

**options :** canvas: tkinter.Canvas, step=5, replace_step=True

**Methods :** `getMinutes`- Takes no arguments and returns the current minutes.

**Events :** `<<MinChanged>>` - Generated when the minutes is changed.

### SpinTimePickerOld

| Methods          |               Arguments                                                       |   Description                                  |
| -----------      | -----------                                                                   |-------                                         |
| addHours12       | min[int], max[int], numberlst[list], start[int], step[int], replace_step[bool]| Used to set up the clock characters            | 
| addHours24       | -                                                                             | draws the clock characters on the canvas       |
| addMinutes       | refer to the above options                                                    | Used to customize the widget                   | 
| addPeriod        | -                                                                             | Gets the current value the hand is pointing to |
| addAll           |
| hours12        | -                                                                             | Gets the current value the hand is pointing to |
| hours24        | -                                                                             | Gets the current value the hand is pointing to |
| addPeriod        | -                                                                             | Gets the current value the hand is pointing to |
| addPeriod        | -                                                                             | Gets the current value the hand is pointing to |
