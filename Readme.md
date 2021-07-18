# tkTimePicker

This is a simple and fully customizable timepicker widgets made for tkinter. You can make use of
three types of timepicker:

1. clock timepicker
2. old-spin timepicker
3. modern-spin timepicker

quick example

```python
import tkinter as tk
from tktimepicker import clockTimePicker

root = tk.Tk()

time_picker = clockTimePicker.AnalogPicker(root)
time_picker.pack()

root.mainloop()
```

for more examples refer [Examples](examples),
for documentation read [Documentation](Documentation.md)

**Clock time picker**

Available themes:

<a id="themes"></a>
**NavyBlue**

![NavyBlue](ReadMeImages/NavyBlue.png)

**Dracula**

![Dracula](ReadMeImages/DraculaDark.png)

**purple**

![Purple](ReadMeImages/Purple.png)

**Old-spin timepicker**

![old-spin timepicker](ReadMeImages/SpinTimeold.png)

**Modern-spin timepicker**

![old-spin timepicker](ReadMeImages/SpinTimeModern.png)
