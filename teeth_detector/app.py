import streamlit as st
from pathlib import Path
from vision_api import VisionAPI
from PIL import Image
import json

# Page configuration
st.set_page_config(
    page_title="Teeth X-ray Wisdom Tooth Detector",
    page_icon="🦷",
    layout="wide"
)

# Title
st.title("🦷 Teeth X-ray Wisdom Tooth Detector")
st.markdown("Upload a dental X-ray to detect wisdom tooth areas using AI vision models")

# Initialize API
# Note: If you update your .env file, you need to restart Streamlit
# or clear the cache (⋮ menu > Clear cache) for changes to take effect
@st.cache_resource
def load_api():
    return VisionAPI()

try:
    vision_api = load_api()
    st.success("✓ Vision API loaded successfully")
except Exception as e:
    st.error(f"Error loading API: {e}")
    st.stop()

# Sidebar for sample images
st.sidebar.header("Sample Images")
# Get the directory where this script is located
script_dir = Path(__file__).parent
sample_dir = script_dir / "sample_images"

if sample_dir.exists():
    # Get all images but exclude annotated images
    all_images = list(sample_dir.glob("*.jpg")) + list(sample_dir.glob("*.png"))
    sample_images = [img for img in all_images if not img.name.startswith("annotated_")]
    if sample_images:
        selected_sample = st.sidebar.selectbox(
            "Choose a sample X-ray:",
            ["Upload your own..."] + [img.name for img in sample_images]
        )
    else:
        st.sidebar.info("No sample images found. Add images to sample_images/ folder")
        selected_sample = "Upload your own..."
else:
    selected_sample = "Upload your own..."

# File uploader and sample selection
uploaded_file = st.file_uploader(
    "Choose an X-ray image...",
    type=["jpg", "jpeg", "png"],
    help="Upload a dental X-ray image"
)

# Handle sample selection
if selected_sample != "Upload your own...":
    image_path = sample_dir / selected_sample
    image = Image.open(image_path)
elif uploaded_file:
    image = Image.open(uploaded_file)
    # Save temporarily
    image_path = Path("temp_upload.jpg")
    image.save(image_path)
else:
    st.info("👆 Upload an image or select a sample from the sidebar")
    st.stop()

# Show input image before analysis
col1, col2 = st.columns(2)
with col1:
    st.subheader("Input")
    st.image(image, caption="Original X-ray", use_column_width=True)
with col2:
    st.subheader("Output")
    if st.button("🔍 Analyze X-ray", type="primary", use_container_width=True, key="analyze_btn"):
        with st.spinner("Analyzing X-ray with AI vision model..."):
            # Call API
            result = vision_api.detect_wisdom_teeth(str(image_path))
            
            # Check if result is a tuple (analysis_text, annotated_image_path)
            if isinstance(result, tuple):
                analysis_text, annotated_image_path = result
            else:
                # Old format - just text
                analysis_text = result
                annotated_image_path = None
            
            # Check if result is an error message
            if analysis_text.startswith("⚠️") or analysis_text.startswith("❌") or analysis_text.startswith("🔑") or analysis_text.startswith("🌐"):
                st.error(analysis_text)
            else:
                # Display annotated image
                if annotated_image_path and Path(annotated_image_path).exists():
                    annotated_img = Image.open(annotated_image_path)
                    st.image(annotated_img, caption="X-ray with Wisdom Tooth Detection", use_column_width=True)
                else:
                    st.image(image, caption="No wisdom teeth detected", use_column_width=True)
                
                # Analysis details
                st.markdown("---")
                st.markdown("### AI Analysis")
                st.markdown(analysis_text)
                
                # Try to parse as JSON if possible
                try:
                    # Extract JSON from text if it's embedded
                    json_start = analysis_text.find('{')
                    json_end = analysis_text.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        json_str = analysis_text[json_start:json_end]
                        result_json = json.loads(json_str)
                        with st.expander("View Structured Analysis Data"):
                            st.json(result_json)
                except:
                    pass  # If not JSON, just show the markdown above
                
                st.success("✓ Analysis complete!")
    else:
        st.info("Click 'Analyze X-ray' to see results")

# Footer
st.markdown("---")
st.markdown("""
**About:** This tool uses GPT-4 Vision to identify wisdom tooth regions in dental X-rays.  
**Note:** This is a demonstration project and should not be used for actual medical diagnosis.
""")