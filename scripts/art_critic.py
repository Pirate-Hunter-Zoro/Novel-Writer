# art_critic.py (v1.0 - The Visual Calibrator)
# This bot analyzes a generated image against the original art prompt
# to ensure perfect adherence to the vision.

import os
import argparse
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# --- INITIALIZATION & ENVIRONMENT SETUP ---
load_dotenv()

# --- CONFIGURATION ---
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- BOT FUNCTION ---

def critique_image(
    image_path: str,
    original_art_prompt: str
) -> str:
    """
    Analyzes a generated image against the prompt it was created from.
    """
    print("--- Art Critic Bot: Engaging VISUAL ANALYSIS Mode ---")

    if not GEMINI_API_KEY:
        raise ValueError("ERROR: GOOGLE_API_KEY not found. Please set it in your .env file.")

    genai.configure(api_key=GEMINI_API_KEY)

    # We need a powerful multimodal model that can understand both text and images!
    # 'gemini-2.5-pro' is perfect for this complex analytical task.
    model = genai.GenerativeModel('gemini-2.5-pro')

    print(f"Art Critic Bot: Loading and analyzing image from {os.path.basename(image_path)}...")
    try:
        image_to_analyze = Image.open(image_path)
    except FileNotFoundError:
        print(f"--- !!! CRITICAL CRITIC ERROR !!! ---")
        print(f"Image file not found at path: {image_path}")
        raise

    # This is our meta-prompt! We give the AI the image AND the rules it was
    # supposed to follow, then ask it to be our critic!
    meta_prompt = [
        "You are an expert Art Critic with a meticulous eye for detail. Your task is to analyze the provided image and determine if it perfectly matches the detailed 'ORIGINAL ART PROMPT' it was generated from. Analyze every aspect: subject, action, composition, environment, lighting, and style.",
        "## ORIGINAL ART PROMPT:",
        original_art_prompt,
        "## IMAGE TO ANALYZE:",
        image_to_analyze,
        "## YOUR CRITIQUE:",
        "Review the image against the prompt. If it is a perfect match in every aspect, your ONLY response must be the single word: SUCCESS. If there are any discrepancies, no matter how small, provide a bulleted list of specific, actionable points of feedback for the artist on what to change. Be strict and precise."
    ]

    print("Art Critic Bot: Sending image and prompt to the cognitive matrix for review...")
    response = model.generate_content(meta_prompt)
    print("Art Critic Bot: Analysis complete!")

    return response.text.strip()

# --- TESTING BLOCK ---
def main():
    """A simple function to test the Art Critic bot's capabilities."""
    print("--- Running Art Critic Bot Test Sequence ---")

    # 1. We need a sample prompt for the test
    sample_art_prompt = """
A cinematic, hyper-detailed digital painting of a female warrior with a giant scythe.
**Subject & Action:** The warrior has short, dark hair with red tips. She is wearing a red cloak and a determined expression.
**Style:** Gritty, textured concept art in an anime style.
"""

    # 2. We need a path to an image to test.
    # IMPORTANT: For this test to work, you MUST have an image file at this path!
    # You can use the one we generated in the last step!
    # Just update the filename to match the one in your 'output/generated_images' folder.
    test_image_path = "output/generated_images/chapter_99_part_12_20250719084739.png" # <--- UPDATE THIS FILENAME!

    if not os.path.exists(test_image_path):
        print(f"\n--- !!! TEST HALTED !!! ---")
        print(f"Could not find the test image at '{test_image_path}'.")
        print("Please update the 'test_image_path' variable in the script to point to a real image.")
        return

    print("\n--- ANALYZING THE FOLLOWING IMAGE ---")
    print(f"File: {os.path.basename(test_image_path)}")
    print("\n--- AGAINST THIS PROMPT ---")
    print(sample_art_prompt)
    print("------------------------------------")

    # 3. Run the critique function
    critique_result = critique_image(
        image_path=test_image_path,
        original_art_prompt=sample_art_prompt
    )

    # 4. Display the magnificent result!
    print("\n--- CRITIQUE RESULT ---")
    print(critique_result)

    print("\n--- Art Critic Bot Test Sequence Complete! ---")


if __name__ == '__main__':
    main()