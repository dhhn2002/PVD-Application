import tkinter as tk
from tkinter import ttk
from helpers import image_placeholder

def build_extraction_side(root):
    extract_frame = ttk.LabelFrame(root, text="EXTRACTION SIDE", style="Section.TLabelframe")
    extract_frame.pack(fill="x", padx=10, pady=(6, 10))

    # Row 0: Buttons
    bot_buttons = ttk.Frame(extract_frame)
    bot_buttons.pack(fill="x", padx=10, pady=(10, 6))

    btn_browse_embed = ttk.Button(bot_buttons, text="Browse Embed Image", style="Wide.TButton")
    btn_extraction = ttk.Button(bot_buttons, text="Extraction", style="Wide.TButton")
    btn_reset = ttk.Button(bot_buttons, text="Reset", style="Wide.TButton")

    btn_browse_embed.pack(side="left")
    btn_extraction.pack(side="left", padx=(10, 0))
    btn_reset.pack(side="left", padx=(10, 0))

    # Row 1: Two columns (Embedded image | Extracted text)
    bot_row = ttk.Frame(extract_frame)
    bot_row.pack(fill="x", padx=10, pady=(6, 12))

    # Column 1: embedded image
    col1 = ttk.Frame(bot_row)
    col1.pack(side="left", expand=True, fill="both")

    img_embedded = image_placeholder(col1, text="Embedded Image")
    img_embedded.pack(padx=10, pady=(0, 4))
    ttk.Label(col1, text="Embedded Image", style="Caption.TLabel").pack(pady=(0, 6))

    # Column 2: extracted text
    col2 = ttk.Frame(bot_row)
    col2.pack(side="left", expand=True, fill="both")

    out_txt_frame = ttk.Frame(col2, style="Box.TFrame")
    out_txt_frame.pack(padx=10, pady=(0, 4), fill="x")
    out_txt = tk.Text(out_txt_frame, height=6, wrap="word", borderwidth=0, highlightthickness=0, font=("Segoe UI", 10))
    out_txt.insert("1.0", "This is another Secret Message")
    out_txt.pack(fill="both", expand=True, padx=4, pady=4)
    ttk.Label(col2, text="Extracted Secret Message", style="Caption.TLabel").pack(pady=(0, 6))
