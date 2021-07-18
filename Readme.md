# tkTimePicker

This is a simple and fully customizable timepicker widgets made for tkinter. You can make use of
three types of timepicker:

1. clock timepicker
2. old-spin timepicker
3. modern-spin timepicker

quick example

```python
import tkinter as tk
from tktimepicker import timepicker

root = tk.Tk()

time_picker = timepicker.AnalogPicker(root)
time_picker.pack()

root.mainloop()
```

for more examples refer [Examples](https://github.com/PaulleDemon/tkTimePicker/tree/master/examples),
for documentation read [Documentation](https://github.com/PaulleDemon/tkTimePicker/blob/master/Documentation.md)

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
