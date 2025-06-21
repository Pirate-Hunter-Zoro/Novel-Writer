# chapter_generator.py
# The Master Control Program! The Brain! The Conductor! (VERSION 2.1 - Parsing Upgrade)
# This script orchestrates the conversation between author.py and critic.py,
# creating a self-correcting loop to generate the perfect chapter.

import os
import argparse
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
import re

# First, we find the absolute path to the directory where this script lives.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Then, we go up one level to get the main project's root directory.
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PROMPTS_DIR = os.path.join(PROJECT_ROOT, "knowledge_db", "rwby_chapter_prompts")

output_dir = os.path.join(PROJECT_ROOT, "output", "generated_chapters")

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

def extract_five_part_prompts(chapter_file_text, chapter_number):
    """
    Parses the text of a single chapter's prompt file and splits it
    into five sequential micro-prompts using a robust method.
    """
    print(f"Parsing Chapter {chapter_number} prompt file for 5-part sequence...")
    
    # This is our new cutting laser! We split the text every time we see
    # the unique marker '### **Prompt '.
    # This is much more robust than matching whitespace.
    split_marker = r'### \*\*Prompt '
    parts = re.split(split_marker, chapter_file_text)

    if len(parts) < 2:
        # This means the marker was not found at all.
        print(f"ERROR: Could not find any prompts. Check for the '### **Prompt ' marker in your file.")
        return []

    # The first part of the split is the text BEFORE the first prompt, so we skip it.
    # The rest of the parts start with things like '1-A:**...'.
    # We just have to stick the '### **Prompt ' back on the front of each one!
    prompts = []
    for part in parts[1:]:
        # Re-assemble the full prompt with its header.
        full_prompt = "### **Prompt " + part.strip()
        prompts.append(full_prompt)

    if len(prompts) < 5:
        print(f"WARNING: Found {len(prompts)} micro-prompts for Chapter {chapter_number}, expected 5.")
    else:
        print(f"Successfully parsed {len(prompts)} micro-prompts!")
        
    return prompts

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

        # First, build the specific file path using our new PROMPTS_DIR variable.
        chapter_prompt_path = os.path.join(PROMPTS_DIR, f"chapter_{args.chapter_number}.md")
        # Now, load the content from that specific file!
        all_prompts_text = load_file_content(chapter_prompt_path)
            
        five_part_prompts = extract_five_part_prompts(all_prompts_text, args.chapter_number)

        if not five_part_prompts:
            print(f"Could not parse the 5-part prompt for Chapter {args.chapter_number}. Aborting!")
            return

        # This is our canvas! It will hold the story as it grows.
        cumulative_story_text = ""
        final_chapter_file = os.path.join(chapter_output_dir, f'chapter_{args.chapter_number:02d}_complete.md')
        all_parts_generated = True

        # This is the new auto-regressive feedback loop!
        for i, micro_prompt in enumerate(five_part_prompts, 1):
            print(f"\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print(f"  GENERATING PART {i}/5 for Chapter {args.chapter_number}")
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

            # This is the magic! We combine the story so far with the next prompt!
            # This fulfills the instructions from chapter_1.md!
            current_full_prompt = cumulative_story_text + "\n\n" + micro_prompt

            # Define the file paths for this specific step
            prompt_step_file = os.path.join(chapter_output_dir, f'prompt_step_{i}_combined.md')
            
            print(f"Saving combined prompt for step {i} to {prompt_step_file}")
            with open(prompt_step_file, 'w', encoding='utf-8') as f:
                f.write(current_full_prompt)

            # Call the Author bot to continue writing the story!
            author_command = ['python', os.path.join(PROJECT_ROOT, 'scripts', 'author.py'), '--prompt-file', prompt_step_file, '--output-file', final_chapter_file, '--api-key', api_key]
            if not run_script(author_command):
                print(f"Author script failed on part {i}. Halting process.")
                all_parts_generated = False
                break # Exit the loop if a part fails
            
            # This is the feedback loop! We read the new, longer story that the
            # author just wrote and make it our new cumulative text for the next step!
            print("Reading generated text to use as context for the next step...")
            cumulative_story_text = load_file_content(final_chapter_file)

        if all_parts_generated:
            print("\n**************************************")
            print(f"  SUCCESS! All 5 parts of Chapter {args.chapter_number} generated and combined!")
            print(f"  Final chapter saved to: {final_chapter_file}")
            print("**************************************")
            
            # --- FINAL QUALITY ASSURANCE CHECK ---
            print("\n--- Sending final chapter for critique... ---")

            # We need to save the original main prompt from the chapter_X.md file
            # for the critic to use as a reference.
            main_prompt_file = os.path.join(chapter_output_dir, f'prompt_chapter_{args.chapter_number:02d}_main.md')
            print(f"Saving main reference prompt to: {main_prompt_file}")
            with open(main_prompt_file, 'w', encoding='utf-8') as f:
                # The 'all_prompts_text' variable holds the full original prompt text!
                f.write(all_prompts_text)

            # Define the output file for our final critique
            final_critique_file = os.path.join(chapter_output_dir, f'critique_chapter_{args.chapter_number:02d}_final.md')

            # Call the Critic bot to analyze the completed chapter!
            critic_command = [
                'python', os.path.join(PROJECT_ROOT, 'scripts', 'critic.py'),
                '--author-prompt-file', main_prompt_file,
                '--generated-file', final_chapter_file,
                '--output-file', final_critique_file,
                '--api-key', api_key
            ]
            
            if run_script(critic_command): #
                print("--- Final critique complete! Check artifacts for results. ---")
            else:
                print("--- CRITIC SCRIPT FAILED. Please check logs. ---")
        else:
            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"  FAILURE! Chapter generation did not complete all 5 parts.")
            print(f"  Check the artifacts in: {chapter_output_dir}")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        print("\n--- narrative engine shutdown ---")
    
    except Exception as e:
        print(f"\n--- A CRITICAL ERROR OCCURRED IN THE MAIN ENGINE! ---")
        print(f"Process halted. Please check the error messages above. Details: {e}")
        print("--- Conductor Engine Emergency Shutdown ---")


if __name__ == '__main__':
    main()