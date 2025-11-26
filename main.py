import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageGrab, ImageTk
import threading
import os
import ctypes

# Enable DPI Awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

# Import our modules
import ocr_engine
import translator
import image_utils

class ScreenShotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Translator")
        self.root.geometry("300x150")
        self.root.attributes("-topmost", True) # Keep window on top

        # UI Elements
        self.label = tk.Label(root, text="Screenshot Translator", font=("Arial", 14))
        self.label.pack(pady=10)

        self.btn_capture = tk.Button(root, text="Capture & Translate", command=self.start_capture, height=2, bg="#4CAF50", fg="white")
        self.btn_capture.pack(fill=tk.X, padx=20, pady=5)

        self.btn_open_folder = tk.Button(root, text="Open Output Folder", command=self.open_folder)
        self.btn_open_folder.pack(fill=tk.X, padx=20, pady=5)

        # Variables for selection
        self.start_x = None
        self.start_y = None
        self.cur_x = None
        self.cur_y = None
        self.rect = None
        self.top = None

    def start_capture(self):
        """Starts the screen capture process by creating a full-screen overlay."""
        self.root.withdraw() # Hide main window
        self.top = tk.Toplevel(self.root)
        self.top.attributes("-fullscreen", True)
        self.top.attributes("-alpha", 0.3) # Transparent
        self.top.configure(background='black')
        self.top.attributes("-topmost", True)

        self.canvas = tk.Canvas(self.top, cursor="cross", bg="grey11")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        # Escape to cancel
        self.top.bind("<Escape>", lambda e: self.cancel_capture())

    def cancel_capture(self):
        if self.top:
            self.top.destroy()
        self.root.deiconify()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=2)

    def on_move_press(self, event):
        self.cur_x, self.cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.cur_x, self.cur_y)

    def on_button_release(self, event):
        if self.start_x is None or self.start_y is None:
            return

        # Calculate coordinates
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        # Close overlay
        self.top.destroy()
        self.root.deiconify()

        # Check if selection is valid (not too small)
        if (x2 - x1) < 10 or (y2 - y1) < 10:
            return

        # Process in a separate thread to not freeze UI
        threading.Thread(target=self.process_screenshot, args=(x1, y1, x2, y2)).start()

    def process_screenshot(self, x1, y1, x2, y2):
        try:
            # Capture screen
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            
            # OCR
            print("Running OCR...")
            text = ocr_engine.extract_text(screenshot)
            print(f"Extracted Text: {text}")
            
            if not text or "Error" in text:
                print("No text found or error occurred.")
                text = ""
            
            # Translate using Gemini
            print("Translating...")
            translated_text = translator.translate_text(text)
            print(f"Translated: {translated_text}")
            
            # Save original screenshot (without overlay)
            filepath = image_utils.save_image(screenshot)
            print(f"Saved to {filepath}")
            
            # Copy translated text to clipboard (not the image)
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(translated_text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            print("Translated text copied to clipboard.")
            
        except Exception as e:
            print(f"Error processing screenshot: {e}")
            # messagebox.showerror("Error", str(e))

    def open_folder(self):
        output_dir = "captured_images"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        os.startfile(output_dir)

    @property
    def x(self):
        return self.start_x
    
    @property
    def y(self):
        return self.start_y

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenShotApp(root)
    root.mainloop()
