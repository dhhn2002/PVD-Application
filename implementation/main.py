import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
from steganography import Steganography

class PVDSteganographyGUI:
    def __init__(self, root):
        self.cover_image_path = None
        self.secret_text = ""
        self.embedded_image_path = None
        self.cover_image = None
        self.embedded_image = None
        
        # Store references to image containers
        self.cover_image_container = None
        self.output_image_container = None
        self.embedded_image_container = None

        self.steganography = Steganography()
        
        self.build_ui(root)

    def build_ui(self, root):
        root.title("IMAGE STEGANOGRAPHY USING PVD")
        root.geometry("920x720")
        root.minsize(920, 720)

        self.make_styles(root)

        # Title
        title = ttk.Label(
            root,
            text="IMAGE STEGANOGRAPHY USING PIXEL VALUE DIFFERENCING (PVD)",
            style="Title.TLabel",
            anchor="center",
            justify="center"
        )
        title.pack(pady=(12, 6))
        
        # Top section: Embedding
        embed_frame = ttk.LabelFrame(root, text="EMBEDDING SIDE", style="Section.TLabelframe")
        embed_frame.pack(fill="x", padx=10, pady=(4, 10))

        # Row 0: Buttons
        top_buttons = ttk.Frame(embed_frame)
        top_buttons.pack(fill="x", padx=10, pady=(10, 6))

        btn_cover = ttk.Button(top_buttons, text="Browse Cover Image", style="Big.TButton", command=self.browse_cover_image)
        btn_secret_file = ttk.Button(top_buttons, text="Browse Secret Text File", style="Big.TButton", command=self.browse_secret_text)
        btn_embedding = ttk.Button(top_buttons, text="Embedding", style="Big.TButton", command=self.embedding)

        btn_cover.pack(side="left", padx=(0, 10))
        btn_secret_file.pack(side="left", padx=(0, 10))
        btn_embedding.pack(side="right")

        # Row 1: Three columns (Input image | Secret text | Output image)
        mid_row = ttk.Frame(embed_frame)
        mid_row.pack(fill="x", padx=10, pady=(6, 0))

        # Column A: input image + caption
        col_a = ttk.Frame(mid_row)
        col_a.pack(side="left", expand=True, fill="x")

        # Create container for cover image
        self.cover_image_container = self.image_placeholder(col_a, text="Input Cover Image")
        self.cover_image_container.pack(padx=10, pady=(0, 4))

        cap_a = ttk.Label(col_a, text="Input Cover Image", style="Caption.TLabel", anchor="center")
        cap_a.pack(pady=(0, 6))

        # Column B: secret text box + caption
        col_b = ttk.Frame(mid_row)
        col_b.pack(side="left", expand=True, fill="x")

        txt_frame = ttk.Frame(col_b, style="Box.TFrame")
        txt_frame.pack(padx=10, pady=(0, 4), fill="x")

        self.secret_text_area = scrolledtext.ScrolledText(
            txt_frame,
            height=5,
            width=30,
            wrap="word",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 10),
            bg='white'
        )
        self.secret_text_area.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        cap_b = ttk.Label(col_b, text="Secret Text Message", style="Caption.TLabel", anchor="center")
        cap_b.pack(pady=(0, 6))

        # Column C: output image + caption
        col_c = ttk.Frame(mid_row)
        col_c.pack(side="left", expand=True, fill="x")

        # Create container for output image
        self.output_image_container = self.image_placeholder(col_c, text="Output Embed Image")
        self.output_image_container.pack(padx=10, pady=(0, 4))

        cap_c = ttk.Label(col_c, text="Output Embed Image", style="Caption.TLabel", anchor="center")
        cap_c.pack(pady=(0, 6))

        # Bottom section: Extraction
        extract_frame = ttk.LabelFrame(root, text="EXTRACTION SIDE", style="Section.TLabelframe")
        extract_frame.pack(fill="x", padx=10, pady=(6, 10))

        # Row 0: Buttons
        bot_buttons = ttk.Frame(extract_frame)
        bot_buttons.pack(fill="x", padx=10, pady=(10, 6))

        btn_browse_embed = ttk.Button(bot_buttons, text="Browse Embed Image", style="Wide.TButton", command=self.browse_embed_image)
        btn_extraction = ttk.Button(bot_buttons, text="Extraction", style="Wide.TButton", command=self.extraction)
        btn_reset = ttk.Button(bot_buttons, text="Reset", style="Wide.TButton", command=self.reset_all)

        btn_browse_embed.pack(side="left")
        btn_extraction.pack(side="left", padx=(10, 0))
        btn_reset.pack(side="left", padx=(10, 0))

        # Row 1: Two columns (Embedded image | Extracted text)
        bot_row = ttk.Frame(extract_frame)
        bot_row.pack(fill="x", padx=10, pady=(6, 12))

        # Column 1: embedded image
        col1 = ttk.Frame(bot_row)
        col1.pack(side="left", expand=True, fill="both")

        # Create container for embedded image
        self.embedded_image_container = self.image_placeholder(col1, text="Embedded Image")
        self.embedded_image_container.pack(padx=10, pady=(0, 4))

        cap1 = ttk.Label(col1, text="Embedded Image", style="Caption.TLabel", anchor="center")
        cap1.pack(pady=(0, 6))

        # Column 2: extracted text box
        col2 = ttk.Frame(bot_row)
        col2.pack(side="left", expand=True, fill="both")

        out_txt_frame = ttk.Frame(col2, style="Box.TFrame")
        out_txt_frame.pack(padx=10, pady=(0, 4), fill="x")
        self.extracted_text_area = tk.Text(out_txt_frame, height=6, wrap="word", borderwidth=0, highlightthickness=0, font=("Segoe UI", 10))
        self.extracted_text_area.pack(fill="both", expand=True, padx=4, pady=4)

        cap2 = ttk.Label(col2, text="Extracted Secret Message", style="Caption.TLabel", anchor="center")
        cap2.pack(pady=(0, 6))

    def reset_output_image_container(self):
        # Reset output image container when new cover image is selected or new secret text is entered/uploaded
        for widget in self.output_image_container.winfo_children():
            widget.destroy()
        self.create_placeholder_content(self.output_image_container, "Output Embed Image")

    def display_image_in_container(self, file_path, container, image_type):
        """Display image in the specified container, replacing the placeholder"""
        try:
            # Load and process the image
            image = Image.open(file_path)
            
            # Calculate dimensions to fit container while maintaining aspect ratio
            container_width = 220
            container_height = 180
            
            # Get image dimensions
            img_width, img_height = image.size
            
            # Calculate scaling factor to fit image in container
            scale_w = container_width / img_width
            scale_h = container_height / img_height
            scale = min(scale_w, scale_h)
            
            # Calculate new dimensions
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize image
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(resized_image)
            
            # Clear the container and add the image
            for widget in container.winfo_children():
                widget.destroy()
            
            # Create a label to display the image
            image_label = tk.Label(container, image=photo, bg="#f6f6f6", bd=0, highlightthickness=0)
            image_label.image = photo  # Keep a reference to prevent garbage collection
            image_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Store the original image
            if image_type == "cover":
                self.cover_image = image
            elif image_type == "embedded":
                self.embedded_image = image
                
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
            return False
    
    def browse_cover_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image files", "*.png *.jpg *.bmp")]
        )
        if file_path:
            self.cover_image_path = file_path
            if self.display_image_in_container(file_path, self.cover_image_container, "cover"):
                print(f"Cover image loaded: {file_path}")
                self.reset_output_image_container()

    def browse_secret_text(self):
        file_path = filedialog.askopenfilename(
            title="Select Secret Text File",
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.secret_text_area.delete("1.0", tk.END)
                    self.secret_text_area.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {str(e)}")

    def embedding(self):
        if not self.cover_image_path:
            messagebox.showerror("Error", "Please select a cover image first!")
            return
        
        secret_text = self.secret_text_area.get("1.0", tk.END).strip()
        if not secret_text:
            messagebox.showerror("Error", "Please enter secret text!")
            return
        
        try:
            embedded_image = self.steganography.embed_text(self.cover_image_path, secret_text) # embed text in image

            save_path = filedialog.asksaveasfilename(
                title="Save Embedded Image",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg")]
            )
            
            if save_path:
                self.steganography.save_image(embedded_image, save_path) # save stego image
                
                self.embedded_image_path = save_path
                self.display_image_in_container(save_path, self.output_image_container, "embedded")
                messagebox.showinfo("Success", f"Embedding successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Embedding failed: {str(e)}")

    def browse_embed_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Embedded Image",
            filetypes=[("Image files", "*.png *.jpg *.bmp")]
        )
        if file_path:
            self.embedded_image_path = file_path
            if self.display_image_in_container(file_path, self.embedded_image_container, "embedded"):
                # Reset text areas
                self.extracted_text_area.delete("1.0", tk.END)
                print(f"Embedded image loaded: {file_path}")

    def extraction(self):
        try:
            if self.steganography:
                image_path = self.embedded_image_path
                decoded_text = self.steganography.decode_text(image_path)
                self.extracted_text_area.insert("1.0", decoded_text)
        except Exception as e:
            messagebox.showerror("Error", f"Extraction failed: {str(e)}")

    def reset_all(self):
        """Reset all images and text to initial state"""
        # Reset image paths
        self.cover_image_path = None
        self.embedded_image_path = None
        self.cover_image = None
        self.embedded_image = None
        
        # Reset cover image container
        for widget in self.cover_image_container.winfo_children():
            widget.destroy()
        self.create_placeholder_content(self.cover_image_container, "Input Cover Image")
        
        # Reset output image container
        self.reset_output_image_container()

        # Reset embedded image container
        for widget in self.embedded_image_container.winfo_children():
            widget.destroy()
        self.create_placeholder_content(self.embedded_image_container, "Embedded Image")

        # Reset text areas
        self.secret_text_area.delete("1.0", tk.END)
        self.extracted_text_area.delete("1.0", tk.END)
        
        print("All data reset")

    def create_placeholder_content(self, container, text):
        """Create placeholder content for image container"""
        width = 220
        height = 180
        canvas = tk.Canvas(container, width=width-2, height=height-2, highlightthickness=0, bg="#f6f6f6", bd=0)
        canvas.place(relx=0.5, rely=0.5, anchor="center")
        canvas.create_rectangle(2, 2, width-6, height-6, outline="#d0d0d0")
        canvas.create_line(10, 10, width-16, height-16, fill="#d0d0d0")
        canvas.create_line(10, height-16, width-16, 10, fill="#d0d0d0")
        canvas.create_text(width/2, height/2, text=text, fill="#999999", font=("Segoe UI", 9))
    
    # ---------------------------
    # helper styles
    # ---------------------------
    def make_styles(self, root):
        style = ttk.Style(root)
        # use default theme to keep it portable across platforms
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
        style.configure("Img.TFrame", borderwidth=0, relief="flat")

    # ---------------------------
    # image placeholder factory
    # ---------------------------
    def image_placeholder(self, parent, width=220, height=180, text="Image Placeholder"):
        outer = ttk.Frame(parent, style="Img.TFrame")
        outer.grid_propagate(False)
        outer.configure(width=width, height=height)
        
        # Create initial placeholder content
        self.create_placeholder_content(outer, text)
        
        return outer

def main():
    root = tk.Tk()
    app = PVDSteganographyGUI(root)

    # ---- Center the window on screen ----
    root.update_idletasks()  # tính toán kích thước thực của window sau khi build UI
    w = root.winfo_width()
    h = root.winfo_height()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw // 2) - (w // 2)
    y = (sh // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")
    # --------------------------------------

    root.mainloop()

if __name__ == "__main__":
    main()