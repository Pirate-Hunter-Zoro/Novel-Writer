import os
import argparse
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
import re

# --- GLOBAL CONFIGURATION & PATHING GPS ---
# This block makes our script location-independent!
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PROMPTS_DIR = os.path.join(PROJECT_ROOT, "knowledge_db", "rwby_chapter_prompts")
output_dir = os.path.join(PROJECT_ROOT, "output", "generated_chapters")


# --- RE-WRITER BOT'S BRAIN ---
REWRITER_SYSTEM_PROMPT_TEMPLATE = """
**SYSTEM COMMAND: You are the Prompt Re-writer LLM, an expert in prompt engineering and iterative refinement. Your sole function is to improve a failed prompt based on a critique.**

**Primary Objective:** You will be given an `[ORIGINAL_PROMPT]` and a `[CRITIQUE_REPORT]` that details its failures (e.g., word count, lore inconsistency, lack of detail). Your task is to generate a `[NEW_IMPROVED_PROMPT]`. This new prompt MUST be a complete, standalone set of instructions for the Author LLM.

**NON-NEGOTIABLE Directives:**
1.  **Analyze the Failures:** Read the `[CRITIQUE_REPORT]` carefully to understand exactly why the `[ORIGINAL_PROMPT]` failed.
2.  **Targeted Improvement:** Your `[NEW_IMPROVED_PROMPT]` must explicitly and aggressively target these failures. For example, if the word count was too low, the new prompt must emphasize a higher word count. If a character detail was wrong, the new prompt must provide the correct detail.
3.  **Do NOT Write the Story:** You are a prompt engineer, not a writer. Your output must ONLY be the new prompt text. Do not generate any story content.
4.  **Preserve the Objective:** The core creative objective of the `[ORIGINAL_PROMPT]` must be maintained. You are improving the prompt, not changing the fundamental goal of the scene.

---
### **[INPUT DATA STARTS NOW]**

**[ORIGINAL_PROMPT]**
{original_prompt}

**[CRITIQUE_REPORT]**
{critique_text}

---
### **[NEW_IMPROVED_PROMPT]**
(Begin your new, improved prompt now. Your output should start directly with the new prompt text.)
"""


# --- HELPER FUNCTIONS & BOT DEFINITIONS ---

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
        # To make sure our conductor knows a bot failed, we re-raise the exception!
        raise
    except FileNotFoundError as e:
        print(f"----- COMMAND FAILED -----")
        print(f"Error: Script not found. Make sure all scripts are in the 'scripts' directory.")
        raise

def load_file_content(file_path):
    """Loads content from a file."""
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
    core_directives_text = ""
    directives_start_marker = "### **CORE DIRECTIVES FOR SUPERIOR WRITING QUALITY"
    directives_end_marker = "\n---\n\n### **Prompt 1-A:"
    start_idx = chapter_file_text.find(directives_start_marker)
    end_idx = chapter_file_text.find(directives_end_marker, start_idx)
    if start_idx != -1 and end_idx != -1:
        core_directives_text = chapter_file_text[start_idx:end_idx].strip()
        print("Successfully extracted Core Directives.")
    else:
        print("WARNING: Could not extract the Core Directives block.")
    
    split_marker = r'### \*\*Prompt '
    parts = re.split(split_marker, chapter_file_text)
    if len(parts) < 2:
        print(f"ERROR: Could not find any prompts. Check for the '### **Prompt ' marker in your file.")
        return core_directives_text, []
    
    prompts = ["### **Prompt " + part.strip() for part in parts[1:]]
    print(f"Successfully parsed {len(prompts)} micro-prompts!")
    return core_directives_text, prompts

def rewrite_prompt_based_on_critique(original_prompt, critique_text, api_key):
    """
    Uses an LLM to rewrite a prompt based on a critique report.
    """
    print("Engaging the Prompt Re-writer bot...")
    rewriter_master_prompt = REWRITER_SYSTEM_PROMPT_TEMPLATE.format(
        original_prompt=original_prompt,
        critique_text=critique_text
    )
    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(rewriter_master_prompt)
        print("Re-writer has generated an improved prompt.")
        return response.text
    except Exception as e:
        print(f"ERROR: Prompt Re-writer failed. Details: {e}")
        return None


# --- MAIN ENGINE ---

def main():
    """The main function that runs the V5 generation and correction loop."""
    load_dotenv()
    parser = argparse.ArgumentParser(description="The Master Control Program for Novel Generation (V5).")
    parser.add_argument('--chapter-number', type=int, required=True, help='The number of the chapter to generate.')
    parser.add_argument('--max-iterations', type=int, default=3, help='Maximum number of correction loops per part.')
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in .env file!")
        return

    print("--- activating narrative engine v5.0 ---")
    try:
        configure_api(api_key)
        chapter_output_dir = os.path.join(output_dir, f'chapter_{args.chapter_number:02d}')
        os.makedirs(chapter_output_dir, exist_ok=True)
        print(f"All artifacts for this run will be saved in: {chapter_output_dir}")

        chapter_prompt_path = os.path.join(PROMPTS_DIR, f"chapter_{args.chapter_number}.md")
        all_prompts_text = load_file_content(chapter_prompt_path)
        core_directives, five_part_prompts = extract_five_part_prompts(all_prompts_text, args.chapter_number)

        if not five_part_prompts:
            raise Exception("Could not parse prompts. Aborting.")

        # --- STAGE 1: PARALLEL GENERATION ---
        print("\n--- STAGE 1: PARALLEL GENERATION ---")
        initial_generated_paths = []
        initial_prompt_paths = []
        for i, micro_prompt in enumerate(five_part_prompts, 1):
            print(f"\n--- Generating Part {i}/5 ---")
            finalized_prompt = core_directives + "\n\n" + micro_prompt
            prompt_part_file = os.path.join(chapter_output_dir, f'prompt_part_{i}_v1.md')
            chapter_part_file = os.path.join(chapter_output_dir, f'chapter_part_{i}_v1.md')
            with open(prompt_part_file, 'w', encoding='utf-8') as f: f.write(finalized_prompt)
            author_command = ['python', os.path.join(PROJECT_ROOT, 'scripts', 'author.py'), '--prompt-file', prompt_part_file, '--output-file', chapter_part_file, '--api-key', api_key]
            run_script(author_command)
            initial_generated_paths.append(chapter_part_file)
            initial_prompt_paths.append(prompt_part_file)
        print("\n--- STAGE 1 COMPLETE ---")


        # --- STAGE 2 & 3: PARALLEL CRITIQUE & CORRECTION LOOP ---
        print("\n--- STAGE 2 & 3: CORRECTION LOOP ---")
        final_passing_part_paths = [None] * len(initial_generated_paths)
        all_parts_perfected = True

        for i, initial_part_path in enumerate(initial_generated_paths):
            current_prompt_path = initial_prompt_paths[i]
            current_part_path = initial_part_path
            part_is_perfect = False

            for attempt in range(1, args.max_iterations + 1):
                print(f"\n--- Reviewing Part {i+1}, Attempt {attempt}/{args.max_iterations} ---")
                critique_path = os.path.join(chapter_output_dir, f'critique_part_{i+1}_v{attempt}.md')
                critic_command = ['python', os.path.join(PROJECT_ROOT, 'scripts', 'critic.py'), '--author-prompt-file', current_prompt_path, '--generated-file', current_part_path, '--output-file', critique_path, '--api-key', api_key]
                run_script(critic_command)
                
                critique_text = load_file_content(critique_path)
                if "FAIL" not in critique_text.upper():
                    print(f"SUCCESS: Part {i+1} passed critique!")
                    final_passing_part_paths[i] = current_part_path
                    part_is_perfect = True
                    break

                print(f"FAILURE DETECTED for Part {i+1}. Engaging Re-writer Bot...")
                if attempt == args.max_iterations:
                    print(f"MAX ATTEMPTS REACHED for Part {i+1}. This part has failed permanently.")
                    break
                
                original_prompt_text = load_file_content(current_prompt_path)
                new_prompt_text = rewrite_prompt_based_on_critique(original_prompt_text, critique_text, api_key)
                if not new_prompt_text:
                    print("Re-writer bot failed. Aborting this part.")
                    break
                
                # Setup for next attempt
                current_prompt_path = os.path.join(chapter_output_dir, f'prompt_part_{i+1}_v{attempt+1}.md')
                current_part_path = os.path.join(chapter_output_dir, f'chapter_part_{i+1}_v{attempt+1}.md')
                with open(current_prompt_path, 'w', encoding='utf-8') as f: f.write(new_prompt_text)
                
                author_command = ['python', os.path.join(PROJECT_ROOT, 'scripts', 'author.py'), '--prompt-file', current_prompt_path, '--output-file', current_part_path, '--api-key', api_key]
                run_script(author_command)

            if not part_is_perfect:
                all_parts_perfected = False
                break
        print("\n--- STAGE 2 & 3 COMPLETE ---")


        # --- STAGE 4: FINAL ASSEMBLY ---
        print("\n--- STAGE 4: FINAL ASSEMBLY ---")
        if all_parts_perfected:
            print("\nSUCCESS! All 5 parts have been perfected. Assembling final chapter...")
            final_chapter_file = os.path.join(chapter_output_dir, f'chapter_{args.chapter_number:02d}_complete.md')
            full_chapter_text = ""
            for part_path in final_passing_part_paths:
                part_content = load_file_content(part_path)
                full_chapter_text += part_content + "\n\n---\n\n"
            with open(final_chapter_file, 'w', encoding='utf-8') as f: f.write(full_chapter_text)
            print(f"\n--- V5 ENGINE RUN COMPLETE! VICTORY! Final chapter saved to: {final_chapter_file} ---")
        else:
            print("\n--- V5 ENGINE RUN FAILED. One or more parts could not be perfected. Final chapter not assembled. ---")

    except Exception as e:
        print(f"\n--- A CRITICAL ERROR OCCURRED IN THE MAIN ENGINE! ---")
        print(f"Process halted. Please check the error messages above. Details: {e}")
        print("--- Conductor Engine Emergency Shutdown ---")

if __name__ == '__main__':
    main()