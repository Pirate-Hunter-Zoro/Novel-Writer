import os
import argparse
import google.generativeai as genai

def configure_api(api_key):
    """Configures the generative AI API with the provided key."""
    try:
        genai.configure(api_key=api_key)
        print("API configured successfully.")
    except Exception as e:
        print(f"Error configuring API: {e}")
        raise

def load_prompt(prompt_file_path):
    """Loads the content of the prompt file."""
    print(f"Loading prompt from: {prompt_file_path}")
    try:
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            prompt_text = f.read()
        print("Prompt loaded successfully.")
        return prompt_text
    except FileNotFoundError:
        print(f"ERROR: Prompt file not found at {prompt_file_path}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while reading the prompt file: {e}")
        raise

def generate_chapter(prompt_text):
    """
    Sends the prompt to the Gemini 1.5 Pro model and generates the chapter text.
    This is where the magic happens! We're sending our instructions to the great
    story-telling machine in the sky!
    """
    print("Initializing Generative Model (Gemini 1.5 Pro)...")
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        print("Model initialized. Generating content... This might take a moment!")
        # We send the prompt and ask the model to generate the content!
        response = model.generate_content(prompt_text)
        print("Content generation complete!")
        return response.text
    except Exception as e:
        print(f"ERROR: Failed to generate content from API. Details: {e}")
        # This could be an API key issue, a connection problem, or something else!
        raise

def save_chapter(chapter_text, output_file_path):
    """Saves the generated chapter text to the specified output file."""
    print(f"Saving generated chapter to: {output_file_path}")
    try:
        # Ensure the output directory exists. It's like making sure the lab has a floor!
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(chapter_text)
        print(f"Chapter successfully saved!")
    except Exception as e:
        print(f"ERROR: Could not write to output file {output_file_path}. Details: {e}")
        raise

def main():
    """
    The main function that orchestrates the authoring process.
    It's the master switch for this specific machine!
    """
    # Set up the command-line interface. This is how the 'brain' will talk to this script!
    parser = argparse.ArgumentParser(description="The Author Script: Generates a chapter from a prompt.")
    parser.add_argument('--prompt-file', required=True, help='Path to the .md file containing the chapter prompt.')
    parser.add_argument('--output-file', required=True, help='Path to save the generated .md chapter file.')
    parser.add_argument('--api-key', required=True, help='Your Google Generative AI API key.')

    args = parser.parse_args()

    print("--- Starting Author Engine ---")
    try:
        # Step 1: Configure the API. No power, no machines!
        configure_api(args.api_key)

        # Step 2: Load our brilliant instructions.
        prompt = load_prompt(args.prompt_file)

        # Step 3: Generate the narrative! This is the big one!
        generated_text = generate_chapter(prompt)

        # Step 4: Save the glorious data!
        #! THE FIX IS RIGHT HERE! Changed the hyphen to an underscore!
        save_chapter(generated_text, args.output_file)

        print("--- Author Engine Shutdown Successful ---")

    except Exception as e:
        # If any of our delicate machinery breaks, we need to know!
        print(f"\n--- A CRITICAL ERROR OCCURRED! ---")
        print(f"Process halted. Please check the error messages above.")
        print("--- Author Engine Emergency Shutdown ---")


if __name__ == '__main__':
    main()