# image_generator.py (v13.0 - The Remote-Controlled Art-Cannon!)
# This bot uses the magnificent, non-clusterfucky Stability AI API!
# It actually works this time! FOR SCIENCE!

import os
import argparse
from datetime import datetime
from dotenv import load_dotenv
import io
from PIL import Image

# --- NEW BRAIN-LINK TOOL! ---
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from stability_sdk import client

# --- INITIALIZATION & ENVIRONMENT SETUP ---
load_dotenv()

# --- CONFIGURATION & PATHING ---
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "generated_images")

# --- THE NEW, GLORIOUS, ACTUALLY-FUNCTIONAL BOT! ---

def generate_image_with_api(
    image_prompt: str,
    chapter_number: int,
    part_number: int
) -> str:
    """
    Takes a text prompt and uses the Stability AI API to generate a real image file.
    """
    print("--- Image Crafter Bot: Engaging REMOTE ART-CANNON! ---")

    if not STABILITY_API_KEY:
        raise ValueError("ERROR: STABILITY_API_KEY not found. Please set it in your .env file.")

    # --- Step 1: Establish the brain-link! ---
    print("Connecting to the Stability AI cognitive matrix...")
    stability_api = client.StabilityInference(
        key=STABILITY_API_KEY,
        verbose=True,
        engine="stable-diffusion-xl-1024-v1-0", # Using the magnificent SDXL brain!
    )

    print("Sending magnificent art prompt to the matrix...")
    
    try:
        # --- Step 2: Fire the cannon! ---
        # This sends the prompt and gets the image data back! So simple!
        answers = stability_api.generate(
            prompt=image_prompt,
            steps=50, # More steps can mean more detail!
            cfg_scale=8.0,
            width=1024,
            height=1024,
            samples=1,
            sampler=generation.SAMPLER_K_DPMPP_2M # A good, high-quality sampler!
        )

        print("...Image data successfully received from the matrix!")

        # --- Step 3: Process the magnificent result! ---
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    print("--- !!! WARNING: Your prompt was flagged by the safety filter! Try a different prompt! ---")
                    return None
                if artifact.type == generation.ARTIFACT_IMAGE:
                    # The image data is here! It's a beautiful binary blob!
                    image_data = artifact.binary
                    
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    image_filename = f"chapter_{chapter_number:02d}_part_{part_number:02d}_{timestamp}.png"
                    image_filepath = os.path.join(OUTPUT_DIR, image_filename)

                    print(f"Saving REAL image to: {image_filename}")
                    os.makedirs(OUTPUT_DIR, exist_ok=True)
                    
                    # We save the magnificent blob to a file!
                    image = Image.open(io.BytesIO(image_data))
                    image.save(image_filepath)
                    
                    print("--- Image Crafter Bot: Creation complete! ---")
                    return image_filepath

    except Exception as e:
        print(f"--- !!! CRITICAL IMAGE GENERATION FAILURE !!! ---")
        print(f"Failed to generate image from API. Details: {e}")
        raise
    
    return None


# --- TESTING BLOCK ---
def main():
    """A simple function to test our new remote-controlled art-cannon."""
    print("--- Running Art-Cannon Bot Test Sequence ---")

    sample_prompt = "A cinematic, hyper-detailed digital painting of Ruby Rose with her scythe, in a desolate desert, gritty concept art style, rwby anime."

    print("\n--- USING THE FOLLOWING IMAGE PROMPT ---")
    print(sample_prompt)
    print("------------------------------------")

    if not os.getenv("STABILITY_API_KEY"):
         print("\n--- !!! TEST HALTED !!! ---")
         print("The 'STABILITY_API_KEY' is missing from your .env file!")
         print("Please add it and let's make some art!")
         return

    generated_image_path = generate_image_with_api(
        image_prompt=sample_prompt,
        chapter_number=99,
        part_number=1
    )

    if generated_image_path:
        print("\n--- LIVE IMAGE GENERATION COMPLETE ---")
        print(f"A REAL, magnificent image has been generated and saved to:")
        print(generated_image_path)
        print("Check the `output/generated_images` folder to see our new masterpiece!")
    else:
        print("\n--- IMAGE GENERATION FAILED ---")
        print("The cannon fizzled! Check the logs above for clues!")

    print("\n--- Art-Cannon Bot Test Sequence Complete! ---")


if __name__ == '__main__':
    main()