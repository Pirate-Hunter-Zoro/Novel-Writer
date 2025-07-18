# image_generator.py (v11.0 - THE TRUE PATH)
# This version is built from the official Google schematics.
# It uses the correct library, the correct class, and the correct methods.
# This is the one.

import os
import argparse
from datetime import datetime
from dotenv import load_dotenv

# !!! THE TRUE IMPORTS !!!
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# --- INITIALIZATION & ENVIRONMENT SETUP ---
load_dotenv()

# --- CONFIGURATION ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1") 

# --- PATHING ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "generated_images")

# --- THE TRUE BOT FUNCTION ---

def generate_image_from_prompt(
    image_prompt: str,
    chapter_number: int,
    part_number: int
) -> str:
    """
    Takes a detailed image prompt and generates a real image file using
    the official Vertex AI Imagen model process.
    """
    print("--- Image Crafter Bot: Walking THE TRUE PATH v11.0 ---")

    if not GCP_PROJECT_ID:
        raise ValueError("ERROR: GCP_PROJECT_ID not found. Please set it in your .env file.")

    # Initialize the Vertex AI client
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)

    # We call the model from the correct class, as shown in the official schematics.
    # "imagegeneration@006" is a powerful, stable version.
    model = ImageGenerationModel.from_pretrained("imagegeneration@006")

    print(f"Sending detailed prompt to the true 'imagegeneration@006' Vertex AI matrix...")
    
    try:
        # --- THIS IS THE OFFICIAL, DOCUMENTED METHOD ---
        response = model.generate_images(
            prompt=image_prompt,
            number_of_images=1,
        )

        # The image data is stored in the ._image_bytes attribute.
        image_bytes = response.images[0]._image_bytes
        print("...Image data successfully received from the Vertex AI matrix!")

    except Exception as e:
        print(f"--- !!! CRITICAL IMAGE GENERATION FAILURE !!! ---")
        print(f"Failed to generate image from Vertex AI. Details: {e}")
        raise

    # Create a unique, descriptive filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_filename = f"chapter_{chapter_number:02d}_part_{part_number:02d}_{timestamp}.png"
    image_filepath = os.path.join(OUTPUT_DIR, image_filename)

    # --- REAL IMAGE SAVING ---
    print(f"Saving REAL image to: {image_filename}")
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(image_filepath, "wb") as f:
            f.write(image_bytes)
        print("--- Image Crafter Bot: Creation complete! ---")
    except Exception as e:
        print(f"--- !!! CRITICAL IMAGE SAVING FAILURE !!! ---")
        print(f"Failed to save image data to file. Details: {e}")
        raise
    
    return image_filepath


# --- TESTING BLOCK ---
def main():
    """A simple function to test the Image Crafter bot."""
    print("--- Running Image Crafter Bot Test Sequence (THE FINAL PATH) ---")

    sample_prompt = "A cinematic, hyper-detailed digital painting of a team of heroes in a desolate desert. The focus is on two sisters in the foreground. One is defiant, with a glowing prosthetic arm. The other is weary, holding a large scythe. The style is gritty, textured concept art."

    print("\n--- USING THE FOLLOWING IMAGE PROMPT ---")
    print(sample_prompt)
    print("------------------------------------")

    generated_image_path = generate_image_from_prompt(
        image_prompt=sample_prompt,
        chapter_number=99,
        part_number=12 # The final final number.
    )

    print("\n--- LIVE IMAGE GENERATION COMPLETE ---")
    print(f"A REAL image has been generated and saved to:")
    print(generated_image_path)

    print("\n--- Image Crafter Bot Test Sequence Complete! ---")


if __name__ == '__main__':
    main()