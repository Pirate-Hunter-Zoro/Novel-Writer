# image_generator.py (v12.0 - The Multimodal Artisan!)
# This bot uses the "Direct Brain-Link" method! It takes a text prompt
# AND reference images to create magnificent, style-consistent art!

import os
import argparse
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io

# --- INITIALIZATION & ENVIRONMENT SETUP ---
load_dotenv()

# --- CONFIGURATION & PATHING ---
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
TRAINING_IMAGES_DIR = os.path.join(PROJECT_ROOT, "training_images")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "generated_images")

# --- NEW HELPER FUNCTION! ---
def find_reference_images(art_prompt_text: str, max_images_per_char=2) -> list:
    """
    Scans the Art Director's prompt for character names and finds a few
    good reference images for each one! So smart!
    """
    print("--- Artisan Bot: Scanning for character references... ---")
    reference_images = []
    
    # We get a list of all our character folders (Ruby, Blake, etc.)
    character_folders = [f for f in os.listdir(TRAINING_IMAGES_DIR) if os.path.isdir(os.path.join(TRAINING_IMAGES_DIR, f))]
    
    for character in character_folders:
        # If the character's name is in the prompt...
        if character.lower() in art_prompt_text.lower():
            print(f"Found reference to '{character}'! Finding sample images...")
            char_folder_path = os.path.join(TRAINING_IMAGES_DIR, character)
            
            # ...we grab a few images from their folder!
            char_images = [os.path.join(char_folder_path, img) for img in os.listdir(char_folder_path) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # We add up to 'max_images_per_char' to our list!
            reference_images.extend(char_images[:max_images_per_char])

    if reference_images:
        print(f"Selected {len(reference_images)} reference images to use as a vision board!")
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
    Takes a text prompt AND reference images and generates a real image file.
    """
    print("--- Image Crafter Bot: Engaging MULTIMODAL ARTISAN Mode ---")

    if not GEMINI_API_KEY:
        raise ValueError("ERROR: GOOGLE_API_KEY not found. Please set it in your .env file.")

    genai.configure(api_key=GEMINI_API_KEY)

    # We use our most powerful multimodal model!
    model = genai.GenerativeModel('gemini-2.5-pro')

    # --- Step 1: Find our reference images! ---
    reference_image_paths = find_reference_images(image_prompt)

    # --- Step 2: Build the magnificent "Vision Board" prompt! ---
    # It's a list that contains text and images! EEEEE! So cool!
    vision_board_prompt = [
        "You are a master artist. Your task is to generate an image that strictly follows the user's text prompt. Additionally, you MUST use the provided reference images to inform the exact appearance, clothing, and art style of the characters. The final image's style should perfectly match the style of the reference images.",
        "--- TEXT PROMPT ---",
        image_prompt,
        "--- REFERENCE IMAGES ---"
    ]
    
    # We load our reference images and add them to the vision board!
    for path in reference_image_paths:
        try:
            vision_board_prompt.append(Image.open(path))
        except Exception as e:
            print(f"--- ⚠️ WARNING: Could not load reference image at {path}. Skipping. Error: {e} ---")

    print("Sending magnificent vision board to the cognitive matrix...")
    
    try:
        response = model.generate_content(vision_board_prompt)
        image_data = response.candidates[0].content.parts[0].blob.data
        print("...Image data successfully received from the matrix!")

    except Exception as e:
        print(f"--- !!! CRITICAL IMAGE GENERATION FAILURE !!! ---")
        print(f"Failed to generate image from API. Details: {e}")
        raise

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_filename = f"chapter_{chapter_number:02d}_part_{part_number:02d}_{timestamp}.png"
    image_filepath = os.path.join(OUTPUT_DIR, image_filename)

    print(f"Saving REAL image to: {image_filename}")
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        image = Image.open(io.BytesIO(image_data))
        image.save(image_filepath)
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