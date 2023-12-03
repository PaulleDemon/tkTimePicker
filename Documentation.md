# Documentation

### Structure
```
timepicker
│
├── __init__.py
├──  basetimepicker.py [BaseClock, SpinBaseClass, HoursClock, MinutesClock]
├── spinlabel.py [HoverClickLabel, PeriodLabel, SpinLabel, LabelGroup]
├── constants.py 
└── clockTimePicker.py [AnalogPicker, SpinTimePickerOld, SpinTimePickerModern, AnalogThemes]
```

### AnalogPicker:
    
This class provides the complete clock timepicker as shown in the image in the [readme.md](https://github.com/PaulleDemon/tkTimePicker/blob/master/Readme.md) file .

The `__init__` method takes the following arguments 
```python 
type=constants.HOURS12 # type of clock, `constants.Hours24` will draw a 24 hours clock
per_orient=constants.VERTICAL # period orientation, `constants.HORIZONTAL` will align AM and PM horizontally
period=constants.AM  # Specifies the default period, `constants.PM` will set PM as default
```

| Methods          |               Arguments                                                       |   Description                                         |
| -----------      | -----------                                                                   |-------                                                |
| configAnalog     | Check The below [base class options](#options)                                | configures both the minutes and hours clock           | 
| configAnalogHrs  | Check The below [base class options](#options)                                | configures the hours clock                            |
| configAnalogMins | Check The below [base class options](#options)                                | configures the minutes clock                          | 
| configSpin       | Check The below [spin class options](#spinoptions)                            | configures both the minutes and hours spin clock      |
| configSpinHrs    | Check The below [spin class options](#spinoptions)                            | configures hours spin                                 |
| configSpinMins   | Check The below [spin class options](#spinoptions)                            | configures minutes spin                               |
| configSeperator  | Check The below [spin class options](#spinoptions)                            | configures separator                                  |
| configurePeriod  | Check The below [spin class options](#spinoptions)                            | configures period                                     |   
| hours            | -                                                                             | returns Hours                                         |
| minutes          | -                                                                             | returns Minutes                                       |
| period           | -                                                                             | returns Period                                        |
| time             | -                                                                             | return a tuple containing hours, minutes and period   |
| setHours         | hrs                                                                           | sets hours  |
| setMinutes       | mins                                                                          | sets minutes   |


### AnalogThemes:
This class provides you with 3 different themes that can be set to `AnalogPicker` widget. 
visit the [Readme Theme](https://github.com/PaulleDemon/tkTimePicker/blob/master/Readme.md#themes)

**Methods Available:**

None of the below methods takes any arguments.

`setNavyBlue`

`setDracula`

`setPurple`

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

The available options used to customize the analog clock widget are as follows

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

This class provides methods to construct a timepicker.

The `__init__` method takes `parent` and `orient` argument. The orient argument specifies how they should be oriented,
either vertically or horizontally.

The below method remains same for both `SpinTimePickerOld` and `SpinTimePickerModern`

| Methods          |               Arguments                                                       |   Description                                             |
| -----------      | -----------                                                                   |-------                                                    |
| addHours12       | -                                                                             | adds 12 hours time                                        | 
| addHours24       | -                                                                             | adds 24 hours time                                        |
| addMinutes       | -                                                                             | adds minutes                                              | 
| addPeriod        | -                                                                             | adds period                                               |
| addAll           | hours[Hours12/Hours24], separator                                             | adds hours(12/24), minutes and period and separator       |
| hours12          | -                                                                             | returns 12 hours time                                     |
| hours24          | -                                                                             | returns 24 hours time                                     |
| hours            | -                                                                             | returns 12hours or 24hours depending upon the type passed |
| minutes          | -                                                                             | returns current minutes                                   |
| period           | -                                                                             | returns current period                                    |
| time             | -                                                                             | returns a tuple containing hours minutes and period       |

### SpinTimePickerModern

This class provides a modern looking timepicker with ability to customize hover color, click color etc.
The user can change the value either using the mouse wheel or directly by using the keyboard.

The `__init__` takes the following arguments.
```python
parent
orient=constants.HORIZONTAL # specifies how hours, minutes is packed  
per_orient=constants.VERTICAL # period orientation either vertical or horizontal
period=constants.AM # default period
```

The below methods are common for both `SpinTimePickerModern` and `SpinTimePickerOld`

| Methods              |               Arguments                                                       |   Description                                              |
| -----------          | -----------                                                                   |-------                                                     |
| configure_12HrsTime  | -                                                                             | customizes 12 hrs time                                     | 
| configure_24HrsTime  | -                                                                             | customizes 24 hours time                                   |
| configure_minute     | -                                                                             | customizes minutes                                         | 
| configure_period     | -                                                                             | customizes period (only for modern timepicker)             |
| configure_seprator   | -                                                                             | customizes seperator                                       |
| configureAll         | -                                                                             | customizes 12 hrs, 24 hrs, minutes, periods and seprerator |

**options available for Modern timepicker:**
The below are set of options available for moder timepicker. Other options that `tkinter.Label` widget accepts
are also applicable for this widget.

<a id="spinoptions"></a>
```python
option = {
            "hovercolor": "#000000",
            "hoverbg": "#ffffff",
            "clickedcolor": "#000000",
            "clickedbg": "#ffffff"
        }
```
options accepted by `tkinter.Spinbox` are also applicable for old time picker
