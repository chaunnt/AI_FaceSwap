import os
import customtkinter as ctk
from typing import Callable, Tuple

import time
import tkinter

ROOT = None
ROOT_HEIGHT = 700
ROOT_WIDTH = 600

PREVIEW = None
PREVIEW_MAX_HEIGHT = 700
PREVIEW_MAX_WIDTH = 1200


def destroy(root):
    root.quit()


LICENSE = "123"


def init_ui():
    def login_event():
        if entry_1.get() == LICENSE:  # This is just a simple demo verification,
            print("OKE")
        else:  # If password doesn't match
            entry_1.configure(text_color="red")
            print("Failed")

    # Define the login page window
    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode("system")

    root_login = ctk.CTk()
    root_login.minsize(ROOT_WIDTH, ROOT_HEIGHT)
    root_login.title("LOGIN PAGE")
    root_login.configure()
    root_login.protocol("WM_DELETE_WINDOW", lambda: destroy(root_login))

    # Add some widgets for login page
    frame = ctk.CTkFrame(master=root_login, width=450, height=450, corner_radius=10)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    label_1 = ctk.CTkLabel(
        master=frame,
        width=400,
        height=60,
        corner_radius=10,
        fg_color=("gray70", "gray35"),
        text="Vui lòng nhập license để tiếp tục",
    )
    label_1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

    entry_1 = ctk.CTkEntry(
        master=frame, corner_radius=20, width=400, placeholder_text="License"
    )
    entry_1.place(relx=0.5, rely=0.52, anchor=tkinter.CENTER)

    status_label = ctk.CTkLabel(root_login, text=None, justify="center")
    status_label.place(relx=0.1, rely=0.9, relwidth=0.8)

    button_login = ctk.CTkButton(
        master=frame,
        text="ĐĂNG NHẬP",
        corner_radius=6,
        command=login_event,
        width=400,
    )
    button_login.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    return root_login
    # root_login.mainloop()
