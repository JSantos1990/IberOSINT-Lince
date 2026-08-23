import customtkinter as ctk
import config
from PIL import Image


class Header(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color=config.BACKGROUND,
            corner_radius=0
        )

        self.pack(fill="x", padx=25, pady=(20, 10))

        banner = ctk.CTkImage(
            light_image=Image.open(
                "/home/iberosint/IberOSINT/Launcher/assets/images/iberosint_lince.jpg"
            ),
            dark_image=Image.open(
                "/home/iberosint/IberOSINT/Launcher/assets/images/iberosint_lince.jpg"
            ),
            size=(900,130)
        )

        header = ctk.CTkLabel(
            self,
            image=banner,
            text=""
        )

        header.pack(
            anchor="w",
            pady=(0,5)
        )