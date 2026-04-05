import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from logic import process_images

class ImageUI:
    def __init__(self, root):
        self.root = root

        self.images = []
        self.output = ""
        self.preview_img = None

        self.downloads = os.path.join(os.path.expanduser("~"), "Descargas")

        # ===== Layout =====
        self.sidebar = ctk.CTkFrame(root, width=300)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.main = ctk.CTkFrame(root)
        self.main.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ===== Sidebar =====
        ctk.CTkLabel(self.sidebar, text="Opciones", font=("Arial", 18)).pack(pady=10)

        ctk.CTkButton(self.sidebar, text="📂 Cargar imágenes",
                      command=self.load_images).pack(pady=5)

        ctk.CTkButton(self.sidebar, text="📁 Cargar carpeta",
                      command=self.load_folder).pack(pady=5)

        ctk.CTkButton(self.sidebar, text="📦 Carpeta destino",
                      command=self.select_output).pack(pady=5)

        # ===== LISTA REAL =====
        ctk.CTkLabel(self.sidebar, text="Archivos").pack(pady=5)

        self.listbox = ctk.CTkScrollableFrame(self.sidebar, height=150)
        self.listbox.pack(fill="x", padx=5)

        # ===== Renombrar =====
        ctk.CTkLabel(self.sidebar, text="Nuevo nombre base").pack(pady=5)
        self.rename_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: imagen")
        self.rename_entry.pack(pady=5)

        # ===== Tamaño =====
        ctk.CTkLabel(self.sidebar, text="Tamaño").pack(pady=10)

        self.w = ctk.CTkEntry(self.sidebar, placeholder_text="Ancho")
        self.w.pack(pady=2)

        self.h = ctk.CTkEntry(self.sidebar, placeholder_text="Alto")
        self.h.pack(pady=2)

        sizes = [(128,128),(512,512),(1024,1024),(1920,1080)]
        for w,h in sizes:
            ctk.CTkButton(self.sidebar, text=f"{w}x{h}",
                          command=lambda w=w,h=h: self.set_size(w,h)).pack(pady=2)

        # ===== Opciones =====
        self.keep = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.sidebar, text="Mantener proporción",
                        variable=self.keep).pack(pady=5)

        self.format = ctk.StringVar(value="PNG")
        ctk.CTkOptionMenu(self.sidebar, variable=self.format,
                          values=["PNG","JPG","WEBP","ICO"]).pack(pady=5)

        # ===== Botones =====
        ctk.CTkButton(self.sidebar, text="🚀 Procesar",
                      command=self.run).pack(pady=10)

        ctk.CTkButton(self.sidebar, text="🧹 Limpiar todo",
                      command=self.clear_all, fg_color="red").pack(pady=5)

        self.status = ctk.CTkLabel(self.sidebar, text="", wraplength=250)
        self.status.pack(pady=5)

        # ===== Preview =====
        ctk.CTkLabel(self.main, text="Vista previa", font=("Arial", 16)).pack(pady=10)

        self.canvas = ctk.CTkCanvas(self.main, bg="#222")
        self.canvas.pack(fill="both", expand=True)

    # ===== FUNCIONES =====

    def update_list(self):
        for widget in self.listbox.winfo_children():
            widget.destroy()

        for path in self.images:
            name = os.path.basename(path)
            ctk.CTkLabel(self.listbox, text=name).pack(anchor="w")

    def clear_all(self):
        self.images = []
        self.output = ""
        self.preview_img = None

        self.w.delete(0, "end")
        self.h.delete(0, "end")
        self.rename_entry.delete(0, "end")

        self.status.configure(text="")

        self.canvas.delete("all")

        for widget in self.listbox.winfo_children():
            widget.destroy()

    def set_size(self, w, h):
        self.w.delete(0, "end")
        self.w.insert(0, str(w))
        self.h.delete(0, "end")
        self.h.insert(0, str(h))

    def show_preview(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((400, 400))

            self.preview_img = ImageTk.PhotoImage(img)

            self.canvas.delete("all")
            self.canvas.update()

            self.canvas.create_image(
                self.canvas.winfo_width() // 2,
                self.canvas.winfo_height() // 2,
                image=self.preview_img
            )
        except:
            pass

    def load_images(self):
        files = filedialog.askopenfilenames(initialdir=self.downloads)

        exts = (".png", ".jpg", ".jpeg", ".webp")
        self.images = [f for f in files if f.lower().endswith(exts)]

        if self.images:
            self.update_list()
            self.show_preview(self.images[0])

    def load_folder(self):
        folder = filedialog.askdirectory(initialdir=self.downloads)

        if folder:
            exts = (".png", ".jpg", ".jpeg", ".webp")

            self.images = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith(exts)
            ]

            if self.images:
                self.update_list()
                self.show_preview(self.images[0])

    def select_output(self):
        self.output = filedialog.askdirectory(initialdir=self.downloads)

    def run(self):
        if not self.images:
            self.status.configure(text="⚠️ No hay imágenes")
            return

        if not self.w.get() or not self.h.get():
            self.status.configure(text="⚠️ Tamaño inválido")
            return

        result = process_images(
            self.images,
            self.output,
            self.w.get(),
            self.h.get(),
            self.keep.get(),
            self.format.get(),
            self.rename_entry.get()
        )

        self.status.configure(text=result)

        # 🔥 RESET automático después de procesar
        self.root.after(2000, self.clear_all)