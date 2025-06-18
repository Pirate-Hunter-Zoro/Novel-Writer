# chapter_generator.py
# The Master Control Program! The Brain! The Conductor! (VERSION 2.1 - Parsing Upgrade)
# This script orchestrates the conversation between author.py and critic.py,
# creating a self-correcting loop to generate the perfect chapter.

import os
import argparse
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv

output_dir = "output/generated_chapters"
prompts_file = "knowledge_db/rwby_chapter_prompts.md"


# This is the system prompt for our NEWEST bot: The Prompt Re-writer!
# Its job is to take a failed prompt and a critique and make the prompt better!
REWRITER_SYSTEM_PROMPT_TEMPLATE = """
**SYSTEM COMMAND: You are the Prompt Re-Writer, a master of instructional design. Your sole purpose is to improve a prompt given to a large language model based on a critique of the previous output.**

**Your Task:** You will receive an `[ORIGINAL_PROMPT]` and a `[CRITIQUE_OF_OUTPUT]`. The critique will detail how the output failed to meet the prompt's requirements. Your job is to rewrite the original prompt to be clearer, more explicit, and more directive to fix those specific failures.

**Key Directives:**
1.  **Integrate Feedback:** Directly address every "Actionable Recommendation" from the critique.
2.  **Reinforce Rules:** Make the non-negotiable rules (like word count and marker inclusion) even more prominent and demanding. Use bold text, all-caps, and assertive language.
3.  **Do Not Lose Intent:** Do not remove or alter the core creative goals of the original prompt. Only add to it and clarify it based on the critique.
4.  **Output Only the New Prompt:** Your final output should ONLY be the full, complete, rewritten prompt text. Do not include any other conversational text or explanation.

---
### **[INPUT DATA STARTS NOW]**

**[ORIGINAL_PROMPT]**
{original_prompt}

**[CRITIQUE_OF_OUTPUT]**
{critique_text}

---
### **[REWRITTEN_PROMPT_FOR_NEXT_ITERATION]**
(Begin your rewritten prompt now. Output only the prompt text.)
"""

def configure_api(api_key):
    """Configures the generative AI API."""
    try:
        genai.configure(api_key=api_key)
        print("API configured successfully for the Conductor.")
    except Exception as e:
        print(f"Error configuring API: {e}")
        raise

def run_script(command):
    """A helper function to run our other python scripts."""
    print(f"\n----- EXECUTING COMMAND: {' '.join(command)} -----")
    try:
        subprocess.run(command, check=True, text=True, capture_output=False)
        print(f"----- COMMAND SUCCEEDED -----\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"----- COMMAND FAILED -----")
        print(f"Error running script: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except FileNotFoundError as e:
        print(f"----- COMMAND FAILED -----")
        print(f"Error: Script not found. Make sure author.py and critic.py are in the same directory.")
        print(f"Details: {e}")
        return False

def load_file_content(file_path):
    """Loads content from a file. We need this to read the prompts and critiques."""
    print(f"Reading data from file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found at {file_path}. Halting.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while reading {file_path}: {e}")
        raise

#! ---------------------------------------------------------------- !#
#! RECALIBRATED PARSING LOGIC! This is the important part!          !#
#! The librarian bot now correctly grabs the *entire* chapter block,!#
#! not just the text in the code fence. More data! Better data!     !#
#! ---------------------------------------------------------------- !#
def extract_prompt_for_chapter(all_prompts_text, chapter_number):
    """
    Parses the large markdown file to find and extract the entire text block for a specific chapter prompt.
    """
    print(f"Searching for Chapter {chapter_number} prompt block in the master file...")
    # This is the unique text that marks the beginning of each chapter's prompt
    start_marker = f"## Chapter {chapter_number} Prompt:"
    # The end marker is just the start of the next chapter
    end_marker = f"## Chapter {chapter_number + 1} Prompt:"

    start_index = all_prompts_text.find(start_marker)
    if start_index == -1:
        print(f"ERROR: Could not find start marker for Chapter {chapter_number}. Is the number correct?")
        return None

    print(f"Found start marker for Chapter {chapter_number}.")
    end_index = all_prompts_text.find(end_marker, start_index)
    
    prompt_text = ""
    if end_index == -1:
        # If we can't find the *next* chapter, it must be the last one! So we take everything from its start.
        print("End marker not found, assuming this is the last chapter in the file.")
        prompt_text = all_prompts_text[start_index:]
    else:
        # If we found the next chapter, we slice the text to get just our part!
        print(f"Found end marker for Chapter {chapter_number + 1}. Slicing text.")
        prompt_text = all_prompts_text[start_index:end_index]
    
    print("Prompt extraction successful!")
    return prompt_text.strip()


def rewrite_prompt(original_prompt, critique_text):
    """Uses the LLM to rewrite the prompt based on the critique."""
    print("Constructing prompt for the Re-Writer LLM...")
    rewriter_master_prompt = REWRITER_SYSTEM_PROMPT_TEMPLATE.format(
        original_prompt=original_prompt,
        critique_text=critique_text
    )

    print("Initializing Re-Writer Model (Gemini 1.5 Pro)...")
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        print("Model initialized. Generating improved prompt...")
        response = model.generate_content(rewriter_master_prompt)
        print("New prompt generated!")
        return response.text
    except Exception as e:
        print(f"ERROR: Failed to generate new prompt from API. Details: {e}")
        raise

def main():
    """The main function that runs the entire generation and correction loop."""
    load_dotenv() # This finds the secret .env file! GOOD!

    parser = argparse.ArgumentParser(description="The Master Control Program for Novel Generation (v2.1).")
    parser.add_argument('--chapter-number', type=int, required=True, help='The number of the chapter to generate.')
    parser.add_argument('--max-iterations', type=int, default=3, help='Maximum number of correction loops to run.')
    
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in .env file! Make sure the .env file exists and the key name is correct.")
        return # Stop if we can't find the key!

    print("---  activating narrative engine v2.1 ---")
    try:
        configure_api(api_key) # Now this line will work!

        chapter_output_dir = os.path.join(output_dir, f'chapter_{args.chapter_number:02d}')
        os.makedirs(chapter_output_dir, exist_ok=True)
        print(f"All artifacts for this run will be saved in: {chapter_output_dir}")

        all_prompts_text = load_file_content(prompts_file)

        initial_prompt_text = extract_prompt_for_chapter(all_prompts_text, args.chapter_number)
        if not initial_prompt_text:
            print(f"Could not extract prompt for Chapter {args.chapter_number}. Aborting mission!")
            return
            
        current_prompt_text = initial_prompt_text

        for i in range(1, args.max_iterations + 1):
            print(f"\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print(f"  STARTING ITERATION {i}/{args.max_iterations} for Chapter {args.chapter_number}")
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

            prompt_file = os.path.join(chapter_output_dir, f'prompt_v{i}.md')
            chapter_file = os.path.join(chapter_output_dir, f'chapter_v{i}.md')
            critique_file = os.path.join(chapter_output_dir, f'critique_v{i}.md')

            print(f"Saving current prompt to {prompt_file}")
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(current_prompt_text)

            # Step 1: Call the Author to write the chapter
            # Pass the key directly to the command!
            #! FIX IS HERE! Added 'scripts/' to the path!
            author_command = ['python', 'scripts/author.py', '--prompt-file', prompt_file, '--output-file', chapter_file, '--api-key', api_key]
            if not run_script(author_command):
                print("Author script failed. Halting process.")
                break

            # Step 2: Call the Critic to analyze the chapter
            # Pass the key directly to the command here too!
            #! AND THE FIX IS HERE TOO!
            critic_command = ['python', 'scripts/critic.py', '--author-prompt-file', prompt_file, '--generated-file', chapter_file, '--output-file', critique_file, '--api-key', api_key]
            if not run_script(critic_command):
                print("Critic script failed. Halting process.")
                break
                
            critique_text = load_file_content(critique_file)

            if "FAILURE" not in critique_text.upper():
                print("\n**************************************")
                print(f"  SUCCESS! Critique reports no failures for Chapter {args.chapter_number}!")
                print(f"  Final chapter saved to: {chapter_file}")
                print("**************************************")
                break
            
            print("Critique reported failures. Attempting to rewrite prompt...")

            current_prompt_text = rewrite_prompt(current_prompt_text, critique_text)
            
            if i == args.max_iterations:
                print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("  Max iterations reached without success.")
                print(f"  Check the final artifacts in: {chapter_output_dir}")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print("\n--- narrative engine shutdown ---")
    
    except Exception as e:
        print(f"\n--- A CRITICAL ERROR OCCURRED IN THE MAIN ENGINE! ---")
        print(f"Process halted. Please check the error messages above. Details: {e}")
        print("--- Conductor Engine Emergency Shutdown ---")


if __name__ == '__main__':
    main()