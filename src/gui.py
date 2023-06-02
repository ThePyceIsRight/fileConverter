import customtkinter
import tkinter


def guiMaster():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.geometry("1000x700")
    root.title("Editor")
    root.iconbitmap("assets/gui/logo.ico")

    # https://stackoverflow.com/a/28519037/17312223
    # above link explains how to show animated gif in tkinter window
    # this may work also? https://stackoverflow.com/a/72659985/17312223



    root.mainloop()