# conductor.py (v1.0 - The Master Control Program)
# This script orchestrates the entire chapter generation process, including
# a self-correcting feedback loop between the Author and the Critic.

import os
import argparse
import subprocess
import time

# --- GLOBAL CONFIGURATION & PATHING GPS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "generated_chapters")

# --- CONFIGURATION FOR THE FEEDBACK LOOP ---
MAX_RETRIES = 3 # A safety valve to prevent infinite loops!
RETRY_DELAY_SECONDS = 5 # A small delay to avoid spamming the API.
# Keywords that indicate the critic has failed the text. So simple!
FAILURE_KEYWORDS = ["FAIL", "Inconsistency Detected", "ABSENT", "Contradiction", "Failure Report"]

def run_script(command):
    """A standardized function to run our other python bots."""
    print(f"\n>>>> [CONDUCTOR] EXECUTING COMMAND: {command}")
    try:
        # We use subprocess to call our other scripts like command-line tools
        subprocess.run(command, check=True, shell=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"!!!! [CONDUCTOR] ERROR running command: {command}")
        print(f"!!!! [CONDUCTOR] Error details: {e}")
        return False
    except Exception as e:
        print(f"!!!! [CONDUCTOR] An unexpected error occurred: {e}")
        return False

def check_critique_for_failure(critique_file_path):
    """Reads the critique file and returns True if failure keywords are found."""
    print(f">>>> [CONDUCTOR] Analyzing critique file: {os.path.basename(critique_file_path)}")
    try:
        with open(critique_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for keyword in FAILURE_KEYWORDS:
            if keyword in content:
                print(f">>>> [CONDUCTOR] ANALYSIS: Failure keyword '{keyword}' found. Retrying.")
                return True # Failure detected
        
        print(">>>> [CONDUCTOR] ANALYSIS: No failure keywords found. Part approved!")
        return False # Success!
    except FileNotFoundError:
        print("!!!! [CONDUCTOR] Critique file not found! Assuming failure.")
        return True # If the file doesn't exist, something went wrong.
    except Exception as e:
        print(f"!!!! [CONDUCTOR] Error reading critique file: {e}")
        return True

def main():
    parser = argparse.ArgumentParser(description="The Conductor Script (v1.0): The Master Control Program.")
    parser.add_argument('--chapter-number', type=int, required=True, help='The chapter number to fully generate and critique.')
    args = parser.parse_args()
    
    chapter_num = args.chapter_number
    
    print("="*50)
    print("      ACTIVATING THE CONDUCTOR MASTER CONTROL PROGRAM")
    print("="*50)

    # --- STEP 1: PREPARE THE ENTIRE WORKSPACE ---
    # We only need to do this once for the whole chapter.
    if not run_script(f"python scripts/prompt_generator.py --chapter-number {chapter_num}"):
        print("!!!! [CONDUCTOR] CRITICAL FAILURE: Could not generate prompts. Shutting down.")
        return

    # --- STEP 2: LOOP THROUGH ALL 5 PARTS OF THE CHAPTER ---
    for part_num in range(1, 6):
        print(f"\n{'='*20} Starting Generation for Chapter {chapter_num}, Part {part_num} {'='*20}")
        
        retries = 0
        is_successful = False
        
        # --- STEP 3: THE GENERATE-AND-CRITIQUE FEEDBACK LOOP ---
        while retries < MAX_RETRIES and not is_successful:
            if retries > 0:
                print(f">>>> [CONDUCTOR] This is RETRY attempt {retries} of {MAX_RETRIES-1}.")
                # In a more advanced system, we would modify the prompt here with the critique feedback!
                # For now, we just retry, hoping for a better random seed.
                time.sleep(RETRY_DELAY_SECONDS)

            # Generate the text
            if not run_script(f"python scripts/author.py --chapter-number {chapter_num} --part-number {part_num}"):
                print("!!!! [CONDUCTOR] Author script failed. Skipping to next part.")
                break # Break the while loop if author fails catastrophically

            # Critique the text
            if not run_script(f"python scripts/critic.py --chapter-number {chapter_num} --part-number {part_num}"):
                print("!!!! [CONDUCTOR] Critic script failed. Skipping to next part.")
                break # Break the while loop if critic fails catastrophically

            # Check the result
            critique_file = os.path.join(OUTPUT_DIR, f'chapter_{chapter_num:02d}', f'critique_part_{part_num}.md')
            if not check_critique_for_failure(critique_file):
                is_successful = True # The part is good!
            else:
                retries += 1
        
        if is_successful:
            print(f"SUCCESS! Chapter {chapter_num}, Part {part_num} has passed all quality checks.")
        else:
            print(f"FAILURE! Chapter {chapter_num}, Part {part_num} failed all {MAX_RETRIES} retry attempts.")
            print("         Manual intervention may be required for this part.")

    print("\n\n" + "="*50)
    print(f"      CONDUCTOR: All tasks for Chapter {chapter_num} are complete.")
    print("="*50)

if __name__ == '__main__':
    main()