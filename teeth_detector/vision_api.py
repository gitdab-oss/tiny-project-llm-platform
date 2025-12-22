import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
from pathlib import Path

# Try to import specific error classes (available in newer versions)
try:
    from openai import APIError, RateLimitError, APIConnectionError
except ImportError:
    # Fallback for older versions - use base Exception
    APIError = Exception
    RateLimitError = Exception
    APIConnectionError = Exception

# Load environment variables
# Try to load from project root (parent of teeth_detector folder)
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    # Fallback to default behavior (current directory)
    load_dotenv()

class VisionAPI:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables.\n"
                f"Checked .env file at: {env_path}\n"
                "Please ensure your .env file exists in the project root with: OPENAI_API_KEY=your_key"
            )
        # Show first 7 chars of key for debugging (e.g., "sk-proj...")
        key_preview = api_key[:7] + "..." if len(api_key) > 7 else "***"
        print(f"Initializing OpenAI client with API key: {key_preview}")
        self.client = OpenAI(api_key=api_key)
    
    def encode_image(self, image_path):
        """Convert image to base64 for API"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def detect_wisdom_teeth(self, image_path):
        """
        Use GPT-4 Vision to identify wisdom tooth areas in X-ray
        """
        try:
            base64_image = self.encode_image(image_path)
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # GPT-4 with vision
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """You are a dental X-ray analysis assistant. 
                                Analyze this dental X-ray image and identify the wisdom teeth (third molars) regions.
                                Provide the approximate locations as bounding box coordinates if visible.
                                Format: {"wisdom_teeth_detected": true/false, "locations": ["upper_left", "upper_right", "lower_left", "lower_right"], "description": "..."}"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Check if it's a rate limit/quota error (429)
            error_str = str(e).lower()
            if '429' in error_str or 'quota' in error_str or 'insufficient_quota' in error_str or 'rate limit' in error_str:
                error_msg = (
                    "⚠️ **API Quota Exceeded**\n\n"
                    "You've exceeded your OpenAI API quota. This means:\n"
                    "• You've used up your available credits\n"
                    "• Your billing limit has been reached\n\n"
                    "**To fix this:**\n"
                    "1. Check your usage at: https://platform.openai.com/usage\n"
                    "2. Add payment method or increase limits at: https://platform.openai.com/account/billing\n"
                    "3. Wait for your quota to reset (if on a free tier)\n\n"
                    f"Technical details: {str(e)}"
                )
                return error_msg
            
            # Check if it's an authentication error (401)
            if '401' in error_str or 'unauthorized' in error_str or 'invalid api key' in error_str:
                error_msg = (
                    "🔑 **Authentication Error**\n\n"
                    "Your API key is invalid or expired. Please:\n"
                    "• Check your API key in the .env file\n"
                    "• Get a new key from: https://platform.openai.com/api-keys\n"
                    "• Make sure OPENAI_API_KEY is set correctly\n"
                )
                return error_msg
            
            # Check if it's a connection error
            if 'connection' in error_str or 'network' in error_str or 'timeout' in error_str:
                error_msg = (
                    "🌐 **Connection Error**\n\n"
                    "Could not connect to the OpenAI API. Please:\n"
                    "• Check your internet connection\n"
                    "• Verify OpenAI service status: https://status.openai.com/\n"
                    "• Try again in a few moments\n\n"
                    f"Error: {str(e)}"
                )
                return error_msg
            
            # Generic API error
            if 'error code' in error_str or 'api' in error_str:
                # Try to extract error code
                error_code = 'Unknown'
                if '429' in error_str:
                    error_code = '429'
                elif '401' in error_str:
                    error_code = '401'
                elif '500' in error_str:
                    error_code = '500'
                
                error_msg = (
                    f"❌ **API Error** (Code: {error_code})\n\n"
                    f"An error occurred while calling the OpenAI API.\n\n"
                    f"Error details: {str(e)}\n\n"
                    "Check the OpenAI status page: https://status.openai.com/"
                )
                return error_msg
            
            # Fallback for any other error
            error_msg = (
                f"❌ **Unexpected Error**\n\n"
                f"An unexpected error occurred: {str(e)}\n\n"
                "Please check your image file and try again."
            )
            return error_msg

# Test function
if __name__ == "__main__":
    api = VisionAPI()
    print("Vision API initialized successfully!")