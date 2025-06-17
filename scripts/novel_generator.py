import google.generativeai as genai
import os
import re

# --- Configuration ---
# Your API key should be loaded from an environment variable for security!
# You should have set this like: export GOOGLE_API_KEY="YOUR_API_KEY_HERE" (Linux/macOS)
# or set GOOGLE_API_KEY="YOUR_API_KEY_HERE" (Windows)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set it before running the script.")
    print("e.g., export GOOGLE_API_KEY='YOUR_KEY_HERE'")
    exit()

genai.configure(api_key=GOOGLE_API_KEY)

# --- Model Initialization ---
model = genai.GenerativeModel('gemini-1.5-pro')

# --- File Paths ---
# Get the directory where the current script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Now build paths relative to the script's directory
KNOWLEDGE_DB_PATH = os.path.join(SCRIPT_DIR, "../knowledge_db/")
CHAPTER_PROMPTS_FILE = os.path.join(KNOWLEDGE_DB_PATH, "rwby_chapter_prompts.md")
OUTPUT_CHAPTERS_PATH = os.path.join(SCRIPT_DIR, "../output/generated_chapters/") # Ensure output path is also relative to script

# Ensure output directory exists (using exist_ok=True is good!)
os.makedirs(OUTPUT_CHAPTERS_PATH, exist_ok=True)

# --- Function to Load Knowledge Database Files ---
def load_knowledge_db(path):
    knowledge = {}
    # Use os.path.abspath to resolve the path before listing
    # This helps with relative paths if the script's current directory is different from execution
    full_path = os.path.abspath(path)
    if not os.path.exists(full_path):
        print(f"Error: Knowledge database path does not exist: {full_path}")
        return {} # Return empty to prevent further errors

    for filename in os.listdir(full_path): # Use full_path here
        if filename.endswith(".md") and filename != "rwby_chapter_prompts.md":
            filepath = os.path.join(full_path, filename) # Use full_path here
            with open(filepath, 'r', encoding='utf-8') as f:
                knowledge[filename.replace('.md', '')] = f.read()
    return knowledge

# --- Function to Extract a Specific Chapter Prompt ---
# --- Function to Extract a Specific Chapter Prompt ---
def extract_chapter_prompt(chapter_number, prompts_file):
    # Use os.path.abspath to resolve the path before opening
    full_prompts_file_path = os.path.abspath(prompts_file)
    if not os.path.exists(full_prompts_file_path):
        print(f"Error: Chapter prompts file does not exist: {full_prompts_file_path}")
        return None

    with open(full_prompts_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # MODIFIED REGEX HERE:
    # This regex now looks for '## Chapter N', then *optionally* any text on the same line (like "Prompt: Title"),
    # then any number of non-greedy characters (including newlines) until the next chapter header or end of file.
    # It also handles optional initial blank lines and the markdown code block.
    # We will then clean up the leading markdown elements *after* extraction.
    pattern = re.compile(rf'## Chapter {chapter_number}(?:[^\n]*)\n(.*?)(?=\n## Chapter \d+|\Z)', re.DOTALL)
    match = pattern.search(content)

    if match:
        raw_prompt = match.group(1).strip()
        # Clean up: remove the initial markdown code block (```python, ```markdown, etc.)
        # and any leading blank lines or "Prompt: Title" line if it wasn't caught by the regex.
        # This is a more aggressive cleanup to ensure only the core instructions remain.
        clean_prompt = re.sub(r'^\s*```[a-zA-Z]*\n', '', raw_prompt, flags=re.DOTALL | re.MULTILINE)
        clean_prompt = re.sub(r'^\s*Prompt:.*?\n', '', clean_prompt, flags=re.DOTALL | re.MULTILINE) # remove the "Prompt: Title" line if it sneaks through
        clean_prompt = clean_prompt.strip() # Re-trim after removing code blocks and title line
        return clean_prompt
    else:
        return None

# --- Main Orchestration Logic ---
def generate_novel_chapter(chapter_num):
    print(f"Initiating generation for Chapter {chapter_num}...")

    # Load all knowledge database files
    knowledge_data = load_knowledge_db(KNOWLEDGE_DB_PATH)
    if not knowledge_data: # Check if knowledge data was loaded successfully
        print("Aborting chapter generation due to missing knowledge database.")
        return
    print("Knowledge Database loaded!")

    # Extract the specific prompt for this chapter
    chapter_prompt_content = extract_chapter_prompt(chapter_num, CHAPTER_PROMPTS_FILE)

    if not chapter_prompt_content:
        print(f"Error: Could not find prompt for Chapter {chapter_num} in {CHAPTER_PROMPTS_FILE}")
        return

    print(f"Chapter {chapter_num} prompt extracted.")

    # Construct the full prompt for the LLM (rest of the prompt is unchanged)
    full_prompt = f"""
    You are an expert novelist tasked with writing a chapter for a RWBY fanfiction novel.
    Your goal is to write a compelling, vivid, and emotionally resonant chapter that
    adheres strictly to the RWBY lore, character personalities, and plot points
    provided in the "Knowledge Database" and the specific chapter prompt.

    ---
    ### CRITICAL INSTRUCTIONS FOR WRITING:
    1.  **Immersive & Sensory Detail:** Focus on "show, don't tell." Describe environments, actions, and character emotions with rich sensory details (sights, sounds, smells, feelings). Make the reader feel like they are *there*.
    2.  **Deep Character Resonance:** Ensure each character's dialogue, actions, and internal thoughts are true to their established personality, quirks, and emotional state as defined in `rwby_characters.md`. Convey their inner turmoil, motivations, and relationships accurately.
    3.  **Varied Language & Pacing:** Use a wide range of vocabulary and sentence structures. Vary the pacing – quick, sharp sentences for action; longer, flowing sentences for description or introspection. Avoid repetition in phrasing or narrative structure.
    4.  **Sophisticated Tone:** Maintain a sophisticated, engaging, and mature tone consistent with the RWBY series (Volumes 4-9 particularly). Avoid generic or simplistic prose.
    5.  **Length & Completeness:** Write a substantial chapter, aiming for a length that feels complete and impactful for a single chapter (e.g., 2000-4000 words). **DO NOT STOP WRITING** until the entire narrative for the chapter is complete and the `[EPIC_MOMENT_END]` marker (if present in the prompt) is reached and passed. If there is an `ILLUSTRATION_PROMPT`, ensure the scene it describes is fully detailed within the chapter.
    6.  **Formatting:** Use standard novel formatting (paragraphs, dialogue with quotation marks). Do NOT include markdown headers within the chapter text itself (e.g., "## Chapter 1"). The only header should be the initial "Chapter X" in the markdown file output.
    7.  **NO META-COMMENTARY:** Do not explain that you are an AI, or mention instructions or internal thoughts. Just write the novel text.
    ---

    ### Knowledge Database for Context:
    Here is critical background information about the RWBY universe, characters, lore, and plot events to ensure accuracy and consistency:

    #### rwby_characters.md:
    {knowledge_data.get('rwby_characters', 'Character data not found.')}

    #### rwby_locations.md:
    {knowledge_data.get('rwby_locations', 'Location data not found.')}

    #### rwby_lore_magic.md:
    {knowledge_data.get('rwby_lore_magic', 'Lore and Magic data not found.')}

    #### rwby_plot_events.md:
    {knowledge_data.get('rwby_plot_events', 'Plot Events data not found.')}

    ---
    ### Specific Instructions for This Chapter (Chapter {chapter_num}):
    {chapter_prompt_content}

    ---
    Begin Chapter {chapter_num} of the RWBY novel now.
    """

    print("Sending prompt to Gemini 1.5 Pro...")
    # Generate the content!
    response = model.generate_content(
        full_prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.95,
            max_output_tokens=4000
        )
    )

    generated_text = ""
    try:
        generated_text = response.text
        if full_prompt in generated_text:
            generated_text = generated_text.replace(full_prompt, "", 1).strip()
        generated_text = generated_text.replace("[EPIC_MOMENT_END]", "").strip()

    except ValueError:
        print("Error: No text generated. Possible content safety block or empty response.")
        if response.prompt_feedback:
            print(f"Prompt feedback: {response.prompt_feedback}")
        if response.candidates:
            for candidate in response.candidates:
                if candidate.finish_reason:
                    print(f"Finish reason: {candidate.finish_reason}")
                if candidate.safety_ratings:
                    print(f"Safety ratings: {candidate.safety_ratings}")
        return

    # Save the generated chapter
    output_filename = os.path.join(OUTPUT_CHAPTERS_PATH, f"Chapter_{chapter_num}.md")
    # Ensure the output directory exists before writing
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# Chapter {chapter_num}\n\n")
        f.write(generated_text)

    print(f"Chapter {chapter_num} generated and saved to {output_filename}")
    print("\n--- BEGIN CHAPTER PREVIEW ---\n")
    print(generated_text[:1000] + "...\n" if len(generated_text) > 1000 else generated_text)
    print("\n--- END CHAPTER PREVIEW ---\n")


# --- Execute the Generation ---
if __name__ == "__main__":
    generate_novel_chapter(1)