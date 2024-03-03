import time
import random
import flet as ft


class AnimateChatResponse():
    def __init__(self, widget) -> None:
        self.widget = widget
        # getting the response to get the value (text)
        self.text = str(self.widget.widget.value)
        # set the value to none to add the new text
        self.widget.widget.value = None
        # # update the text
        self.widget.widget.update()
        # start the ghost typing effect
        self.Start_effect()

    def Start_effect(self) -> None:
        # looping for each msg for adding it to the msg holder
        for i in range(len(self.text)):
            self.widget.widget.value += self.text[i]  # type: ignore
            self.widget.widget.update()  # type: ignore
            number: int = random.randrange(1, 5)
            time.sleep(number / 100)

    @staticmethod
    def animate_send_btnOnHover(e: ft.ControlEvent) -> None:
        state = e.data
        container: ft.Container = e.control
        icon_button: ft.IconButton = e.control.content.controls[0]
        text: ft.Text = e.control.content.controls[1]
        if state == "true":
            container.width = 130
            icon_button.scale = ft.Scale(1.50)
            icon_button.rotate.angle = 56.55
            text.scale = ft.Scale(1.30)
            text.offset = ft.Offset(0, 0)
            text.opacity = 1
        elif state == "false":
            container.width = 40
            icon_button.scale = ft.Scale(1)
            icon_button.rotate.angle -= 1.55 #55
            text.scale = ft.Scale(1.30)
            text.offset = ft.Offset(1.5, 0)
            text.opacity = 0
            icon_button.offset = ft.Offset(0, 0)

        container.update()
        icon_button.update()
        text.update()

    @staticmethod
    def animate_send_btnOnClick(e: ft.ControlEvent) -> None:
        container: ft.Container = e.control
        icon_button: ft.IconButton = e.control.content.controls[0]
        text: ft.Text = e.control.content.controls[1]
        text.opacity = 0
        container.width = 130
        icon_button.offset = ft.Offset(1.5, 0)
        container.update()
        icon_button.update()
        text.update()
