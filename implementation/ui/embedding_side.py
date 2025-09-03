import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from helpers import image_placeholder
from PIL import Image, ImageTk

def load_and_display_image(self, file_path, label_widget, image_type):
    try:
        # Load image
        image = Image.open(file_path)
        
        # Resize image to fit the frame
        frame_width = 250
        frame_height = 200
        image.thumbnail((frame_width, frame_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(image)
        
        # Update label
        label_widget.configure(image=photo, text="")
        label_widget.image = photo  # Keep a reference
        
        # Store the original image
        if image_type == "cover":
            self.cover_image = Image.open(file_path)
        elif image_type == "embedded":
            self.embedded_image = Image.open(file_path)
            
    except Exception as e:
        messagebox.showerror("Error", f"Could not load image: {str(e)}")

def browse_cover_image(self):
    file_path = filedialog.askopenfilename(
        title="Select Cover Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if file_path:
        self.cover_image_path = file_path
        self.load_and_display_image(file_path, self.cover_image_label, "cover")

# def browse_cover_image(self):
#     try:
#         file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.bmp)") # filter file directory by image files
#         if file_path:
#             self.image_path.setText(file_path) # set image path in input field
#             pixmap = QPixmap(file_path) # create pixmap from image
#             self.original_scene.addPixmap(pixmap) # add pixmap to scene
#     except Exception as e:
#         self._show_error_message(f"Error browsing image: {e}.\nMake sure the file is an image.")

def build_embedding_side(root):
    embed_frame = ttk.LabelFrame(root, text="EMBEDDING SIDE", style="Section.TLabelframe")
    embed_frame.pack(fill="x", padx=10, pady=(4, 10))

    # Row 0: Buttons
    top_buttons = ttk.Frame(embed_frame)
    top_buttons.pack(fill="x", padx=10, pady=(10, 6))

    btn_cover = ttk.Button(top_buttons, text="Browse Cover Image", style="Big.TButton", command=self.browse_cover_image)
    btn_secret_file = ttk.Button(top_buttons, text="Browse Secret Text File", style="Big.TButton")
    btn_embedding = ttk.Button(top_buttons, text="Embedding", style="Big.TButton")

    btn_cover.pack(side="left", padx=(0, 10))
    btn_secret_file.pack(side="left", padx=(0, 10))
    btn_embedding.pack(side="right")

    # Row 1: Three columns (Input image | Secret text | Output image)
    mid_row = ttk.Frame(embed_frame)
    mid_row.pack(fill="x", padx=10, pady=(6, 0))

    # Column A: input image
    col_a = ttk.Frame(mid_row)
    col_a.pack(side="left", expand=True, fill="x")

    img_in = image_placeholder(col_a, text="Input Cover Image")
    img_in.pack(padx=10, pady=(0, 4))
    ttk.Label(col_a, text="Input Cover Image", style="Caption.TLabel").pack(pady=(0, 6))

    # Column B: secret text
    col_b = ttk.Frame(mid_row)
    col_b.pack(side="left", expand=True, fill="x")

    txt_frame = ttk.Frame(col_b, style="Box.TFrame")
    txt_frame.pack(padx=10, pady=(0, 4), fill="x")
    txt = tk.Text(txt_frame, height=8, wrap="word", borderwidth=0, highlightthickness=0, font=("Segoe UI", 10))
    txt.insert("1.0", "This is another Secret Message")
    txt.pack(fill="both", expand=True, padx=4, pady=4)
    ttk.Label(col_b, text="Secret Text Message", style="Caption.TLabel").pack(pady=(0, 6))

    # Column C: output image
    col_c = ttk.Frame(mid_row)
    col_c.pack(side="left", expand=True, fill="x")

    img_out = image_placeholder(col_c, text="Output Embed Image")
    img_out.pack(padx=10, pady=(0, 4))
    ttk.Label(col_c, text="Output Embed Image", style="Caption.TLabel").pack(pady=(0, 6))
