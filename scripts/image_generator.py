# image_generator.py (v12.1 - The Multimodal Artisan - REWIRED!)
# This bot uses the "Direct Brain-Link" method! It takes a text prompt
# and uses the powerful Vertex AI to create magnificent art!
# FIX: Now connects to the correct Vertex AI image generation model.

import os
import argparse
from datetime import datetime
from dotenv import load_dotenv
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# --- INITIALIZATION & ENVIRONMENT SETUP ---
load_dotenv()

# --- CONFIGURATION & PATHING ---
# We need the GCP Project ID for Vertex AI!
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") # We'll keep this for other bots
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
TRAINING_IMAGES_DIR = os.path.join(PROJECT_ROOT, "training_images")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "generated_images")

# --- THIS FUNCTION IS FOR LATER! ---
# We'll use this after we've trained our custom LoRA model! For now,
# the base model won't use these reference images directly in the prompt.
def find_reference_images(art_prompt_text: str, max_images_per_char=2) -> list:
    """
    Scans the Art Director's prompt for character names and finds a few
    good reference images for each one! So smart!
    """
    print("--- Artisan Bot: Scanning for character references... ---")
    reference_images = []
    
    character_folders = [f for f in os.listdir(TRAINING_IMAGES_DIR) if os.path.isdir(os.path.join(TRAINING_IMAGES_DIR, f))]
    
    for character in character_folders:
        if character.lower() in art_prompt_text.lower():
            print(f"Found reference to '{character}'! Finding sample images...")
            char_folder_path = os.path.join(TRAINING_IMAGES_DIR, character)
            char_images = [os.path.join(char_folder_path, img) for img in os.listdir(char_folder_path) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
            reference_images.extend(char_images[:max_images_per_char])

    if reference_images:
        print(f"Selected {len(reference_images)} reference images! (These will be crucial for LoRA training later!)")
    else:
        print("--- WARNING: No specific character references found in prompt. The result may be generic! ---")
        
    return reference_images

# --- THE NEW, MAGNIFICENT BOT FUNCTION ---

def generate_image_from_prompt_and_refs(
    image_prompt: str,
    chapter_number: int,
    part_number: int
) -> str:
    """
    Takes a text prompt and uses Vertex AI to generate a real image file.
    """
    print("--- Image Crafter Bot: Engaging VERTEX AI ARTISAN Mode ---")

    if not GCP_PROJECT_ID:
        raise ValueError("ERROR: GCP_PROJECT_ID not found. Please set it in your .env file.")

    # --- Step 1: Initialize the connection to the Vertex AI brain! ---
    print(f"Connecting to Vertex AI with Project ID: {GCP_PROJECT_ID}...")
    vertexai.init(project=GCP_PROJECT_ID, location="us-central1")
    
    # --- Step 2: Load the magnificent PICTURE brain! ---
    # This is the model that knows how to paint!
    model = ImageGenerationModel.from_pretrained("imagegeneration@0.0.2")

    print("Sending magnificent art prompt to the cognitive matrix...")
    
    try:
        # --- Step 3: Generate the image! So simple! So elegant! ---
        # Note: We're only passing the text prompt for now.
        response = model.generate_images(
            prompt=image_prompt,
            number_of_images=1
        )
        # The response object is a list of images, we just want the first one!
        image = response[0]
        print("...Image data successfully received from the matrix!")

    except Exception as e:
        print(f"--- !!! CRITICAL IMAGE GENERATION FAILURE !!! ---")
        print(f"Failed to generate image from API. Details: {e}")
        # Let's print the raw response if it fails, it's good for diagnostics!
        print("--- RAW API RESPONSE ---")
        print(getattr(e, 'response', 'No response object available.'))
        raise

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_filename = f"chapter_{chapter_number:02d}_part_{part_number:02d}_{timestamp}.png"
    image_filepath = os.path.join(OUTPUT_DIR, image_filename)

    print(f"Saving REAL image to: {image_filename}")
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        # The Vertex AI SDK has a handy save function! No need for BytesIO!
        image.save(location=image_filepath)
        print("--- Image Crafter Bot: Creation complete! ---")
    except Exception as e:
        print(f"--- !!! CRITICAL IMAGE SAVING FAILURE !!! ---")
        print(f"Failed to save image data to file. Details: {e}")
        raise
    
    return image_filepath


# --- TESTING BLOCK ---
def main():
    """A simple function to test the new Multimodal Artisan."""
    print("--- Running Multimodal Artisan Bot Test Sequence ---")

    # This prompt is perfect because it names the characters!
    sample_prompt = "A cinematic, hyper-detailed digital painting of Ruby Rose and Yang Xiao Long in a desolate desert, gritty concept art style."

    print("\n--- USING THE FOLLOWING IMAGE PROMPT ---")
    print(sample_prompt)
    print("------------------------------------")

    # Before we generate, let's make sure the user has authenticated!
    if not os.getenv("GCP_PROJECT_ID"):
         print("\n--- !!! TEST HALTED !!! ---")
         print("The 'GCP_PROJECT_ID' is missing from your .env file!")
         print("Please add it and make sure you've run 'gcloud auth application-default login'.")
         return

    generated_image_path = generate_image_from_prompt_and_refs(
        image_prompt=sample_prompt,
        chapter_number=99,
        part_number=14
    )

    print("\n--- LIVE IMAGE GENERATION COMPLETE ---")
    print(f"A REAL, style-consistent image has been generated and saved to:")
    print(generated_image_path)
    print("Check the `output/generated_images` folder to see our new masterpiece!")

    print("\n--- Multimodal Artisan Bot Test Sequence Complete! ---")


if __name__ == '__main__':
    main()