# conductor.py (v1.1 - The Grand Orchestrator - Calibrated)
# This is the master script that controls the entire chapter generation process.
# FIX: Now correctly assembles the prompt_string before passing it to the author.

import os
import argparse
import time

# Let's import the functions from our specialized bot scripts!
# We now need CORE_DIRECTIVES from the prompt_generator!
from prompt_generator import generate_story_beats_from_api, extract_chapter_summary, load_file_content, CORE_DIRECTIVES
from author import write_first_draft, edit_draft
from critic import critique_text
from archivist import summarize_events_from_text, append_events_to_log

# --- CONFIGURATION ---
MAX_CRITIC_REVIEWS = 3 # The maximum number of times a chapter part can be sent for edits.

# --- PATHING GPS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
KNOWLEDGE_DB_DIR = os.path.join(PROJECT_ROOT, "knowledge_db")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "generated_chapters")
PLOT_OUTLINE_FILE = os.path.join(KNOWLEDGE_DB_DIR, "rwby_novel_plot_outline.md")

# --- MAIN ORCHESTRATION ENGINE ---

def main():
    """The main function that orchestrates the entire chapter generation."""
    parser = argparse.ArgumentParser(description="The Grand Orchestrator: Generates a full chapter from start to finish.")
    parser.add_argument('--chapter-number', type=int, required=True, help='The number of the chapter to generate.')
    args = parser.parse_args()

    print(f"--- CONDUCTOR ONLINE: INITIATING GENERATION FOR CHAPTER {args.chapter_number} ---")
    
    chapter_output_dir = os.path.join(OUTPUT_DIR, f'chapter_{args.chapter_number:02d}')
    os.makedirs(chapter_output_dir, exist_ok=True)
    print(f"Output for Chapter {args.chapter_number} will be saved in: {chapter_output_dir}")

    full_chapter_text = []

    try:
        # --- STAGE 1: PLANNING ---
        print("\n--- [CONDUCTOR] Engaging Planner Bot ---")
        outline_text = load_file_content(PLOT_OUTLINE_FILE)
        chapter_summary = extract_chapter_summary(outline_text, args.chapter_number)
        planned_beats = generate_story_beats_from_api(chapter_summary)
        print("--- [CONDUCTOR] Planner Bot has delivered the 5-part plan! ---")

        # --- STAGE 2: GENERATION (Loop through all 5 parts) ---
        for i, beat_data in enumerate(planned_beats, 1):
            print(f"\n\n{'='*20} STARTING CHAPTER {args.chapter_number}, PART {i} OF 5 {'='*20}")
            
            # !!! THIS IS THE FIX !!!
            # We now assemble the full prompt string here inside the conductor.
            prompt_for_author = f"""
{CORE_DIRECTIVES}

---

### **PROMPT FOR CHAPTER {args.chapter_number}, PART {i}: {beat_data['title']}**

**Objective:** {beat_data['objective']}

**Crucial Ending Point:** {beat_data['ending_point']}
"""
            prompt_for_author = prompt_for_author.strip()
            
            current_prose = ""
            is_approved = False
            
            # This is the feedback loop!
            for attempt in range(MAX_CRITIC_REVIEWS + 1):
                if attempt == 0:
                    current_prose = write_first_draft(prompt_for_author)
                else:
                    print(f"--- [CONDUCTOR] Sending text back to Author for Edit Attempt #{attempt} ---")
                    current_prose = edit_draft(current_prose, critique_result, prompt_for_author)

                print(f"--- [CONDUCTOR] Text generated. Sending to Critic for review (Attempt {attempt + 1}/{MAX_CRITIC_REVIEWS + 1}) ---")
                
                time.sleep(5)

                critique_result = critique_text(
                    prose_text=current_prose,
                    original_prompt=prompt_for_author,
                    key_characters=beat_data['key_characters'],
                    key_locations=beat_data['key_locations']
                )

                if critique_result == "SUCCESS":
                    print(f"--- [CRITIC] SUCCESS! Chapter Part {i} has been approved! ---")
                    is_approved = True
                    break
                else:
                    print(f"--- [CRITIC] Edits required for Chapter Part {i}. Feedback: ---")
                    print(critique_result)
                    print("----------------------------------------------------------")

            # --- STAGE 3: APPROVAL & ARCHIVING ---
            if is_approved:
                print(f"\n--- [CONDUCTOR] Finalizing approved text for Part {i} ---")
                
                part_filename = os.path.join(chapter_output_dir, f'chapter_{args.chapter_number:02d}_part_{i}_approved.md')
                with open(part_filename, 'w', encoding='utf-8') as f:
                    f.write(current_prose)
                print(f"Saved approved text to: {os.path.basename(part_filename)}")

                full_chapter_text.append(current_prose)

                print("\n--- [CONDUCTOR] Engaging Archivist Bot ---")
                chapter_part_info = f"Chapter {args.chapter_number}, Part {i}"
                events_summary = summarize_events_from_text(current_prose, chapter_part_info)
                append_events_to_log(events_summary, chapter_part_info)
                print("--- [CONDUCTOR] Archivist has updated the official canon! ---")
            else:
                print(f"\n\n--- !!! CRITICAL FAILURE !!! ---")
                print(f"Chapter Part {i} failed to pass Critic review after {MAX_CRITIC_REVIEWS + 1} attempts.")
                print("Halting chapter generation to prevent further errors.")
                raise Exception(f"Failed to produce approved text for Chapter {args.chapter_number}, Part {i}.")

        # --- STAGE 4: FINALIZATION ---
        print(f"\n\n{'='*20} CHAPTER {args.chapter_number} GENERATION COMPLETE! {'='*20}")
        final_chapter_filename = os.path.join(chapter_output_dir, f'chapter_{args.chapter_number:02d}_complete.md')
        
        final_text = "\n\n---\n\n".join(full_chapter_text)

        with open(final_chapter_filename, 'w', encoding='utf-8') as f:
            f.write(final_text)
        
        print(f"Successfully generated and saved the complete Chapter {args.chapter_number} to:")
        print(final_chapter_filename)
        print("\n--- CONDUCTOR OFFLINE ---")

    except Exception as e:
        print(f"\n--- A CATASTROPHIC ERROR OCCURRED IN THE CONDUCTOR ---")
        print(f"Process halted. Details: {e}")
        print("--- CONDUCTOR EMERGENCY SHUTDOWN ---")

if __name__ == '__main__':
    main()