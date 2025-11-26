from PIL import Image, ImageDraw, ImageFont
import os
import datetime
import io
import win32clipboard

def save_image(image: Image.Image, output_dir="captured_images"):
    """Saves the image to a directory with a timestamp."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)
    image.save(filepath)
    return filepath

def copy_to_clipboard(image: Image.Image):
    """Copies the PIL Image to the Windows clipboard."""
    output = io.BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def draw_text_overlay(image: Image.Image, text: str) -> Image.Image:
    """
    Draws text over the image.
    This is a simple implementation that adds a semi-transparent background
    and draws text on top.
    """
    # Create a copy to draw on
    img_copy = image.copy().convert("RGBA")
    overlay = Image.new("RGBA", img_copy.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Simple logic: Draw a text box at the top or bottom
    # For better UX, we might want to try to position it near the original text,
    # but for now, let's put it in a readable box.
    
    # Font settings (default font might be small/ugly, try to load a system font)
    try:
        # Try to load a Japanese font (MS Gothic or Meiryo)
        font = ImageFont.truetype("msgothic.ttc", 20)
    except IOError:
        try:
            font = ImageFont.truetype("meiryo.ttc", 20)
        except IOError:
            font = ImageFont.load_default()
        
    # Calculate text size (approximate if using default font)
    # text_bbox = draw.textbbox((0, 0), text, font=font) # Pillow >= 8.0.0
    # width = text_bbox[2] - text_bbox[0]
    # height = text_bbox[3] - text_bbox[1]
    
    # Draw a semi-transparent black rectangle at the bottom
    w, h = img_copy.size
    # Estimate height needed for text
    lines = text.split('\n')
    text_height = len(lines) * 25 + 10
    
    rect_y = max(0, h - text_height)
    draw.rectangle([(0, rect_y), (w, h)], fill=(0, 0, 0, 180))
    
    # Draw text
    y = rect_y + 5
    for line in lines:
        draw.text((10, y), line, font=font, fill=(255, 255, 255, 255))
        y += 25
        
    # Composite
    return Image.alpha_composite(img_copy, overlay)
