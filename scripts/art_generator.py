# scripts/art_generator.py

import argparse
import os
import glob
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel, Image
# --- THE FIX! ---
# We need to import the special "types" tools from the RIGHT toolbox!
from google.cloud.aiplatform_v1.types.content import SafetySetting, HarmCategory
from google.generativeai.types import HarmBlockThreshold, HarmSeverity
# And the reference image tools are in here!
from vertexai.preview.vision_models import (
    StyleReferenceImage,
    StyleReferenceConfig,
    EditImageConfig,
)
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()

# This is the new model that understands style references!
CUSTOMIZATION_MODEL = "imagen-3.0-capability-001"
# --- THE OTHER FIX! ---
# We'll build a super-robust, absolute path to the training images!
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
TRAINING_IMAGES_DIR = os.path.join(PROJECT_ROOT, 'training_images')


def generate_styled_image(project_id, location, prompt, characters, output_path):
    """
    Generates an image using a prompt and character-specific style reference images.
    """
    print(f"🎨 Art Generator v4.1 (GPS & Correct Toolbox Edition) activated!")
    
    vertexai.init(project=project_id, location=location)
    model = ImageGenerationModel.from_pretrained(CUSTOMIZATION_MODEL)
    
    # --- Find Our Style Reference Images! ---
    reference_images = []
    print(f"  - Searching for character style references in: {TRAINING_IMAGES_DIR}")
    for i, full_char_name in enumerate(characters):
        first_name = full_char_name.split()[0]
        char_folder = os.path.join(TRAINING_IMAGES_DIR, first_name)
        
        if os.path.isdir(char_folder):
            found_images = glob.glob(os.path.join(char_folder, '*.jpg')) + glob.glob(os.path.join(char_folder, '*.png'))
            if found_images:
                ref_path = found_images[0]
                print(f"    - Found style reference for {full_char_name}: {os.path.basename(ref_path)}")
                # This is how we tell the bot to use a picture as a style guide!
                ref_image_obj = Image.load_from_file(ref_path)
                # Now we're using the RIGHT tool from the RIGHT toolbox!
                style_ref = StyleReferenceImage(
                    reference_id=str(i), # Each image needs a unique ID
                    reference_image=ref_image_obj,
                    config=StyleReferenceConfig(style_description=f"The art style for {full_char_name}")
                )
                reference_images.append(style_ref)
            else:
                print(f"    - WARNING: No image files found in {char_folder} for {first_name}.")
    
    if not reference_images:
        print("  - WARNING: No reference images found for ANY characters. Generating image without style injection.")

    try:
        print(f"  - Generating image with {len(reference_images)} style references...")
        
        # We use edit_image, but without a base image, it becomes a style-guided generation!
        response = model.edit_image(
            prompt=prompt,
            reference_images=reference_images,
            config=EditImageConfig(
                number_of_images=1,
                seed=42 # Using a seed helps make results more repeatable!
            )
        )
        
        if response.generated_images:
            print("✅ Image generated successfully!")
            response.generated_images[0].save(location=output_path)
            print(f"🎉 SUCCESS! Image saved to: {output_path}")
        else:
            print("❌ ERROR: The model returned no images. The prompt was likely blocked.")

    except Exception as e:
        print(f"💥 DANGER! A critical meltdown occurred in the Art Generator's core!")
        print(f"Error details: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a styled image using reference images.")
    parser.add_argument("--prompt", required=True, help="The text prompt for the image.")
    parser.add_argument("--characters", nargs='+', required=True, help="List of character names for style reference.")
    parser.add_argument("--output-path", required=True, help="The file path to save the generated PNG image.")
    args = parser.parse_args()

    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

    generate_styled_image(project_id, location, args.prompt, args.characters, args.output_path)