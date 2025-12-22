import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

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
    
    def refine_bounding_box(self, x1, y1, x2, y2, img_width, img_height, quadrant):
        """
        Refine bounding box coordinates to ensure they're valid and well-positioned
        """
        # Ensure coordinates are within image bounds
        x1 = max(0, min(x1, img_width - 1))
        y1 = max(0, min(y1, img_height - 1))
        x2 = max(x1 + 10, min(x2, img_width - 1))  # Ensure minimum width
        y2 = max(y1 + 10, min(y2, img_height - 1))  # Ensure minimum height
        
        # Ensure x2 > x1 and y2 > y1
        if x2 <= x1:
            x2 = x1 + 50
        if y2 <= y1:
            y2 = y1 + 50
        
        return [int(x1), int(y1), int(x2), int(y2)]
    
    def draw_bounding_boxes(self, image_path, bounding_boxes):
        """
        Draw bounding boxes on the image with yellow outline and red semi-transparent fill
        """
        img = Image.open(image_path).convert("RGB")
        img_width, img_height = img.size
        draw = ImageDraw.Draw(img, "RGBA")
        
        for bbox in bounding_boxes:
            coords = bbox["coordinates"]
            if len(coords) != 4:
                continue
                
            x1, y1, x2, y2 = coords
            quadrant = bbox.get("quadrant", "")
            
            # Refine coordinates
            x1, y1, x2, y2 = self.refine_bounding_box(x1, y1, x2, y2, img_width, img_height, quadrant)
            
            label = bbox.get("label", "Wisdom Tooth")
            
            # Draw semi-transparent red fill
            draw.rectangle([x1, y1, x2, y2], fill=(255, 0, 0, 100), outline=None)
            
            # Draw yellow outline
            draw.rectangle([x1, y1, x2, y2], outline=(255, 255, 0, 255), width=3)
            
            # Draw label above the box
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Position label above box, ensuring it's visible
            label_y = max(0, y1 - 25)
            draw.text((x1, label_y), label, fill=(255, 255, 0, 255), font=font)
        
        return img
    
    def detect_wisdom_teeth(self, image_path):
        """
        Use GPT-4 Vision to identify wisdom tooth areas in X-ray and return analysis with bounding boxes
        Returns: (analysis_text, annotated_image_path)
        """
        try:
            base64_image = self.encode_image(image_path)
            
            # Get image dimensions for coordinate reference
            img = Image.open(image_path)
            img_width, img_height = img.size
            
            response = self.client.chat.completions.create(
                model="gpt-4o",  # GPT-4 with vision
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert dental radiologist with years of experience analyzing dental X-rays. You can analyze X-ray images in detail and identify specific dental structures including wisdom teeth. Provide accurate, detailed analysis based on what you observe in the images. You MUST provide bounding box coordinates in pixel coordinates relative to the image dimensions."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""You are an expert dental radiologist analyzing a dental X-ray image.

IMAGE DIMENSIONS: Width={img_width}px, Height={img_height}px

TASK: Carefully examine this X-ray image and provide a detailed analysis of the wisdom teeth (third molars) with precise bounding box coordinates.

REQUIREMENTS:
1. Look at the image carefully and identify if wisdom teeth are present
2. For each detected wisdom tooth, provide PRECISE bounding box coordinates in pixels
3. Coordinates should be in format [x1, y1, x2, y2] where:
   - (x1, y1) is the top-left corner of the wisdom tooth (including crown and root)
   - (x2, y2) is the bottom-right corner of the wisdom tooth
   - The bounding box should tightly surround the ENTIRE wisdom tooth structure
   - Include a small margin (5-10 pixels) around the tooth for better visibility
   - All coordinates must be valid pixel positions within the image dimensions
4. BOUNDING BOX PRECISION:
   - The box should be centered on the wisdom tooth
   - For upper wisdom teeth: boxes should be in the upper portion of the image
   - For lower wisdom teeth: boxes should be in the lower portion of the image
   - For left wisdom teeth: boxes should be on the left side of the image
   - For right wisdom teeth: boxes should be on the right side of the image
   - The box should encompass the entire visible tooth structure (crown + visible root)
5. Determine their locations in the four quadrants: upper left, upper right, lower left, lower right
6. Describe what you see: Are they fully erupted, partially erupted, impacted, or absent?

OUTPUT FORMAT: Provide your analysis in JSON format:
{{
    "wisdom_teeth_detected": true/false,
    "bounding_boxes": [
        {{
            "quadrant": "upper_left/upper_right/lower_left/lower_right",
            "coordinates": [x1, y1, x2, y2],
            "label": "Wisdom Tooth (Upper Left)",
            "status": "erupted/partially_erupted/impacted",
            "confidence": 0.0-1.0
        }}
    ],
    "analysis": {{
        "upper_left": {{"present": true/false, "status": "...", "notes": "..."}},
        "upper_right": {{"present": true/false, "status": "...", "notes": "..."}},
        "lower_left": {{"present": true/false, "status": "...", "notes": "..."}},
        "lower_right": {{"present": true/false, "status": "...", "notes": "..."}}
    }},
    "overall_description": "Detailed description of what you observe",
    "recommendations": "Any observations or notes"
}}

CRITICAL: 
- You MUST provide bounding box coordinates for each detected wisdom tooth
- The coordinates must be valid pixel positions within the image dimensions (0 to width-1 for x, 0 to height-1 for y)
- The bounding boxes should be PRECISELY positioned to surround each wisdom tooth
- Look carefully at where the wisdom teeth are located in the X-ray and place the boxes directly over them
- Do not say you cannot provide coordinates - carefully observe the image and provide accurate pixel coordinates
- Double-check that your coordinates match the actual tooth positions in the image"""
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
                max_tokens=1500
            )
            
            analysis_text = response.choices[0].message.content
            
            # Try to parse JSON and draw bounding boxes
            try:
                analysis_json = json.loads(analysis_text)
                bounding_boxes = analysis_json.get("bounding_boxes", [])
                
                if bounding_boxes:
                    # Draw bounding boxes on the image
                    annotated_img = self.draw_bounding_boxes(image_path, bounding_boxes)
                    
                    # Save annotated image to a temp directory (not in sample_images)
                    # This prevents annotated images from appearing in the sample dropdown
                    image_path_obj = Path(image_path)
                    if "sample_images" in str(image_path_obj):
                        # If source is in sample_images, save to a temp folder
                        temp_dir = image_path_obj.parent.parent / "temp_annotations"
                        temp_dir.mkdir(exist_ok=True)
                        output_path = temp_dir / f"annotated_{image_path_obj.name}"
                    else:
                        # Otherwise save in same directory as source
                        output_path = image_path_obj.parent / f"annotated_{image_path_obj.name}"
                    annotated_img.save(output_path)
                    
                    return analysis_text, str(output_path)
                else:
                    return analysis_text, None
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from text
                try:
                    # Look for JSON in the response
                    start_idx = analysis_text.find('{')
                    end_idx = analysis_text.rfind('}') + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        json_str = analysis_text[start_idx:end_idx]
                        analysis_json = json.loads(json_str)
                        bounding_boxes = analysis_json.get("bounding_boxes", [])
                        
                        if bounding_boxes:
                            annotated_img = self.draw_bounding_boxes(image_path, bounding_boxes)
                            output_path = Path(image_path).parent / f"annotated_{Path(image_path).name}"
                            annotated_img.save(output_path)
                            return analysis_text, str(output_path)
                except:
                    pass
            
            return analysis_text, None
            
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