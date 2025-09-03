import tkinter as tk
from tkinter import ttk

def make_styles(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground="#0046ff", background=root.cget("bg"))
    style.configure("Section.TLabelframe.Label", font=("Segoe UI", 11, "bold"))
    style.configure("Caption.TLabel", font=("Segoe UI", 9, "bold"))
    style.configure("Footer.TLabel", font=("Segoe UI", 10, "bold"), foreground="#cc0000")
    style.configure("Big.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 6))
    style.configure("Wide.TButton", font=("Segoe UI", 10, "bold"), padding=(10, 6))
    style.configure("Box.TFrame", borderwidth=1, relief="solid")
    style.configure("Img.TFrame", borderwidth=1, relief="solid")

def image_placeholder(parent, width=220, height=180, text="Image Placeholder"):
    outer = ttk.Frame(parent, style="Img.TFrame")
    outer.grid_propagate(False)
    outer.configure(width=width, height=height)

    canvas = tk.Canvas(outer, width=width-2, height=height-2, highlightthickness=0, bg="#f6f6f6")
    canvas.place(relx=0.5, rely=0.5, anchor="center")
    canvas.create_rectangle(2, 2, width-6, height-6, outline="#d0d0d0")
    canvas.create_line(10, 10, width-16, height-16, fill="#d0d0d0")
    canvas.create_line(10, height-16, width-16, 10, fill="#d0d0d0")
    canvas.create_text(width/2, height/2, text=text, fill="#999999", font=("Segoe UI", 9))
    return outer
