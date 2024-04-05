import flet as ft

class LoginUI(ft.SafeArea):
    "The Main UI for Login Route"
    def __init__(self) -> None:
        super().__init__()
        self.username = ft.TextField(hint_text="UserName....", max_length=10)
        self.API_text = ft.TextField(
            hint_text="API....",
            max_length=10,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.login_btn = ft.ElevatedButton(text="Login", on_click=self.validate_login)

        self.content = ft.Column(
            controls=[
                self.username,
                self.API_text,
                self.login_btn,
            ]
        )


    def validate_login(self, _) -> None:
        username: str | None = self.username.value
        api: str | None = self.API_text.value
        if username.strip(): #type: ignore
            self.page.client_storage.set("USERNAME", username)  # type: ignore
            if api == "123":
                self.page.client_storage.set("API", api)  # type: ignore
                self.page.go("/chat") #type: ignore
            else:
                self.API_text.error_text = "Wrong API"
                self.API_text.update()
        else:
            self.username.error_text = "fill up your name please"
            self.username.update()
