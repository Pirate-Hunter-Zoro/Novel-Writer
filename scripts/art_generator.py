# scripts/art_generator.py

import argparse
import os
import glob
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel, Image
from dotenv import load_dotenv
import genai

# --- Configuration ---
load_dotenv()

# This is the new model that understands style references!
CUSTOMIZATION_MODEL = "imagen-3.0-capability-001"
TRAINING_IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'training_images')

def generate_styled_image(project_id, location, prompt, characters, output_path):
    """
    Generates an image using a prompt and character-specific style reference images.
    """
    print(f"🎨 Art Generator v4.0 (Style-Injection Edition) activated!")
    
    vertexai.init(project=project_id, location=location)
    model = ImageGenerationModel.from_pretrained(CUSTOMIZATION_MODEL)
    
    # --- Find Our Style Reference Images! ---
    reference_images = []
    print("  - Searching for character style references...")
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
                style_ref = genai.types.StyleReferenceImage(
                    reference_id=str(i), # Each image needs a unique ID
                    reference_image=ref_image_obj,
                    config=genai.types.StyleReferenceConfig(style_description=f"The art style for {full_char_name}")
                )
                reference_images.append(style_ref)
    
    if not reference_images:
        print("  - WARNING: No reference images found. Generating image without style injection.")

    try:
        print(f"  - Generating image with {len(reference_images)} style references...")
        
        # We use edit_image, but without a base image, it becomes a style-guided generation!
        response = model.edit_image(
            prompt=prompt,
            reference_images=reference_images,
            config=genai.types.EditImageConfig(
                number_of_images=1,
                seed=42 # Using a seed helps make results more repeatable!
            )
        )
        
        if response.generated_images:
            print("✅ Image generated successfully!")
            response.generated_images[0].save(location=output_path)
            print(f"🎉 SUCCESS! Image saved to: {output_path}")
        else:
            print("❌ ERROR: The model returned no images. The prompt may have been blocked.")

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