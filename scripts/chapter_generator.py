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
    Parses a chapter prompt file to extract TWO things:
    1. The 'CORE DIRECTIVES' block.
    2. A list of the five sequential micro-prompts.
    """
    print(f"Parsing Chapter {chapter_number} for Core Directives and 5-part sequence...")

    # --- NEW PART 1: Extract the Core Directives ---
    core_directives_text = ""
    directives_start_marker = "### **CORE DIRECTIVES FOR SUPERIOR WRITING QUALITY"
    # The directives end where the first prompt begins, marked by '---'
    directives_end_marker = "\n---\n\n### **Prompt 1-A:"

    start_idx = chapter_file_text.find(directives_start_marker)
    end_idx = chapter_file_text.find(directives_end_marker, start_idx)

    if start_idx != -1 and end_idx != -1:
        core_directives_text = chapter_file_text[start_idx:end_idx].strip()
        print("Successfully extracted Core Directives.")
    else:
        print("WARNING: Could not extract the Core Directives block.")


    # --- PART 2: Extract the five micro-prompts (our existing logic) ---
    split_marker = r'### \*\*Prompt '
    parts = re.split(split_marker, chapter_file_text)

    if len(parts) < 2:
        print(f"ERROR: Could not find any prompts. Check for the '### **Prompt ' marker in your file.")
        return core_directives_text, [] # Return directives even if prompts fail

    prompts = []
    for part in parts[1:]:
        full_prompt = "### **Prompt " + part.strip()
        prompts.append(full_prompt)

    if len(prompts) < 5:
        print(f"WARNING: Found {len(prompts)} micro-prompts for Chapter {chapter_number}, expected 5.")
    else:
        print(f"Successfully parsed {len(prompts)} micro-prompts!")
        
    return core_directives_text, prompts

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
            
        core_directives, five_part_prompts = extract_five_part_prompts(all_prompts_text, args.chapter_number)

        if not five_part_prompts:
            print(f"Could not parse the 5-part prompt for Chapter {args.chapter_number}. Aborting!")
            return

        # Lists to hold the paths to all our new little files! So organized!
        generated_part_paths = []
        prompt_part_paths = []
        all_parts_succeeded = True

        # The new "Divide and Conquer" loop!
        for i, micro_prompt in enumerate(five_part_prompts, 1):
            print(f"\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print(f"  GENERATING PART {i}/5 for Chapter {args.chapter_number}")
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

            # We need to re-inject the core directives for each individual part.
            # This ensures each generation task has the full set of rules.
            finalized_prompt = core_directives + "\n\n" + micro_prompt

            # Define unique file names for each part's prompt and generated text
            prompt_part_file = os.path.join(chapter_output_dir, f'prompt_part_{i}.md')
            chapter_part_file = os.path.join(chapter_output_dir, f'chapter_part_{i}.md')

            print(f"Saving focused prompt for part {i} to {prompt_part_file}")
            with open(prompt_part_file, 'w', encoding='utf-8') as f:
                f.write(finalized_prompt)

            # Call the Author bot to write just this one, focused piece!
            author_command = ['python', os.path.join(PROJECT_ROOT, 'scripts', 'author.py'), '--prompt-file', prompt_part_file, '--output-file', chapter_part_file, '--api-key', api_key]
            
            if run_script(author_command):
                # The part was generated successfully! Let's save the paths.
                generated_part_paths.append(chapter_part_file)
                prompt_part_paths.append(prompt_part_file)
            else:
                # A part failed! We have to stop.
                print(f"Author script failed on part {i}. Halting generation process.")
                all_parts_succeeded = False
                break

        if all_parts_succeeded:
            print("\n**************************************")
            print(f"  SUCCESS! All 5 individual parts of Chapter {args.chapter_number} generated!")
            print("  Next step: Parallel Critique.")
            print("**************************************")
            
            print("\n--- INITIATING PARALLEL CRITIQUE ---")
            critique_part_paths = []
            all_critiques_succeeded = True

            # A new loop! It iterates through each part we generated.
            for i, chapter_part_path in enumerate(generated_part_paths, 1):
                print(f"\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                print(f"  CRITIQUING PART {i}/5 for Chapter {args.chapter_number}")
                print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")

                # The prompt that CREATED this part.
                prompt_part_path = prompt_part_paths[i-1] 
                # The file where we'll save this part's critique.
                critique_part_file = os.path.join(chapter_output_dir, f'critique_part_{i}.md')

                # Build the command to critique just this one part!
                critic_command = [
                    'python', os.path.join(PROJECT_ROOT, 'scripts', 'critic.py'),
                    '--author-prompt-file', prompt_part_path,
                    '--generated-file', chapter_part_path,
                    '--output-file', critique_part_file,
                    '--api-key', api_key
                ]
                
                if run_script(critic_command):
                    critique_part_paths.append(critique_part_file)
                else:
                    print(f"CRITIC FAILED on part {i}. Halting critique process.")
                    all_critiques_succeeded = False
                    break

            if all_critiques_succeeded:
                print("\n**************************************")
                print(f"  SUCCESS! All 5 parts of Chapter {args.chapter_number} have been individually critiqued!")
                print("**************************************")
                
                print("\n--- INITIATING FINAL REVIEW & ASSEMBLY ---")
                all_parts_passed_critique = True
                
                # This loop reads every critique report!
                for critique_path in critique_part_paths:
                    print(f"Reading critique file: {critique_path}")
                    critique_text = load_file_content(critique_path)
                    # We're scanning for any sign of failure!
                    if "FAIL" in critique_text.upper():
                        print(f"FAILURE DETECTED in {critique_path}. Halting assembly.")
                        all_parts_passed_critique = False
                        break # No need to check the others if one failed!

                # This is the final decision!
                if all_parts_passed_critique:
                    print("\n**************************************")
                    print("  SUCCESS! All 5 parts passed individual critique!")
                    print("  Beginning final chapter assembly...")
                    print("**************************************")

                    # --- THE FINAL STITCHING MECHANISM ---
                    final_chapter_file = os.path.join(chapter_output_dir, f'chapter_{args.chapter_number:02d}_complete.md')
                    full_chapter_text = ""

                    for part_path in generated_part_paths:
                        part_content = load_file_content(part_path)
                        full_chapter_text += part_content + "\n\n---\n\n"

                    print(f"Saving final, assembled chapter to: {final_chapter_file}")
                    with open(final_chapter_file, 'w', encoding='utf-8') as f:
                        f.write(full_chapter_text)
                    
                    print("\n--- V4 ENGINE RUN COMPLETE! VICTORY! ---")

                else:
                    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("  FAILURE! One or more parts failed critique.")
                    print("  Final chapter will NOT be assembled. Check individual critique files for details.")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                
        else:
            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"  FAILURE! Chapter generation did not complete all 5 parts.")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


        print("\n--- narrative engine shutdown ---")
    
    except Exception as e:
        print(f"\n--- A CRITICAL ERROR OCCURRED IN THE MAIN ENGINE! ---")
        print(f"Process halted. Please check the error messages above. Details: {e}")
        print("--- Conductor Engine Emergency Shutdown ---")


if __name__ == '__main__':
    main()