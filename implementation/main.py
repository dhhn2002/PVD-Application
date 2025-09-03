import tkinter as tk
from tkinter import ttk
from helpers import make_styles
from ui.embedding_side import build_embedding_side
from ui.extraction_side import build_extraction_side

def build_ui(root):
    root.title("IMAGE STEGANOGRAPHY USING PVD")
    root.geometry("920x700")
    root.minsize(920, 700)

    make_styles(root)

    # Title
    title = ttk.Label(
        root,
        text="IMAGE STEGANOGRAPHY USING PIXEL VALUE DIFFERENCING (PVD)",
        style="Title.TLabel",
        anchor="center",
        justify="center"
    )
    title.pack(pady=(12, 6))

    # Embedding
    build_embedding_side(root)

    # Extraction
    build_extraction_side(root)

if __name__ == "__main__":
    root = tk.Tk()
    build_ui(root)
    root.mainloop()
