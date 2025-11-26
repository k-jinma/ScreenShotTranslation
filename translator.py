import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: GEMINI_API_KEY not found in .env file")

# Initialize model
model = genai.GenerativeModel('gemini-2.5-flash')

def translate_text(text: str, source='auto', target='ja') -> str:
    """
    Translates text to Japanese using Google Gemini API.
    
    Args:
        text: Text to translate.
        source: Source language code (not used with Gemini, kept for compatibility).
        target: Target language code (default: 'ja').
        
    Returns:
        Translated text.
    """
    if not text or not text.strip():
        return ""
    
    if not api_key:
        return "Error: Gemini API key not configured"
        
    try:
        # Create a prompt for natural, fluent translation
        prompt = f"""あなたは優秀な翻訳者です。以下の英文を、自然で流暢な日本語に翻訳してください。

翻訳の際の注意事項：
- 文脈を十分に理解し、意訳も含めて最も自然な日本語表現を使用する
- 技術用語や専門用語は適切に訳す
- 長文は適切に段落分けし、読みやすくする
- 直訳ではなく、日本語として自然な文章構造にする
- 翻訳結果のみを出力し、説明や注釈は一切付けない

英文:
{text}

日本語訳:"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        # Fallback to basic translator if Gemini fails
        print(f"Gemini API error: {e}")
        try:
            from deep_translator import GoogleTranslator
            translator = GoogleTranslator(source='auto', target=target)
            return translator.translate(text)
        except Exception as fallback_error:
            return f"Translation error: {fallback_error}"
