import requests
import os
from pathlib import Path

def download_sample_images():
    """Download a few sample teeth X-ray images for testing"""
    
    # Create directory if it doesn't exist
    output_dir = Path("teeth_detector/sample_images")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Downloading sample X-ray images...")
    
    # We'll use the Hugging Face dataset API
    # For now, create placeholder instructions
    print("""
    To download sample images:
    1. Visit: https://huggingface.co/datasets/RayanAi/Main_teeth_dataset
    2. Click 'Files and versions' tab
    3. Download 5-10 sample .jpg or .png files
    4. Save them to: teeth_detector/sample_images/
    
    Or use the Hugging Face CLI:
    pip install huggingface-hub
    """)
    
    # Create a README in the folder
    readme_path = output_dir / "README.md"
    with open(readme_path, "w") as f:
        f.write("""# Sample Images Directory

Place 5-10 teeth X-ray images here for testing.

Download from: https://huggingface.co/datasets/RayanAi/Main_teeth_dataset
""")
    
    print(f"✓ Created directory: {output_dir}")
    print(f"✓ Created README with instructions")

if __name__ == "__main__":
    download_sample_images()