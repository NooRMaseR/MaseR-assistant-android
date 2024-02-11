import flet as ft


class LoginUI(ft.UserControl):
    def __init__(self) -> None:
        super().__init__()

    def build(self) -> ft.SafeArea:
        self.API_text = ft.TextField(hint_text="API....", max_length=10)
        self.login_btn = ft.ElevatedButton(text="Login", on_click= self.validate_login)

        return ft.SafeArea(
            content= ft.Column(
                controls=[
                    self.API_text,
                    self.login_btn
                ]
            )
        )

    def validate_login(self, _) -> None:
        self.page.client_storage.set("API", self.API_text.value)  # type: ignore
        self.page.go("/chat") #type: ignore
