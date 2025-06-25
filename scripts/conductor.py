import os
import argparse
import subprocess
import time
import re
import tempfile #! NEW IMPORT for our clean room!

# --- GLOBAL CONFIGURATION & PATHING GPS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "generated_chapters")

# --- CONFIGURATION FOR THE FEEDBACK LOOP ---
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5
FAILURE_KEYWORDS = ["FAIL", "Inconsistency Detected", "ABSENT", "Contradiction", "Failure Report"]

def run_script(command):
    """A standardized function to run our other python bots."""
    print(f"\n>>>> [CONDUCTOR] EXECUTING COMMAND: {command}")
    try:
        # We need to see the output to debug, so we capture it.
        result = subprocess.run(command, check=True, shell=True, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print("---- STDERR ----")
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"!!!! [CONDUCTOR] ERROR running command: {command}")
        print(f"!!!! [CONDUCTOR] STDOUT: {e.stdout}")
        print(f"!!!! [CONDUCTOR] STDERR: {e.stderr}")
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
                print(f">>>> [CONDUCTOR] ANALYSIS: Failure keyword '{keyword}' found. Initiating correction loop.")
                return True
        
        print(">>>> [CONDUCTOR] ANALYSIS: No failure keywords found. Part approved!")
        return False
    except FileNotFoundError:
        print("!!!! [CONDUCTOR] Critique file not found! Assuming failure.")
        return True
    except Exception as e:
        print(f"!!!! [CONDUCTOR] Error reading critique file: {e}")
        return True

def process_critique_feedback(critique_file_path):
    """
    Reads the critique file and extracts TWO things:
    1. The full, original failure text for context.
    2. A specific list of 'NEGATIVE_CONSTRAINT' directives for the new prompt.
    Returns a dictionary: {'full_text': str, 'constraints': list}
    """
    print(">>>> [CONDUCTOR] Activating Feedback Processor...")
    try:
        with open(critique_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        constraints = re.findall(r'NEGATIVE_CONSTRAINT: (.*)', content)
        failures_match = re.search(r'(FAILURES:|FAILURE REPORT|FAIL\.)(.*)', content, re.DOTALL | re.IGNORECASE)
        failure_text = failures_match.group(2).strip() if failures_match else "General failure detected. Please review and improve the entire text."
        
        if constraints:
            print(f">>>> [CONDUCTOR] Extracted {len(constraints)} specific guardrail directives!")
        else:
            print(">>>> [CONDUCTOR] No specific guardrail directives found. Using general feedback.")

        return {'full_text': failure_text, 'constraints': constraints}
            
    except Exception as e:
        print(f"!!!! [CONDUCTOR] Could not extract feedback details: {e}")
        return {'full_text': "Error reading critique file.", 'constraints': []}

def main():
    parser = argparse.ArgumentParser(description="The Conductor Script (v3.1): Perfected Clean Room MCP.")
    parser.add_argument('--chapter-number', type=int, required=True, help='The chapter number to fully generate and critique.')
    args = parser.parse_args()
    
    chapter_num = args.chapter_number
    
    print("="*50)
    print("      ACTIVATING THE CONDUCTOR v3.1 (w/ Perfected Feedback Loop!)")
    print("="*50)

    if not run_script(f"python scripts/prompt_generator.py --chapter-number {chapter_num}"):
        print("!!!! [CONDUCTOR] CRITICAL FAILURE: Could not generate prompts. Shutting down.")
        return

    for part_num in range(1, 6):
        print(f"\n{'='*20} Starting Generation for Chapter {chapter_num}, Part {part_num} {'='*20}")
        
        retries = 0
        is_successful = False
        prompt_file_for_author = os.path.join(OUTPUT_DIR, f'chapter_{chapter_num:02d}', f'prompt_part_{part_num}.md')
        
        with open(prompt_file_for_author, 'r', encoding='utf-8') as f:
            original_prompt_text = f.read()

        current_author_prompt_text = original_prompt_text

        while retries < MAX_RETRIES and not is_successful:
            # Write the current prompt for the author to use
            with open(prompt_file_for_author, 'w', encoding='utf-8') as f:
                f.write(current_author_prompt_text)

            if not run_script(f"python scripts/author.py --chapter-number {chapter_num} --part-number {part_num}"):
                print("!!!! [CONDUCTOR] Author script failed. Breaking retry loop for this part.")
                break

            # ! THE CLEAN ROOM TECHNIQUE !
            # We create a temporary, clean prompt file for the Critic that contains ONLY the original prompt.
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.md', encoding='utf-8') as temp_prompt_for_critic:
                temp_prompt_for_critic.write(original_prompt_text)
                temp_prompt_file_path = temp_prompt_for_critic.name
            
            # The critic script needs to be modified to accept a prompt path argument.
            # For now, we will just manually create the command.
            # This is a conceptual change. Let's assume critic can take a prompt path.
            # The ideal way is to modify critic.py to take an optional prompt path.
            # Since we can't do that now, we will overwrite the main prompt file before critic runs
            # and restore it after. This is less clean, but works with the current critic script.
            
            # OVERWRITE the prompt file with the original for the critic
            with open(prompt_file_for_author, 'w', encoding='utf-8') as f:
                f.write(original_prompt_text)

            if not run_script(f"python scripts/critic.py --chapter-number {chapter_num} --part-number {part_num}"):
                print("!!!! [CONDUCTOR] Critic script failed. Breaking retry loop for this part.")
                # Restore the prompt before breaking
                with open(prompt_file_for_author, 'w', encoding='utf-8') as f:
                    f.write(current_author_prompt_text)
                break

            critique_file = os.path.join(OUTPUT_DIR, f'chapter_{chapter_num:02d}', f'critique_part_{part_num}.md')
            if not check_critique_for_failure(critique_file):
                is_successful = True
            else:
                retries += 1
                if retries < MAX_RETRIES:
                    feedback = process_critique_feedback(critique_file)
                    guardrail_section = ""
                    if feedback['constraints']:
                        guardrail_directives = "\n".join([f"- {c}" for c in feedback['constraints']])
                        guardrail_section = f"""---
**! CRITICAL DIRECTIVES ENGAGED !**
Your previous attempt generated multiple inconsistencies. To proceed, you MUST strictly adhere to the following hard-coded constraints. Violation of these rules WILL result in immediate failure.

{guardrail_directives}
---
"""
                    
                    current_author_prompt_text = f"""{guardrail_section}
**PREVIOUS FAILURE REPORT (FOR CONTEXT):**
{feedback['full_text']}

---
Regenerate the text for the original prompt below, ensuring you incorporate all fixes.

**Original Prompt:**
{original_prompt_text}
"""
                    print(">>>> [CONDUCTOR] Prompt has been upgraded with dynamic guardrails for the next attempt!")

        # Restore the original prompt file to its clean state for the next part
        with open(prompt_file_for_author, 'w', encoding='utf-8') as f:
            f.write(original_prompt_text)
        print(f">>>> [CONDUCTOR] Original prompt for Part {part_num} has been restored.")

        if is_successful:
            print(f"SUCCESS! Chapter {chapter_num}, Part {part_num} has passed all quality checks.")
        else:
            print(f"FAILURE! Chapter {chapter_num}, Part {part_num} failed all {retries} attempts.")
            print("         Manual intervention may be required for this part.")

    print("\n\n" + "="*50)
    print(f"      CONDUCTOR: All tasks for Chapter {chapter_num} are complete.")
    print("="*50)

if __name__ == '__main__':
    main()
