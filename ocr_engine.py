import easyocr
from PIL import Image
import numpy as np

# Initialize reader (lazy loading)
_reader = None

def get_reader():
    """Get or create the EasyOCR reader instance."""
    global _reader
    if _reader is None:
        # Initialize with English only for better accuracy
        # gpu=False to avoid CUDA requirements
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader

def extract_text(image: Image.Image, lang='ja') -> str:
    """
    Extracts text from the given PIL Image using EasyOCR.
    
    Args:
        image: PIL Image object.
        lang: Language code (default: 'ja'). Not used with EasyOCR as it's set at initialization.
        
    Returns:
        Extracted text as a string.
    """
    try:
        # Convert PIL Image to numpy array
        img_array = np.array(image)
        
        # Get reader
        reader = get_reader()
        
        # Perform OCR
        # readtext returns list of (bbox, text, confidence)
        results = reader.readtext(img_array)
        
        # Extract just the text
        text_lines = [result[1] for result in results]
        
        return '\n'.join(text_lines)
        
    except Exception as e:
        return f"Error during OCR: {e}"
