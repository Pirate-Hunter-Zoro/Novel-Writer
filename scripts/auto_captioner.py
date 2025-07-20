# scripts/auto_captioner.py

import os
import google.generativeai as genai
import argparse
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

# --- Configuration ---
MODEL_NAME = "gemini-1.5-flash"
# --- UPGRADED PROMPT ---
# We make the prompt a template that we can fill with the character's name.
PROMPT_TEMPLATE = (
    "You are an expert LoRA image tagger. Your task is to generate a comma-separated list of keywords "
    "for an image of a character from the show RWBY. The character's name is {character_name}.\n\n"
    "CRITICAL INSTRUCTIONS:\n"
    "1. The caption MUST start with the unique trigger word: '{trigger_word}'.\n"
    "2. List only objective, visual features like hair color, eye color, clothing, weapon, and any unique "
    "racial traits like Faunus cat ears. Be concise and accurate."
)


def generate_caption_via_api(image_path, character_name):
    """Sends an image to the Gemini API and gets a caption."""
    print(f"  > Analyzing {image_path.name} via API...")
    
    # --- NEW: Create the dynamic trigger word and prompt ---
    trigger_word = f"{character_name.lower()}_rwby_character"
    prompt_text = PROMPT_TEMPLATE.format(character_name=character_name, trigger_word=trigger_word)
    
    try:
        img = Image.open(image_path)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([prompt_text, img])
        
        caption = response.text.strip()
        return caption
        
    except Exception as e:
        print(f"  ! ERROR: An API error occurred. Details: {e}")
        return None

def process_character_folder(character_name):
    """Processes all images in a specific character's training folder."""
    
    base_folder = Path("training_images")
    character_folder = base_folder / character_name
    
    if not character_folder.is_dir():
        print(f"ERROR: Directory not found: {character_folder}")
        return
        
    print(f"--- Starting API Auto-Captioning for character: {character_name} ---")
    
    image_files = list(character_folder.glob("*.png")) + \
                  list(character_folder.glob("*.jpg")) + \
                  list(character_folder.glob("*.jpeg"))
                  
    if not image_files:
        print(f"No image files found in {character_folder}")
        return

    for image_path in image_files:
        caption_path = image_path.with_suffix(".txt")
        
        if caption_path.exists():
            print(f"  - Skipping {image_path.name}, caption already exists.")
            continue
            
        # --- NEW: Pass the character name to the caption generator ---
        caption_text = generate_caption_via_api(image_path, character_name)
        
        if caption_text:
            with open(caption_path, "w", encoding='utf-8') as f:
                f.write(caption_text)
            print(f"  + Caption saved to {caption_path.name}")
            
    print(f"--- Finished API Auto-Captioning for {character_name} ---")

# --- NEW, SMARTER MAIN BRAIN! ---
def main():
    """
    Finds all character folders in the training_images directory
    and processes each one.
    """
    print("🤖 DEPLOYING AUTONOMOUS CAPTIONER BOT! 🤖")
    
    if not os.getenv('GOOGLE_API_KEY'):
        print("ERROR: The GOOGLE_API_KEY environment variable is not set.")
        print("Please set it to your API key to continue.")
        return

    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
    
    base_folder = Path("training_images")
    if not base_folder.is_dir():
        print(f"ERROR: The base directory '{base_folder}' was not found!")
        return
        
    # This is the magic part! It finds all the folders for us!
    character_folders = [d for d in base_folder.iterdir() if d.is_dir()]
    
    if not character_folders:
        print("No character folders found to process. All done!")
        return
        
    print(f"Found {len(character_folders)} character folders to process!")
    
    for char_folder in character_folders:
        # The name of the folder IS the character's name! So smart!
        process_character_folder(char_folder.name)

    print("\n🎉 ALL FOLDERS PROCESSED! The entire library has been captioned! 🎉")


if __name__ == "__main__":
    # No more arguments! We just run the main brain! WOOO!
    main()