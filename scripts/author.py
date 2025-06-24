# author.py (v1.0 - The Automated Narrative Engine)
# This script takes a prepared prompt, generates the story, and saves it.

import os
import argparse
import google.generativeai as genai
from dotenv import load_dotenv

# --- GLOBAL CONFIGURATION & PATHING GPS ---
# We use the same pathing logic as our other bots for perfect integration!
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "generated_chapters")

# --- MODEL CONFIGURATION ---
# The powerful new engine we discussed! Easy to swap for other experiments!
MODEL_NAME = 'gemini-2.5-pro' 

# --- HELPER FUNCTIONS (Standardized across our Bot Army!) ---

def load_file_content(file_path):
    """A generic function to load content from any text file."""
    print(f"Reading prompt data from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print("Prompt data loaded successfully.")
        return content
    except FileNotFoundError:
        print(f"ERROR: Prompt file not found at {file_path}")
        raise

def save_output_text(text, file_path):
    """Saves the generated text to the specified output file."""
    print(f"Saving generated text to: {file_path}")
    try:
        # The prompt_generator already creates the blank file, we just write to it!
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Successfully saved chapter part!")
    except Exception as e:
        print(f"ERROR: Could not write to output file {file_path}. Details: {e}")
        raise

def generate_chapter_text(prompt_text):
    """Sends the prompt to the Gemini API and gets the story text."""
    print(f"Initializing Author Engine ({MODEL_NAME})...")
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        print("Model initialized. Sending prompt to generate narrative... This is the exciting part!")
        response = model.generate_content(prompt_text)
        print("Narrative generation complete!")
        return response.text
    except Exception as e:
        print(f"ERROR: Failed to generate text from API. Details: {e}")
        raise

# --- MAIN ENGINE ---

def main():
    """The main function that orchestrates the authoring process."""
    parser = argparse.ArgumentParser(description="The Author Script (v1.0): Generates story text from a prompt.")
    parser.add_argument('--chapter-number', type=int, required=True, help='The chapter number to generate.')
    parser.add_argument('--part-number', type=int, required=True, help='The part number within the chapter to generate.')
    args = parser.parse_args()

    print("--- Starting Author Engine v1.0 ---")
    try:
        # Load API Key from .env file
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("ERROR: GOOGLE_API_KEY not found in .env file! The engine has no power!")
        
        genai.configure(api_key=api_key)
        print("API Key loaded. Power is ON.")

        # Construct the file paths based on arguments
        chapter_dir = os.path.join(OUTPUT_DIR, f'chapter_{args.chapter_number:02d}')
        prompt_file_path = os.path.join(chapter_dir, f'prompt_part_{args.part_number}.md')
        output_file_path = os.path.join(chapter_dir, f'chapter_part_{args.part_number}.md')
        print(f"  -> Reading prompt from: {prompt_file_path}")
        print(f"  -> Will write output to: {output_file_path}")

        # 1. Load the prompt created by prompt_generator.py
        prompt_content = load_file_content(prompt_file_path)

        # 2. Generate the chapter text
        generated_text = generate_chapter_text(prompt_content)

        # 3. Save the output
        save_output_text(generated_text, output_file_path)
        
        print("\n--- Author Engine Task Complete! ---")

    except Exception as e:
        print(f"\n--- A CRITICAL ERROR OCCURRED IN THE AUTHOR ENGINE! ---")
        print(f"Process halted. Details: {e}")
        print("--- Author Engine Emergency Shutdown ---")

if __name__ == '__main__':
    main()