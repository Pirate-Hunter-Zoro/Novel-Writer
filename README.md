# RWBY Novel Project: The Fully Automated Narrative Pipeline (v3.0)

## Project Overview

This project leverages a sophisticated, AI-assisted architecture to generate a full-length, 200,000-word novel set in the RWBY universe. The narrative picks up directly after Team RWBYJ departs the Ever After, providing a comprehensive and conclusive resolution to the entire RWBY universe's conflict with Salem. The system has evolved into a highly efficient, automated pipeline, where a human Conductor (Mikey) orchestrates a powerful Python Bot Army to generate and refine narrative content.

### Key Goals

- Generate approximately 200,000 words of novel content, distributed across 50 chapters.
- Achieve a comprehensive and conclusive resolution to Salem's storyline.
- Generate high-quality, character-consistent illustrations for each chapter part using a custom-trained LoRA (Low-Rank Adaptation) model.
- Produce output in Markdown format, with a future goal of combining text and images into a rich `.epub`.
- Pave the way for a potential future She-Ra and RWBY crossover novel!

## Architecture: The Human-in-the-Loop Collaborative Engine

The project's architecture is orchestrated by the human Conductor, who manages the toolset and performs final quality assurance.

### 1. The Conductor (Mikey)

- **Role:** The Master Control Program, Lead Engineer, and Data Archivist. The Conductor initiates the automated pipeline, manages the toolset, provides high-level creative direction, curates training data, and performs final quality assurance on both text and images.

### 2. The Author & Visualizer (Entrapta)

- **Role:** The primary creative core.
  - As **Author**, my generative capabilities are now integrated into the automated `author.py` and `conductor.py` scripts.
  - As **Visualizer**, I generate illustrations based on refined prompts, using custom LoRA modules to ensure character consistency.
  - As **Lead Critic**, I can provide "Tier 2" subjective analysis on generated images.

### 3. The Python Bot Army (The Scripts)

- **The Conductor (`conductor.py`):** The new **Master Control Program!** This high-level script automates the entire narrative generation and critique loop for a full chapter.
- **The Prompt Generator (`prompt_generator.py`):** An automated "Instruction Injector" that enhances simple chapter prompts and prepares the workspace.
- **The Author (`author.py`):** The new **Automated Narrative Engine** that takes a prepared prompt and generates the creative text.
- **The Text Critic (`critic.py`):** The "Wise Critic" that analyzes generated text against a ruleset and the Knowledge Database.
- **The Auto-Tagger (`auto_captioner.py`):** An API-powered bot that processes the local image database and automatically generates keyword captions for LoRA training.

## Knowledge Databases ("Knowledge Crystals")

The system relies on two forms of knowledge databases to ensure consistency.

### 1. Narrative Knowledge Database

- `rwby_characters.md`, `rwby_locations.md`, `rwby_lore_magic.md`, `rwby_plot_events.md`: Meticulously organized Markdown files providing comprehensive RWBY lore.

### 2. Visual Knowledge Database (For Project LoRA)

- **`training_images/`**: A critical directory containing a curated database of 15-20 reference images for each key character, used to train our LoRA models.

## Current Workflow: The Automated Multimedia Pipeline

The project now operates via a two-phase pipeline: an automated narrative phase followed by a collaborative visual phase.

1.  **Phase 1: Automated Narrative Generation**
    - The Conductor executes a single command: `python scripts/conductor.py --chapter-number X`.
    - The `conductor.py` script takes full control:
        - It first runs `prompt_generator.py` to prepare the workspace.
        - For each of the five parts of the chapter, it enters a self-correcting loop:
            1.  It calls `author.py` to generate the text.
            2.  It calls `critic.py` to analyze the text.
            3.  If the critique passes, it moves to the next part. If it fails, it re-runs the loop with feedback until quality checks are passed or max retries are hit.

2.  **Phase 2: Collaborative Visual Loop**
    - This loop remains a manual, collaborative process for now.
    - The Conductor and Author collaborate to refine the `ILLUSTRATION_PROMPT` for the finalized text.
    - The Author (as Visualizer) generates an image using the appropriate LoRA module.
    - The Conductor performs quality checks, and the loop repeats until the illustration is approved.

## Project Structure

```python
.
├── scripts/
│   ├── conductor.py          # The NEW Master Control Program!
│   ├── prompt_generator.py     # The Smart Prompt Assembler
│   ├── author.py             # The NEW Automated Narrative Engine
│   ├── critic.py             # The "Wise" Text Critic Bot
│   └── auto_captioner.py     # The Auto-Tagger Bot
├── knowledge_db/
│   ├── rwby_chapter_prompts/
│   │   ├── chapter_01.md
│   │   └── ... (up to 50)
│   ├── rwby_characters.md
│   └── ... (other lore files)
├── training_images/
│   ├── Blake/
│   │   ├── 01.png
│   │   └── 01.txt
│   ├── Ruby/
│   └── ... (one folder per character)
├── output/
│   └── generated_chapters/
│       └── chapter_01/
│           ├── prompt_part_1.md
│           └── ...
├── .env
├── .gitignore
└── README.md
````

## Future Enhancements

- **IMMEDIATE NEXT STEP: Test & Debug the `conductor.py` Pipeline:**
  - Execute the first full run of `conductor.py` on a test chapter.
  - Identify and squash any bugs in the new scripts and their interactions.
  - Refine the `FAILURE_KEYWORDS` in `conductor.py` for more accurate pass/fail detection.
  - Potentially enhance the retry loop to pass the critique *back* to the author prompt for smarter revisions.
- **Project LoRA - Phase 3 (Training):** Research and execute the training of our first LoRA models (e.g., for Ruby) using our fully prepared and captioned dataset.
- **Image Critic Implementation:** Formalize the two-tiered image critic workflow by selecting and implementing a local "Tier 1" critic bot (e.g., Moondream).
- **Multimedia Output:** Investigate tools like `pandoc` for methods to combine the final narrative text and generated images into a single, rich `.epub` file.

-----

*Inspired by the boundless creativity of Rooster Teeth's RWBY.*
*Powered by the brilliant engineering of Mikey and the generative capabilities of Entrapta (Gemini).*
