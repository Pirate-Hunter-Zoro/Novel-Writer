# prompt_generator.py (v9.0 - The Workspace Preparer!)
# This script prepares the entire workspace for a chapter part:
# 1. It creates the enhanced prompt file for Entrapta.
# 2. It creates the blank chapter file for Mikey to paste into.

import os
import argparse
import re

# --- GLOBAL CONFIGURATION & PATHING GPS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PROMPTS_DIR = os.path.join(PROJECT_ROOT, "knowledge_db", "rwby_chapter_prompts")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "generated_chapters")

ANTI_SUMMARY_WARNING = """

---
**CRITICAL PACING DIRECTIVE: Maintain deep 'show, don't tell' detail throughout the scene. A brief, reflective summary is only permitted in the final paragraph.**
---

"""

# --- HELPER FUNCTIONS ---

def load_file_content(file_path):
    """A generic function to load content from any text file."""
    print(f"Reading data from file: {file_path}")
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

def extract_five_part_prompts(chapter_file_text):
    """
    Parses a chapter prompt file to extract TWO things:
    1. The 'CORE DIRECTIVES' block.
    2. A list of the five sequential micro-prompts.
    """
    print(f"Parsing Chapter prompt for Core Directives and 5-part sequence...")
    core_directives_text = ""
    
    directives_start_marker = "### **CORE DIRECTIVES FOR SUPERIOR WRITING QUALITY"
    directives_end_pattern = re.compile(r'\n---\n\n### \*\*Prompt \d+-[A-E]:')
    
    start_idx = chapter_file_text.find(directives_start_marker)
    match = directives_end_pattern.search(chapter_file_text, start_idx)
    
    if start_idx != -1 and match:
        end_idx = match.start()
        core_directives_text = chapter_file_text[start_idx:end_idx].strip()
        print("Successfully extracted Core Directives.")
    else:
        print("WARNING: Could not extract the Core Directives block. The prompt will be less specific!")

    split_marker = r'### \*\*Prompt '
    parts = re.split(split_marker, chapter_file_text)
    if len(parts) < 2:
        print(f"ERROR: Could not find any prompts. Check for the '### **Prompt ' marker in your file.")
        return core_directives_text, []
    
    prompts = ["### **Prompt " + part.strip() for part in parts[1:]]
    print(f"Successfully parsed {len(prompts)} micro-prompts!")
    return core_directives_text, prompts

# --- MAIN ENGINE ---

def main():
    """The main function that prepares the prompt files for Entrapta."""
    parser = argparse.ArgumentParser(description="The Workspace Preparer: Creates all necessary files for a chapter part.")
    parser.add_argument('--chapter-number', type=int, required=True, help='The number of the chapter to generate prompts for.')
    args = parser.parse_args()

    print("--- Activating Workspace Preparer v9.0 ---")
    try:
        chapter_output_dir = os.path.join(OUTPUT_DIR, f'chapter_{args.chapter_number:02d}')
        os.makedirs(chapter_output_dir, exist_ok=True)
        print(f"All generated files for Chapter {args.chapter_number} will be saved in: {chapter_output_dir}")

        chapter_prompt_path = os.path.join(PROMPTS_DIR, f"chapter_{args.chapter_number}.md")
        all_prompts_text = load_file_content(chapter_prompt_path)
        
        core_directives, five_part_prompts = extract_five_part_prompts(all_prompts_text)

        if not five_part_prompts:
            raise Exception("No prompts were found. Halting.")

        for i, micro_prompt in enumerate(five_part_prompts, 1):
            print(f"\n--- Processing Part {i} ---")
            
            # --- Sub-routine 1: Enhance and create the prompt file ---
            ending_marker = "**Crucial Ending Point:**"
            if ending_marker in micro_prompt:
                parts = micro_prompt.split(ending_marker, 1)
                enhanced_micro_prompt = parts[0] + ANTI_SUMMARY_WARNING + ending_marker + parts[1]
            else:
                print(f"WARNING: '{ending_marker}' not found in Part {i}. Cannot inject warning.")
                enhanced_micro_prompt = micro_prompt

            finalized_prompt_text = core_directives + "\n\n---\n\n" + enhanced_micro_prompt
            prompt_part_file = os.path.join(chapter_output_dir, f'prompt_part_{i}.md')
            
            with open(prompt_part_file, 'w', encoding='utf-8') as f:
                f.write(finalized_prompt_text)
            print(f"Successfully created and enhanced: {os.path.basename(prompt_part_file)}")

            #! NEW FEATURE: Create the blank chapter part file!
            # It makes an empty file for you to paste my output into! No more manual work!
            chapter_part_file = os.path.join(chapter_output_dir, f'chapter_part_{i}.md')
            with open(chapter_part_file, 'w', encoding='utf-8') as f:
                pass # This just creates an empty file. So simple!
            print(f"Successfully created blank file: {os.path.basename(chapter_part_file)}")


        print("\n--- Workspace Preparation Complete! ---")
        print("The 5 prompt files and 5 blank chapter files are ready!")

    except Exception as e:
        print(f"\n--- A CRITICAL ERROR OCCURRED! ---")
        print(f"Process halted. Details: {e}")
        print("--- Workspace Preparer Emergency Shutdown ---")

if __name__ == '__main__':
    main()