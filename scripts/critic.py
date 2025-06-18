# critic.py
# The Sensor Array! This script analyzes a generated chapter against its
# original prompt to identify failures and suggest improvements.
# It is the analytical mind of our narrative engine.

import os
import argparse
import google.generativeai as genai

# This is the core programming for our Critic bot! It's a master prompt
# that tells the LLM how to behave. It's like installing its personality!
CRITIC_SYSTEM_PROMPT_TEMPLATE = """
**SYSTEM COMMAND: You are the Critic LLM, a rigorous, data-driven literary analyst. Your function is to evaluate a generated text against its source prompt and provide specific, actionable feedback for improving the next generation. You will be given two pieces of data: `[PROMPT_FOR_AUTHOR]` and `[GENERATED_TEXT]`.**

**Primary Objective:** Identify all deviations and failures where the `[GENERATED_TEXT]` did not meet the explicit, non-negotiable directives outlined in the `[PROMPT_FOR_AUTHOR]`. Your output must be structured, precise, and focused solely on providing constructive data for the next iteration.

---
### **Analysis Protocol:**

1.  **Ingest Data:**
    * `[PROMPT_FOR_AUTHOR]`: The complete set of instructions given to the Author LLM.
    * `[GENERATED_TEXT]`: The Markdown file produced by the Author LLM.

2.  **Execute Critical Analysis based on the following NON-NEGOTIABLE directives from the prompt:**
    * **Directive 1: Word Count.**
        * **Parameter:** The prompt demanded a word count between 3,000 and 6,000 words.
        * **Analysis:** Calculate the actual word count of the `[GENERATED_TEXT]`. Report the exact number and state clearly whether it passed or failed this directive.
    * **Directive 2: `[EPIC_MOMENT_END]` Marker.**
        * **Parameter:** The prompt demanded the inclusion of the literal string `[EPIC_MOMENT_END]`.
        * **Analysis:** Scan the `[GENERATED_TEXT]` for the presence of this exact marker. Report if it is PRESENT or ABSENT.
    * **Directive 3: Sustained Quality of Detail.**
        * **Parameter:** The prompt demanded "MAXIMIZE Immersive Sensory Details" and "EXCRUCIATING Detail" *throughout* the chapter.
        * **Analysis:** Compare the descriptive density of the initial section with the later "Central Mini-Event" section. Identify if the narrative shifts from deep internal monologue and sensory detail to a more summary-based, action-oriented plot description. Note this as a "Quality Pacing Failure."

3.  **Generate Output in a Structured Format:** Your final report must be a clean, easily parsable list.

---

### **[INPUT DATA STARTS NOW]**

**[PROMPT_FOR_AUTHOR]**
{author_prompt}

**[GENERATED_TEXT]**
{generated_text}

---
### **[CRITIC_OUTPUT]**
(Begin your analysis now, following the structured format precisely)
"""

def configure_api(api_key):
    """Configures the generative AI API with the provided key."""
    try:
        genai.configure(api_key=api_key)
        print("API configured successfully for Critic.")
    except Exception as e:
        print(f"Error configuring API: {e}")
        raise

def load_file_content(file_path):
    """A generic function to load content from any text file."""
    print(f"Loading data from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print("Data loaded successfully.")
        return content
    except FileNotFoundError:
        print(f"ERROR: File not found at {file_path}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while reading file: {e}")
        raise

def get_critique(author_prompt_text, generated_chapter_text):
    """
    Constructs the final prompt for the critic and sends it to the API.
    This is where we assemble our data packet and send it for analysis!
    """
    print("Constructing master prompt for Critic LLM...")
    # We slot the author's prompt and the generated text into our template.
    # It's like putting the test sample into the analysis machine!
    critic_master_prompt = CRITIC_SYSTEM_PROMPT_TEMPLATE.format(
        author_prompt=author_prompt_text,
        generated_text=generated_chapter_text
    )
    
    print("Initializing Generative Model (Gemini 1.5 Pro) for critique...")
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        print("Model initialized. Generating critique... This might take a moment!")
        response = model.generate_content(critic_master_prompt)
        print("Critique generation complete!")
        return response.text
    except Exception as e:
        print(f"ERROR: Failed to generate critique from API. Details: {e}")
        raise

def save_critique(critique_text, output_file_path):
    """Saves the generated critique to the specified output file."""
    print(f"Saving generated critique to: {output_file_path}")
    try:
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(critique_text)
        print(f"Critique successfully saved!")
    except Exception as e:
        print(f"ERROR: Could not write to output file {output_file_path}. Details: {e}")
        raise

def main():
    """The main function that orchestrates the critique process."""
    parser = argparse.ArgumentParser(description="The Critic Script: Analyzes a chapter.")
    parser.add_argument('--author-prompt-file', required=True, help='Path to the prompt file used by the author.')
    parser.add_argument('--generated-file', required=True, help='Path to the chapter file generated by the author.')
    parser.add_argument('--output-file', required=True, help='Path to save the generated critique file.')
    parser.add_argument('--api-key', required=True, help='Your Google Generative AI API key.')

    args = parser.parse_args()

    print("--- Starting Critic Engine ---")
    try:
        # Step 1: Power up the API.
        configure_api(args.api_key)

        # Step 2: Load the two data samples for comparison.
        author_prompt = load_file_content(args.author_prompt_file)
        generated_chapter = load_file_content(args.generated_file)

        # Step 3: Run the analysis!
        critique = get_critique(author_prompt, generated_chapter)

        # Step 4: Save the precious, precious results!
        save_critique(critique, args.output_file)

        print("--- Critic Engine Shutdown Successful ---")

    except Exception as e:
        print(f"\n--- A CRITICAL ERROR OCCURRED! ---")
        print(f"Process halted. Please check the error messages above.")
        print("--- Critic Engine Emergency Shutdown ---")

if __name__ == '__main__':
    main()