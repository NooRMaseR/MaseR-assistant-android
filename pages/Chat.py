from widgets.animations import AnimateChatResponse
from widgets.Send_btn import Send_btn
import platform, requests, sys
import flet as ft

# * check if using mobile for modules
isMobile: bool = False if platform.system() in ["Windows", "Macos"] else True
if not isMobile:
    import speech_recognition as sr 
    from io import BytesIO
    import pygame 
    import base64


class ChatUI(ft.UserControl):
    "The Main UI for Chat Route"
    def __init__(self, window: ft.Page) -> None:
        super().__init__()
        pygame.mixer.init()
        self.er = None
        self.version = "v1.1.1"
        self.window: ft.Page = window
        self.window.on_resize = self.handel_resize
        self.using_mic: bool = False
        self.mic_error: bool = False
        self.langs: dict[str, str] = {
            "English (Australia)": "com.au",
            "English (United Kingdom)": "com.uk",
            "English (United States)": "us",
            "English (Canada)": "ca",
            "English (India)": "co.in",
            "English (Ireland)": "ie",
            "English (South Africa)": "co.za",
            "French (Canada)": "ca",
            "French (France)": "fr",
            "Portuguese (Brazil)": "com.pr",
            "Portuguese (Portugal)": "pt",
            "Spanish (Mexico)": "com.mx",
            "Spanish (Spain)": "es",
            "Spanish (United States)": "us"   
        }
        # self.file_picker: ft.FilePicker = ft.FilePicker(
        #     on_result=self.change_user_profile
        # )
        # self.window.overlay.append(self.file_picker)

        self.username: str = (
            "User"  # type: ignore
            if not self.window.client_storage.get("USERNAME")  # type: ignore
            else self.window.client_storage.get("USERNAME")  # type: ignore
        )
        self.theme: str = (
            "system"  # type: ignore
            if not self.window.client_storage.get("THEME")  # type: ignore
            else self.window.client_storage.get("THEME")  # type: ignore
        )
        self.acc: str = (
            "English (United States)"
            if not self.window.client_storage.get("ACC")  # type: ignore
            else self.window.client_storage.get("ACC")  # type: ignore
        )

    def Appbar(self) -> ft.AppBar:
        self.voice_enable = ft.Checkbox(
            value=False,
            label="Enable Voice Chat",
            label_position=ft.LabelPosition.RIGHT,
            disabled=True if isMobile else False
        )

        return ft.AppBar(
            leading=ft.CircleAvatar(
                content=ft.Image("assets/my_pic.jpeg", border_radius=50)
            ),
            title=ft.Text("MaseR Assistant"),
            center_title=True,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            content=self.voice_enable,
                        ),
                        ft.PopupMenuItem(
                            text="Settings",
                            icon=ft.icons.SETTINGS,
                            on_click=lambda _: self.window.show_bottom_sheet(self.bottom_sheet_settings),
                        ),
                        ft.PopupMenuItem(
                            text="clear conversation",
                            icon=ft.icons.CLEAR_ALL,
                            on_click=lambda _: self.window.show_dialog(self.dialog_clear),
                        ),
                        ft.PopupMenuItem(
                            text="About",
                            icon=ft.icons.INFO,
                            on_click=lambda _: self.window.show_dialog(self.dialog_about),
                        ),
                        ft.PopupMenuItem(
                            text="Logout",
                            icon=ft.icons.LOGOUT,
                            on_click=lambda _: self.window.show_dialog(self.dialog_logout),
                        ),
                    ]
                )
            ],
        )

    def logout(self, _) -> None:
        self.clear_conversation(_)
        self.window.close_dialog()
        self.window.client_storage.remove("API")  # type: ignore
        self.window.go("/login")

    def build(self) -> ft.SafeArea:

        # a container for the sent messages
        self.msgs_container: ft.Container = ft.Container(
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                on_scroll_interval=5,
                auto_scroll=True,
                height=self.window.height - 200,
                controls=[ft.ListView(auto_scroll=True, spacing=20)],
            )
        )
        # TextField to type a question
        self.textbox: ft.TextField = ft.TextField(
            hint_text="ask....",
            multiline=True,
            max_lines=2,
            expand=True,
            filled=True,
            border_radius=10,
            autocorrect=True,
            read_only=False,
            shift_enter=True,
            on_submit=self.send_msg,
        )

        # microphone
        self.microphone = ft.IconButton(
            "mic",
            on_click= self.mic_on,
            tooltip="Talk With Mic (SOON)" if isMobile else "Talk With Mic",
            disabled= True if isMobile else False
        )

        self.send_btn = Send_btn(
            lambda e: [self.enable_mic_when_send_btn(), self.send_msg(e)],
            self.textbox
        )

        # loading animation when sending msg
        self.loading: ft.ProgressBar = ft.ProgressBar(visible=False)

        msg: str = (
            f"""
        appName: MaseR Assistant
version: {self.version}
Developer: NooR MaseR
        """.strip()
        )

        # adialog to display for About
        self.dialog_about = ft.AlertDialog(
            modal=True,
            title=ft.Text("About"),
            content=ft.Text(msg, selectable=True),
            actions=[
                ft.ElevatedButton(
                    "Close", on_click=lambda _: self.window.close_dialog()
                ),
            ],
        )

        self.dialog_clear = ft.CupertinoAlertDialog(
            title=ft.Text("Clear Chat ?"),
            content=ft.Text("This will clear all the messages."),
            actions=[
                ft.CupertinoDialogAction(
                    "Cancel",
                    is_default_action=True,
                    on_click=lambda _: self.window.close_dialog(),
                ),
                ft.CupertinoDialogAction(
                    "Ok",
                    is_destructive_action=True,
                    on_click=lambda _: [self.clear_conversation(_), self.window.close_dialog()]
                ),
            ],
        )

        self.dialog_logout = ft.CupertinoAlertDialog(
            title=ft.Text("Log Out ?"),
            content=ft.Text("Are You Sure You Want To Log Out ?"),
            actions=[
                ft.CupertinoDialogAction(
                    "Cancel",
                    is_default_action=True,
                    on_click= lambda _: self.window.close_dialog(),
                ),
                ft.CupertinoDialogAction(
                    "Ok",
                    is_destructive_action=True,
                    on_click= self.logout,
                ),
            ],
        )

        self.profile_pic = ft.Container(
            content=ft.CircleAvatar(
                content=ft.Image("assets/user.png", border_radius=50)
            ),
            # ink=True,
            # on_click=lambda _: self.file_picker.pick_files(
            #     dialog_title="Pick a photo",
            #     file_type=ft.FilePickerFileType.IMAGE,
            #     allow_multiple=False,
            # ),
            tooltip="Change Profile (SOON)",
        )

        # A bottom sheet to display for settings
        self.bottom_sheet_settings = ft.BottomSheet(
            # show_drag_handle=True,
            dismissible=False,
            enable_drag=False,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("settings", size=24, weight=ft.FontWeight.W_500),
                    ft.Divider(),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[ft.Text("User Profile"), self.profile_pic],
                    ),
                    ft.Container(
                        padding=ft.padding.only(left=5, right=5),
                        margin=ft.margin.only(bottom=5),
                        content=ft.Column(
                            controls=[
                                ft.TextField(label="User Name", value=self.username),
                                ft.Dropdown(
                                    on_change=self.change_theme,
                                    label="theme",
                                    value=self.theme,
                                    options=[
                                        ft.dropdown.Option(text="system"),
                                        ft.dropdown.Option(text="light"),
                                        ft.dropdown.Option(text="dark"),
                                    ],
                                ),
                                ft.Dropdown(
                                    on_change=self.change_acc,
                                    label="voice accent",
                                    value=self.acc,
                                    error_text="Not working for now" if isMobile else None,
                                    options=[
                                        ft.dropdown.Option(text=lang) for lang in self.langs.keys()
                                    ],
                                ),
                            ]
                        ),
                    ),
                    ft.Container(height=5),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.ElevatedButton(
                                "Close", on_click=self.close_bottom_sheet
                            ),
                        ],
                    ),
                    ft.Container(height=5),
                ],
            ),
        )

        return ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.msgs_container,
                    self.loading,
                    ft.Container(
                        shadow=ft.BoxShadow(
                            color=ft.colors.BLACK12,
                            # spread_radius=10,
                            blur_radius=40,
                            offset=ft.Offset(0, -40),
                            blur_style=ft.ShadowBlurStyle.NORMAL
                        ),
                        content= ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                self.textbox,
                                self.microphone,
                                self.send_btn,
                            ],
                        ),
                    )
                ],
            )
        )

    def enable_mic_when_send_btn(self) -> None:
        self.mic_error = False
        
    def mic_on(self,_) -> None:
        mic = sr.Recognizer()
        self.mic_error = False
        self.using_mic = True
        try:
            with sr.Microphone() as source:

                self.textbox.value = "Listening....."
                self.textbox.disabled = True
                self.send_btn.disabled = True
                self.microphone.disabled = True
                self.textbox.update()
                self.send_btn.update()
                self.microphone.update()
                print("lisnning...")
                audio = mic.listen(source)  # listen for the user's voice activity on the microphone
                self.text_from_mic = str(mic.recognize_google(audio))  # convert speech to text
                print(self.text_from_mic)
                self.send_msg(_)
                del mic
                self.textbox.value = None
                self.textbox.disabled = False
                self.send_btn.disabled = False
                self.textbox.update()
                self.send_btn.update()
        except Exception as e:
            self.er = e
            print(f"error: {e}")
            self.mic_error = True
            self.textbox.value = None
            self.using_mic = False
            self.textbox.disabled = False
            self.send_btn.disabled = False
            self.microphone.disabled = False
            self.textbox.update()
            self.send_btn.update()
            self.microphone.update()

    def change_acc(self, e: ft.ControlEvent) -> None:
        self.window.client_storage.set("ACC", e.data) #type: ignore
        self.acc = e.data

    def change_theme(self, e: ft.ControlEvent):
        self.window.client_storage.set("THEME", e.data)  # type: ignore
        self.window.theme_mode = e.data  # type: ignore
        self.window.update()

    def clear_conversation(self, _: ft.ControlEvent):
        "a function for deleting all messages in the conversation"
        self.msgs_container.content.controls[0].controls.clear()  # type:ignore
        self.msgs_container.content.update()  # type:ignore

    def send_msg(self, _: ft.ControlEvent) -> None:
        """
        sending a `POST` request to the URL
        "https://maser-assistant.onrender.com/chat/quary-android" with a JSON payload. The payload
        includes the `quary` (question), `voiceEnabled` (a boolean indicating whether voice is
        enabled), `acc` (for accent) and `APIkey` (an API key). The request also includes the `Content-Type` header
        set to `application/json`.
        """
        if not self.mic_error:
            question: str = str(self.textbox.value).strip() if not self.using_mic else str(self.text_from_mic)
        else:
            question: str = "error"

        self.using_mic = False
        if question:
            self.loading.visible = True
            self.loading.update()
            self.microphone.disabled = True
            self.microphone.update()
            self.textbox.value = "Connecting...."
            self.textbox.read_only = True
            user_question = CreateUserQuestion(self.username, question)
            self.msgs_container.content.controls[0].controls.append(user_question)  # type: ignore
            # self.msgs_container.content.controls[0].controls.append(ft.Text(self.er if self.er else "No Error")) #? check for error for mobile
            self.msgs_container.content.controls[0].update()  # type: ignore
            self.textbox.update()

            try:
                error = False
                self.req = requests.post(
                    url="https://maser-assistant.onrender.com/chat/quary-android",
                    json={
                        "quary": question,
                        "voiceEnabled": True if self.voice_enable.value else False,
                        "acc": self.langs.get(self.acc),
                        "APIkey": "NooRMaseR1234567892024",
                    },
                    headers={"Content-Type": "application/json"},
                )
                response: dict = self.req.json()
                self.req.close()
                self.question: str | None = response.get("result")

                # ? enable for running audio
                if response.get("aud"):
                    self.base64_audio = base64.b64decode(response["aud"])
                    pygame.mixer.music.load(BytesIO(self.base64_audio))
                    pygame.mixer.music.play()
            except Exception as e:
                print(e, file=sys.stderr)
                self.question = "error while connecting"
                error = True

            answer = CreateChatResponse(self.question, error, self.mic_error)  # type: ignore
            self.msgs_container.content.controls[0].controls.append(answer)  # type: ignore
            self.msgs_container.content.controls[0].update()  # type: ignore
            AnimateChatResponse(answer)
            self.loading.visible = False
            self.textbox.value = None
            self.textbox.read_only = False
            self.microphone.disabled = False
            self.microphone.update()
            self.update()

    def close_bottom_sheet(self, _: ft.ControlEvent) -> None:
        new_username_field: str = self.window.bottom_sheet.content.controls[3].content.controls[0].value.strip()  # type: ignore
        if new_username_field:
            self.edit_user(new_username_field)
            self.window.close_bottom_sheet()

    def edit_user(self, new_username: str) -> None:
        self.window.client_storage.set("USERNAME", new_username)  # type: ignore
        self.username = new_username

    def handel_resize(self, _: ft.ControlEvent) -> None:
        self.msgs_container.height = self.window.height - 200
        self.update()

    #! can not use on mobile
    # def change_user_profile(self, e: ft.FilePickerResultEvent) -> None:
    #     # breakpoint()
    #     self.__image_path: str = e.files[0].path  # type: ignore
    #     if os.path.exists(self.__image_path) and os.path.isfile(self.__image_path):
    #         print(f"{self.__image_path = }")
    # Image.open(self.__image_path).save("assets/user.png", format="PNG")
    # self.window.bottom_sheet.content.controls[2].controls[1].content.content.src = "assets/user.png" # type: ignore
    # self.window.bottom_sheet.content.controls[2].controls[1].content.content.update() # type: ignore


class CreateChatResponse(ft.UserControl):
    def __init__(self, answer: str | None, error: bool, mic_error: bool) -> None:
        super().__init__()
        self.widget: ft.Text
        self.answer: str | None = answer
        self.error: bool = error
        self.mic_error: bool = mic_error

    def build(self) -> ft.Container:
        self.widget = ft.Text(
            self.answer if not self.mic_error else "error wile initializing microphone",
            color=ft.colors.WHITE if self.error or self.mic_error else None
        )
        return ft.Container(
            bgcolor=ft.colors.RED_700 if self.error or self.mic_error else None,
            content=ft.ListTile(
                title=ft.Text(
                    "MaseR Assistant",
                    color=ft.colors.WHITE if self.error or self.mic_error else None,
                ),
                leading=ft.CircleAvatar(
                    content=ft.Image("assets/my_pic.jpeg", border_radius=50)
                ),
                subtitle=self.widget,
                trailing=ft.IconButton(
                    ft.icons.COPY_OUTLINED,
                    icon_color=(
                        ft.colors.WHITE if self.error or self.mic_error else None
                    ),
                    on_click=self.copy_msg,
                    tooltip="Copy",
                ),
            ),
        )

    def copy_msg(self, e: ft.ControlEvent) -> None:
        e.page.set_clipboard(self.answer)
        e.page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Copied"), show_close_icon=True, duration=2500)
        )


class CreateUserQuestion(ft.UserControl):
    def __init__(self, user_name: str, question: str):
        super().__init__()
        self.question: str = question
        self.user_name = user_name

    def build(self) -> ft.ListTile:
        return ft.ListTile(
            title=ft.Text(self.user_name),
            leading=ft.CircleAvatar(
                content=ft.Image("assets/user.png", border_radius=50)
            ),
            subtitle=ft.Text(self.question),
            trailing=ft.IconButton(
                ft.icons.COPY_OUTLINED, on_click=self.copy_msg, tooltip="Copy"
            ),
        )

    def copy_msg(self, e: ft.ControlEvent) -> None:
        e.page.set_clipboard(self.question)
        e.page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Copied"), show_close_icon=True, duration=2500)
        )
