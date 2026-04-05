import customtkinter as ctk
from ui import ImageUI

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    root = ctk.CTk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    root.geometry(f"{width}x{height}")
    root.title("Image Processor Pro")

    app = ImageUI(root)
    root.mainloop()