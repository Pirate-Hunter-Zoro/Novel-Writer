# art_director.py (v1.0 - The Visual Dreamer)
# This bot analyzes the approved prose of a chapter part and generates
# a detailed, high-quality prompt for an image generation model.

import os
import argparse
from dotenv import load_dotenv
import google.generativeai as genai

# --- INITIALIZATION & ENVIRONMENT SETUP ---
load_dotenv()

# --- CONFIGURATION ---
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- BOT FUNCTION ---

def generate_image_prompt_from_prose(prose_text: str) -> str:
    """
    Uses the most powerful Gemini model to analyze prose and create a rich
    image prompt.
    """
    print("--- Art Director Bot: Engaging VISUAL ANALYSIS Mode ---")

    if not GEMINI_API_KEY:
        raise ValueError("ERROR: GOOGLE_API_KEY not found. Please set it in your .env file.")

    genai.configure(api_key=GEMINI_API_KEY)

    # We use our most powerful model for this complex, subjective, creative task!
    model = genai.GenerativeModel('gemini-2.5-pro')  # Using the powerful art director model!

    # This meta-prompt is the Art Director's soul! It tells the AI how to think like an artist.
    meta_prompt = f"""
    You are an expert Art Director with a profound understanding of visual storytelling, composition, and emotional impact. Your task is to read the following section of a novel and generate a single, high-quality, detailed prompt for an advanced AI image generation model.

    **Your Process:**
    1.  **Identify the Core Moment:** Read the entire text and identify the single most visually compelling and emotionally resonant moment. This could be a dramatic action, a quiet character beat, or a stunning landscape reveal.
    2.  **Construct the Prompt:** Build a detailed prompt that vividly describes this moment.

    **Prompt Requirements:**
    * **Subject & Action:** Clearly describe the main character(s), their poses, expressions, and what they are doing.
    * **Composition & Framing:** Specify the shot type (e.g., "wide shot," "extreme close-up," "medium shot from a low angle").
    * **Environment & Background:** Detail the surroundings, including key landmarks, textures, and atmospheric conditions.
    * **Lighting:** Describe the quality of the light (e.g., "harsh midday sun," "soft twilight," "ominous, magical glow").
    * **Color Palette & Mood:** Suggest the dominant colors and the overall mood or tone (e.g., "desaturated and grim," "vibrant and hopeful," "dark and terrifying").
    * **Style:** Specify a desired art style (e.g., "hyper-realistic digital painting," "cinematic anime style," "gritty, textured concept art").
    * **Negative Prompt (Optional but helpful):** Suggest things to avoid (e.g., "no text, no speech bubbles, not blurry").

    --- PROSE TO ANALYZE ---
    {prose_text}
    ---

    Now, generate the single, detailed image prompt.
    """

    print("Art Director Bot: Analyzing prose for visual potential...")
    response = model.generate_content(meta_prompt)
    print("Art Director Bot: Image prompt generated!")

    return response.text.strip()


# --- TESTING BLOCK ---
def main():
    """A simple function to test the Art Director bot's capabilities."""
    print("--- Running Art Director Bot Test Sequence ---")

    # 1. Create a sample piece of prose to analyze
    sample_prose = """
    The silence that followed their return was a fraud. It was a thin veneer stretched taut over a cacophony of howling wind and the frantic, ragged symphony of their own breathing. Here, in the heart of Vacuo’s desolation, the world was an anvil and the sun a hammer, beating down with a relentless, percussive force that baked the very air until it shimmered like troubled water.

    Yang stood with her feet planted wide, a defiant silhouette against the shimmering horizon. For her, the heat was a tangible enemy, something to be met with a stubborn glare and clenched fists. Her cybernetic arm, a marvel of Atlesian engineering, had become a brand. The metal, exposed to the direct solar onslaught, was a conduit of pure heat, radiating a searing warmth through its socket into the very bone of her shoulder. She consciously kept it away from her body, the air around it visibly wavering. Her gaze flickered to Ruby, and the fire in her eyes banked into a smoldering, protective concern.

    Ruby herself was the quietest of all. She stood slightly apart, Crescent Rose planted in the sand beside her like a grim, metal shepherd’s crook. The metallic scent of her scythe, the familiar heft of its grip in her hand—these were the only anchors tethering her to this blistering present. *I led them here,* the insidious thought whispered, a chilling counterpoint to the hot wind. *I led them to the fall. Now… what?* She looked at Jaune, then at Weiss and Blake and her sister, seeing not just her team, but the totality of her responsibility manifest as four figures slowly being worn down by the elements.
    """

    print("\n--- ANALYZING THE FOLLOWING PROSE ---")
    print(sample_prose)
    print("------------------------------------")

    # 2. Run the prompt generation function
    image_prompt = generate_image_prompt_from_prose(sample_prose)

    # 3. Display the magnificent result!
    print("\n--- GENERATED IMAGE PROMPT ---")
    print(image_prompt)

    print("\n--- Art Director Bot Test Sequence Complete! ---")


if __name__ == '__main__':
    main()