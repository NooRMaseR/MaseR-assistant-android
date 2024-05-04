from pages.Login import LoginUI
from pages.Chat import ChatUI
import flet_easy as fs
import flet as ft

# ? SpeechRecognition==3.10.0

app = fs.FletEasy(route_init="/chat", route_login="/login")


@app.config # type: ignore
async def app_config(page: ft.Page):
    THEME: str | None = await page.client_storage.get_async("THEME") 
    if THEME:
        page.theme_mode = THEME # type: ignore
    else:
        THEME = "system"
        await page.client_storage.set_async("THEME", THEME)
        page.theme_mode = THEME # type: ignore


@app.page("/chat", protected_route=True, share_data=True)
def main(data: fs.Datasy) -> ft.View:
    page = data.page
    page.title = "MaseR Assistant"

    # page.window_width = 366  #! remove or comment this line when building mobile app (for testing on desktop only)
    # page.window_center()  #! remove or comment this line when building mobile app (for testing on desktop only)
    UI = ChatUI(page)
    return ft.View("/chat", controls=[UI], appbar=UI.Appbar())


@app.page("/login", page_clear=True)
def login_page(data: fs.Datasy) -> ft.View:
    page = data.page
    page.title = "Log in"

    return ft.View("/login", controls=[LoginUI()])


@app.login
def login(page: fs.Datasy) -> bool:
    if page.page.client_storage.get("API") == "123":  # type: ignore
        return True
    return False


app.run(assets_dir="assets")
