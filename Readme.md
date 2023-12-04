# tkTimePicker

This is a simple and fully customizable timepicker widgets made for tkinter. You can make use of
three types of timepicker:

1. clock timepicker
2. old-spin timepicker
3. modern-spin timepicker

quick example

```python
import tkinter as tk
from tktimepicker import AnalogPicker, AnalogThemes
# note: you can also make use of mouse wheel or keyboard to scroll or enter the spin timepicker
root = tk.Tk()

time_picker = AnalogPicker(root)
time_picker.pack(expand=True, fill="both")

# theme = AnalogThemes(time_picker)
# theme.setDracula()

root.mainloop()
```

For more examples refer [Examples](https://github.com/PaulleDemon/tkTimePicker/tree/master/examples),
For documentation read [Documentation](https://browsedocs.com/BB3qVRTUgrko)

**Clock time picker**

Available themes:

<a id="themes"></a>
**NavyBlue**

![NavyBlue](https://github.com/PaulleDemon/tkTimePicker/blob/master/ReadMeImages/NavyBlue.png?raw=True)

**Dracula**

![Dracula](https://github.com/PaulleDemon/tkTimePicker/blob/master/ReadMeImages/DraculaDark.png?raw=True)

**purple**

![Purple](https://github.com/PaulleDemon/tkTimePicker/blob/master/ReadMeImages/Purple.png?raw=True)

**Old-spin timepicker**

![old-spin timepicker](https://github.com/PaulleDemon/tkTimePicker/blob/master/ReadMeImages/SpinTimeold.png?raw=True)

**Modern-spin timepicker**

![old-spin timepicker](https://github.com/PaulleDemon/tkTimePicker/blob/master/ReadMeImages/SpinTimeModern.png?raw=True)

> Note: you can also use mouse wheel to change the time when using modern timepicker, 
> or you can also make use of keypress to change time if you hover over the timepicker.


> Note: You can also have your own colors besides this. you can also make use of 24 hrs clock, read the
> documentation for more info.

**Other libraries you might be interested in**

* [tkvideoplayer](https://pypi.org/project/tkvideoplayer/) - Plays video files in tkinter.

* [tkstylesheet](https://pypi.org/project/tkstylesheet/) - Helps you style your tkinter application using stylesheets.

* [PyCollision](https://pypi.org/project/PyCollision/) - Helps you draw hitboxes for 2d games.


**Support Open-source:**
  
I'm a passionate supporter of open-source initiatives. Developing and maintaining open-source projects requires a significant commitment of time and effort. My goal is to transition to working on open-source projects on a full-time basis. If you'd like to support me and the open-source community, please consider making small donations so I can dedicate more time to open-source work.
[Donate](https://www.buymeacoffee.com/ArtPaul)

[<img src="https://github.com/PaulleDemon/PaulleDemon/blob/main/images/buy-me-coffee.png" height="100px" width="350px">](https://www.buymeacoffee.com/ArtPaul)

**Other ways to support**

The site [https://adostrings.com](https://adostrings.com) is for sale to support open-source initiatives. Send mail to paul@adostrings.com to get to know more.

You can also purchase the smaller version of the above site at.
[https://creators.adostrings.com](https://creators.adostrings.com) or [https://creators.adostrings.com/startups](https://creators.adostrings.com/startups) 
