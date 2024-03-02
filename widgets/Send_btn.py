from typing import Callable
from .animations import AnimateChatResponse
import flet as ft


class Send_btn(ft.UserControl):
    def __init__(self, sendit: Callable, message_field: ft.TextField) -> None:
        super().__init__()
        self.sendit = sendit
        self.message_feild = message_field

    def build(self) -> ft.Row:
        self.btn = ft.IconButton(
            icon=ft.icons.SEND_SHARP,
            icon_color="white",
            rotate=ft.Rotate(angle=55),
            offset=ft.Offset(0, 0),
            animate_scale=ft.Animation(900, ft.AnimationCurve.DECELERATE),
            animate_rotation=ft.Animation(900, ft.AnimationCurve.DECELERATE),
            animate_offset=ft.Animation(900, ft.AnimationCurve.DECELERATE),
        )
        self.text = ft.Text(
            value="Send",
            color="white",
            opacity=0,
            offset=ft.Offset(1.5, 0),
            weight=ft.FontWeight.W_700,
            animate_scale=ft.Animation(900, ft.AnimationCurve.DECELERATE),
            animate_offset=ft.Animation(900, ft.AnimationCurve.DECELERATE),
            animate_opacity=ft.Animation(700, ft.AnimationCurve.DECELERATE),
        )
        self.container = ft.Container(
            content=ft.Row(controls=[self.btn, self.text], alignment="center"),  # type: ignore
            bgcolor=ft.colors.BLUE,
            border_radius=50,
            width=40,  # 130 to make it full
            on_hover=AnimateChatResponse.animate_send_btnOnHover,
            on_click=self.Send_Message,
            alignment=ft.alignment.center,
            animate=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            gradient=ft.LinearGradient(
                colors=["#DB44FF", "#EB9AFF"],
                begin=ft.alignment.center_left,
                end=ft.alignment.center_right,
            ),
        )
        return ft.Row(controls=[self.container], expand=True, alignment="center")  # type: ignore

    def Send_Message(self, e) -> None:
        AnimateChatResponse.animate_send_btnOnClick(e)
        self.sendit(str(self.message_feild.value))
