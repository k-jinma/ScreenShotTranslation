import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageGrab, ImageTk
import threading
import os
import ctypes
from datetime import datetime

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
        self.root.geometry("300x200")
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
        # Disable the capture button to prevent multiple clicks
        self.btn_capture.config(state=tk.DISABLED)
        
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
        # Re-enable the capture button
        self.btn_capture.config(state=tk.NORMAL)

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
            self.log_to_file("INFO", "Starting OCR...")
            text = ocr_engine.extract_text(screenshot)
            self.log_to_file("INFO", f"OCR completed. Text length: {len(text)}")
            self.log_to_file("DEBUG", f"Extracted Text: {text}")
            
            if not text:
                self.log_to_file("WARNING", "No text extracted from image")
                text = ""
            elif "Error" in text:
                self.log_to_file("ERROR", f"OCR error: {text}")
            
            # Translate using Gemini
            self.log_to_file("INFO", "Starting translation...")
            translated_text = translator.translate_text(text)
            self.log_to_file("INFO", f"Translation completed. Length: {len(translated_text)}")
            self.log_to_file("DEBUG", f"Translated: {translated_text}")
            
            # Save translation to log file
            self.save_translation_to_file(text, translated_text)
            
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
            
            # Show success dialog in main thread
            self.root.after(0, lambda: self.show_completion_dialog(True, translated_text, filepath))
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.log_to_file("ERROR", f"Error processing screenshot: {e}\n{error_details}")
            # Show error dialog in main thread
            self.root.after(0, lambda: self.show_completion_dialog(False, str(e), None))
    
    def show_completion_dialog(self, success, message, filepath):
        """Show completion dialog and re-enable the capture button."""
        # Re-enable the capture button
        self.btn_capture.config(state=tk.NORMAL)
        
        if success:
            messagebox.showinfo(
                "翻訳完了", 
                f"翻訳が完了しました!\n\n翻訳テキストがクリップボードにコピーされました。\n\n保存先: {filepath}"
            )
        else:
            # Show error with suggestion to check log file
            messagebox.showerror(
                "エラー", 
                f"処理中にエラーが発生しました:\n\n{message}\n\n詳細は captured_images\\app_log.txt をご確認ください。"
            )

    def log_to_file(self, level, message):
        """Write log message to error log file."""
        output_dir = "captured_images"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        error_log = os.path.join(output_dir, "app_log.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(error_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {level}: {message}\n")
    
    def save_translation_to_file(self, original_text, translated_text):
        """Save translation to a log file with timestamp."""
        output_dir = "captured_images"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        log_file = os.path.join(output_dir, "translation_log.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"[{timestamp}]\n")
            f.write(f"Original: {original_text}\n")
            f.write(f"Translation: {translated_text}\n")
            f.write("=" * 80 + "\n\n")
        
        self.log_to_file("INFO", f"Translation saved to {log_file}")
        
        # Open the log file in notepad
        os.startfile(log_file)
    
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
