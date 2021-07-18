from clockTimePicker import AnalogPicker


class AnalogThemes:

    def __init__(self, timepicker: AnalogPicker):
        self.time_picker = timepicker

    def setNavyBlue(self):
        self.time_picker.configAnalog(headcolor="#009688", handcolor="#009688", bg="#eeeeee",
                                      clickedcolor="#ffffff", textcolor="#000000", canvas_bg="#ffffff",
                                      alttextwidth=2, bdwidth=0)

        self.time_picker.configSpin(bg="#009688", height=2, fg="#ffffff", font=("Times", 16), hoverbg="#00695f",
                                    hovercolor="#b6cbd1", clickedbg="#00695f", clickedcolor="#ffffff")

        self.time_picker.configSeperator(font=("Times", 18, "bold"), width=1)

    def setDracula(self):
        self.time_picker.configAnalog(headcolor="#863434", handcolor="#863434", bg="#363636",
                                      clickedcolor="#ffffff", textcolor="#ffffff", canvas_bg="#404040",
                                      alttextwidth=2, bdwidth=0)

        self.time_picker.configSpin(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",
                                    hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")

        self.time_picker.configSeperator(font=("Times", 18, "bold"), width=1)

    def setPurple(self):
        self.time_picker.configAnalog(headcolor="#ee333d", handcolor="#ee333d", bg="#71135c",
                                      clickedcolor="#ffffff", textcolor="#ffffff", canvas_bg="#4e0d3a",
                                      alttextwidth=2, bdwidth=0)

        self.time_picker.configSpin(bg="#71135c", height=2, fg="#ffffff", font=("Times", 16), hoverbg="#3d0430",
                                    hovercolor="#ffffff", clickedbg="#ad118c", clickedcolor="#ffffff")
        self.time_picker.configSeperator(font=("Times", 18, "bold"), width=1)
