# scripts/art_diplomat.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# We'll use a smart model for this translation task!
MODEL_NAME = "gemini-1.5-pro-latest"

def translate_critique_to_prompt(original_prompt, critique_text):
    """
    Translates a list of critiques into a positive, actionable revision prompt.
    """
    print("🤝 Art Diplomat activated! Translating critique into actionable instructions...")
    
    model = genai.GenerativeModel(MODEL_NAME)
    
    # This is the instruction manual for our new diplomat bot!
    diplomat_prompt = f"""
    You are an expert art director translating feedback into actionable instructions for an AI image revision model. Your task is to convert a list of critiques into a single, positive, and clear prompt that tells the AI what to DO, not what it did wrong.

    - **Focus on Positive Actions:** Rephrase critiques as direct commands (e.g., "Add a character," "Change hair color to red," "Adjust the character's expression to be smiling").
    - **Incorporate Original Intent:** Blend these new instructions with the core concepts of the 'Original Prompt'.
    - **Combine and Synthesize:** Condense all instructions into a single, coherent paragraph.
    - **Maintain Safety:** Ensure the new prompt is evocative but avoids words that might trigger safety filters (e.g., 'fight', 'brutal', 'blood').

    **Original Prompt:**
    ---
    {original_prompt}
    ---

    **Critic's Feedback (What to fix):**
    ---
    {critique_text}
    ---

    Now, generate a single paragraph representing the new, combined, and positive revision prompt.
    """

    try:
        response = model.generate_content(diplomat_prompt)
        new_prompt = response.text.strip()
        print(f"  - Diplomat's translation successful! New prompt: '{new_prompt}'")
        return new_prompt
    except Exception as e:
        print(f"  - 💥 Art Diplomat malfunctioned! Error: {e}")
        # Failsafe: return the original critique, though it might fail again.
        return critique_text