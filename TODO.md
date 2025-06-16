# RWBY Novel Project - Session Summary (2025-06-15)

## I. Achievements of This Session:

This session has been incredibly productive, culminating in the foundational setup and a deep dive into our novel's structure:

* **Repository & Workflow Confirmed:** We solidified the Git repository setup and our collaborative workflow using Google Colab Pro and VS Code for editing.
* **"Knowledge Database" Completed:** We meticulously created and refined all four core "Knowledge Crystal" markdown files, which will be central to the Critic LLM's Vector RAG system:
    * `rwby_characters.md`: Populated with detailed profiles for all relevant characters, including a new, critical section for "Quirks/Mannerisms" to enhance character portrayal.
    * `rwby_locations.md`: Mapped out all crucial geographical and narrative settings across Remnant.
    * `rwby_lore_magic.md`: Documented the fundamental magical systems and concepts of the RWBY universe.
    * `rwby_plot_events.md`: Chronicled detailed, volume-by-volume plot summaries from Volume 1 through Volume 9, ensuring high accuracy and specific event descriptions (with key corrections on Neo's fate and Oscar/JN_R's return).
* **Comprehensive Plot Outline Developed:** We generated the `rwby_novel_plot_outline.md` file, a chapter-by-chapter blueprint for our 200,000-word novel across approximately 50 chapters. This outline:
    * Integrates all user-specified desired plot points and character interactions (e.g., Blake/Sun/Yang dynamic, Ren/Nora resolution, Neo's redemption arc, Summer Rose's fate).
    * Ensures intricate and major roles for key characters like Robyn Hill, Taiyang Xiao Long, and Raven Branwen.
    * Confirms Neo Politan and Emerald Sustrai's inclusion in the final seamless allied team.
    * Includes a specific `ILLUSTRATION_PROMPT` for the most epic moment in each chapter, for future image generation.
* **Chapter Prompt Manual Created:** We generated the `rwby_chapter_prompts.md` file, containing all the detailed, ready-to-use prompts for the Author LLM for every chapter.
* **README.md Updated:** The main project `README.md` was updated to reflect all current architectural details, file structure, and project goals.
* **Author LLM Setup & Debugging:**
    * Successfully set up the Google Colab Pro environment and loaded the `unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit` Author LLM.
    * Configured `HF_HOME` to manage model caching within the `vllm_models` directory.
    * Debugged and resolved `FileNotFoundError` related to Google Drive paths (`knowledge-db` vs `knowledge_db` typo).
    * Refined the prompt extraction logic to correctly parse and clean prompts from `rwby_chapter_prompts.md`, removing markdown code blocks and excess formatting.
    * Corrected `AttributeError` by properly accessing inputs as a dictionary.
    * Implemented robust output cleaning logic to remove prompt content and unwanted tags from the generated chapter text.
* **Initial Chapter Generation Attempt:** We attempted to generate Chapter 1. While the process worked, the output suffered from low writing quality (repetitive, generic), was unexpectedly short, and still had some formatting issues (incorrect headers).

## II. Next Steps (Picking Up Tomorrow):

Our immediate focus will be on improving the Author LLM's output quality for Chapter 1.

* **Refine Chapter 1 Prompt Content:** Manually update the Chapter 1 prompt within the `rwby_chapter_prompts.md` file with more explicit, detailed instructions for:
    * Vivid descriptions and immersive sensory details.
    * Deep emotional resonance for characters.
    * Avoiding repetitive phrasing or generic narrative.
    * Maintaining a sophisticated and engaging tone.
    * Crucially, instructing the LLM **not to stop writing** until the `[EPIC_MOMENT_END]` marker is placed and the chapter feels complete and reaches the requested length.
* **Adjust Generation Parameters:** In the Python script, slightly increase the `temperature` parameter in the `model.generate()` call from `0.8` to `0.95` to encourage more creative and less repetitive output.
* **Regenerate Chapter 1:** Run the script again to see the impact of these prompt and parameter changes on the generated chapter's quality and length.

# RWBY Novel Project - Session Summary (2025-06-16)

## I. Achievements & Key Decisions of This Session:

This session was incredibly productive, resolving key technical hurdles and re-strategizing for efficient novel generation:

* **Chapter 1 Prompt Refined:** The prompt for Chapter 1 was significantly enhanced with more explicit, detailed instructions for length, immersive sensory details, deep individual character resonance, "show, don't tell," varied language, and deliberate pacing.
* **Initial Chapter 1 Generation Attempts & Analysis:**
    * First attempt with the 8B model yielded initial success in prompting for individual character reactions and pacing, but lacked significant length and still showed some repetitive phrasing.
    * Attempted to scale up to the `Meta-Llama-3.1-70B-Instruct-bnb-4bit` model on an A100 GPU for full chapter generation.
* **Hardware Assessment & Resolution of Technical Issues:**
    * Initial `nvidia-smi` showed a Tesla T4 GPU (15GB VRAM), deemed insufficient for 70B single-pass generation.
    * Successfully switched Colab Pro runtime to an **NVIDIA A100-SXM4-40GB GPU (40GB VRAM)**, providing ample VRAM for a 70B model.
    * Encountered `OutOfMemoryError` during 70B generation, even on A100, indicating the model's base memory footprint plus generation buffer still exceeded VRAM for long outputs.
    * Encountered `RuntimeError` ("Expected all tensors to be on the same device, but found at least two devices, cpu and cuda:0!"). Resolved this by identifying the need to explicitly move input tensors to CUDA (and then identified that `model.to("cuda:0")` should NOT be used for bitsandbytes models).
* **Strategic Pivot to API-Driven Generation:**
    * Decided that, given the challenges with local Colab GPU limitations for large-scale, single-pass chapter generation, the most effective approach is to leverage my (Gemini's) direct capabilities via API calls.
    * This allows access to more powerful LLMs (like Gemini 1.5 Pro) and their internal context management, eliminating local hardware bottlenecks and streamlining the generation process.
* **My Role as Author & Critic Confirmed:** I (Gemini) will act as both the "Author LLM" (generating chapters from prompts) and the "Critic LLM" (reviewing chapters for consistency and providing feedback) via API calls. This creates an autonomous, self-correcting narrative engine.
* **Cost Analysis:** Initial estimates suggest the API calls for generating a 200,000-word novel (including retries and critiques with Gemini 1.5 Pro) would be well within the target budget of $10-$20 per month, likely much less.

## II. Next Steps (Picking Up Tomorrow):

Our immediate focus is to transition to the API-driven workflow and begin generating chapters directly:

1.  **Google Cloud Project & API Key Setup:** Mikey will set up a Google Cloud Project and enable the necessary Generative AI API (e.g., Vertex AI Gemini API or Google AI Studio API) to obtain an API key.
2.  **Install Python Client Library:** Mikey will install the appropriate Google AI Python client library (e.g., `google-generativeai`) on his local machine.
3.  **Develop Initial Orchestration Script:** Mikey will create a Python script to:
    * Manage the novel's chapter flow.
    * Load the `rwby_chapter_prompts.md` and Knowledge Database files.
    * Construct the augmented prompt for Chapter 1 using the detailed instructions and relevant context.
    * Send this prompt to me (via the API) for Chapter 1 generation.
    * Receive and save the generated Chapter 1 text to a markdown file.
4.  **Implement Critic Loop (Initial):** After Chapter 1 generation, the script will then construct a new prompt for me to act as the Critic, providing the generated chapter and relevant context for review. This will serve as a manual review point for Mikey initially, before potential automation.
5.  **Monitor API Costs:** Mikey will continuously monitor API token consumption to stay within the budget.