# scripts/art_critic.py

import argparse
import os
import glob
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image

# --- Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
VISION_MODEL_NAME = "gemini-2.5-pro"
TRAINING_IMAGES_DIR = os.path.join(os.path.dirname(__file__), '..', 'training_images')

def critique_art(generated_image_path, original_prompt, characters):
    print(f"Art Critic Bot v2.4 (Robust Scanner Edition) activated! Engaging the {VISION_MODEL_NAME} visual cortex...")

    # --- Find Our Style Reference Images! ---
    reference_images = {}
    print("Searching for character style references...")
    for full_char_name in characters:
        # Reverted the incorrect .lower() change! We're using the capitalized name now.
        first_name = full_char_name.split()[0]
        
        char_folder = os.path.join(TRAINING_IMAGES_DIR, first_name)
        if not os.path.isdir(char_folder):
            print(f"WARNING: No training directory found for character '{first_name}'. Skipping style check for them.")
            continue
        
        # --- NEW ROBUST SCANNER! ---
        # Instead of glob, we'll list all files and then check them. It's more reliable!
        try:
            all_files = os.listdir(char_folder)
            found_images = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        except Exception as e:
            print(f"ERROR: Could not scan directory {char_folder}. Details: {e}")
            continue
        # --- END OF NEW SCANNER ---

        if found_images:
            # We'll use the first image we find as the reference.
            reference_path = os.path.join(char_folder, found_images[0])
            reference_images[full_char_name] = reference_path
            print(f"  - Found style reference for {full_char_name} in folder '{first_name}': {os.path.basename(reference_path)}")
        else:
            print(f"WARNING: No images found in the directory for character: {first_name}")
    
    if not reference_images and characters:
        print("ERROR: Could not find any valid reference images for the characters provided. Cannot perform critique.")
        return "ERROR: No reference images found."

    # --- Build the Prompt for our Super-Smart Critic Bot! ---
    try:
        model = genai.GenerativeModel(VISION_MODEL_NAME)
        
        prompt_parts = [
            "You are a meticulous Art Critic. Your task is to evaluate a 'Generated Image' based on two equally important criteria:\n"
            "1.  **Character Style Adherence:** The artistic style (line work, color, shading, facial features, and clothing) for each character in the 'Generated Image' MUST stylistically match their corresponding 'Reference Image'.\n"
            "2.  **Prompt Content Adherence:** The 'Generated Image' must accurately depict the scene, actions, and objects described in the 'Original Prompt'.\n\n"
            "Analyze the following images and prompt, then provide your verdict.\n"
            "If the 'Generated Image' is a strong match for BOTH style and content, respond with only the single word: SUCCESS\n"
            "Otherwise, respond with a short, bulleted list of the specific changes needed to improve the image, prefixed with the word: CORRECTIONS:"
        ]

        for char_name, img_path in reference_images.items():
            prompt_parts.append(f"\n--- REFERENCE IMAGE FOR {char_name.upper()} ---")
            prompt_parts.append(PIL.Image.open(img_path))
        
        prompt_parts.append("\n--- GENERATED IMAGE TO CRITIQUE ---")
        prompt_parts.append(PIL.Image.open(generated_image_path))
        
        prompt_parts.append(f"\n--- ORIGINAL PROMPT ---")
        prompt_parts.append(original_prompt)

        print("\nSending all data to the visual cortex for analysis... This might take a moment.")
        response = model.generate_content(prompt_parts)
        
        print("\n--- [CRITIC'S VERDICT] ---")
        verdict = response.text.strip()
        print(verdict)
        print("--------------------------")
        
        return verdict

    except Exception as e:
        print(f"ERROR: A critical failure in the Art Critic's visual sensors!")
        print(f"Error details: {e}")
        return f"ERROR: {e}"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="The Character-Aware Art Critic Bot.")
    parser.add_argument("--generated-image-path", required=True, help="Path to the newly generated image.")
    parser.add_argument("--original-prompt", required=True, help="The original text prompt used for generation.")
    parser.add_argument("--characters", nargs='+', required=True, help="A list of important character names present in the scene.")
    
    args = parser.parse_args()
    
    critique_art(args.generated_image_path, args.original_prompt, args.characters)