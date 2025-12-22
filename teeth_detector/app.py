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
    sample_images = list(sample_dir.glob("*.jpg")) + list(sample_dir.glob("*.png"))
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

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input X-ray")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an X-ray image...",
        type=["jpg", "jpeg", "png"],
        help="Upload a dental X-ray image"
    )
    
    # Handle sample selection
    if selected_sample != "Upload your own...":
        image_path = sample_dir / selected_sample
        image = Image.open(image_path)
        st.image(image, caption=selected_sample, use_column_width=True)
    elif uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded X-ray", use_column_width=True)
        # Save temporarily
        image_path = Path("temp_upload.jpg")
        image.save(image_path)
    else:
        st.info("👆 Upload an image or select a sample from the sidebar")
        st.stop()

with col2:
    st.subheader("Analysis Results")
    
    if st.button("🔍 Analyze X-ray", type="primary", use_container_width=True):
        with st.spinner("Analyzing X-ray with AI vision model..."):
            # Call API
            result = vision_api.detect_wisdom_teeth(str(image_path))
            
            # Check if result is an error message
            if result.startswith("⚠️") or result.startswith("❌") or result.startswith("🔑") or result.startswith("🌐"):
                st.error(result)
            else:
                st.markdown("### AI Analysis")
                st.markdown(result)
                
                # Try to parse as JSON if possible
                try:
                    result_json = json.loads(result)
                    st.json(result_json)
                except:
                    pass  # If not JSON, just show the markdown above
                
                st.success("✓ Analysis complete!")

# Footer
st.markdown("---")
st.markdown("""
**About:** This tool uses GPT-4 Vision to identify wisdom tooth regions in dental X-rays.  
**Note:** This is a demonstration project and should not be used for actual medical diagnosis.
""")