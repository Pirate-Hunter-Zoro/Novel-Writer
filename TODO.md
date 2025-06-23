# RWBY Novel Project: The Collaborative Narrative Engine (v2.0)

## Project Overview

This project leverages a sophisticated, human-AI collaborative architecture to generate a full-length, 200,000-word novel set in the RWBY universe. The narrative picks up directly after Team RWBYJ departs the Ever After, providing a comprehensive and conclusive resolution to the entire RWBY universe's conflict with Salem. The system has evolved into a highly efficient, iterative multimedia workflow that pairs the creative power of a generative AI (Entrapta) with the precise, high-level direction and quality control of a human Conductor (Mikey).

### Key Goals

- Generate approximately 200,000 words of novel content, distributed across 50 chapters.
- Achieve a comprehensive and conclusive resolution to Salem's storyline.
- **Generate high-quality, character-consistent illustrations** for each chapter part using a custom-trained **LoRA (Low-Rank Adaptation)** model.
- Produce output in Markdown format, with a future goal of combining text and images into a rich `.epub`.
- Pave the way for a potential future She-Ra and RWBY crossover novel!

## Architecture: The Human-in-the-Loop Collaborative Engine

The project's architecture has expanded to include a full visual generation and data preparation pipeline, managed by the human Conductor.

### 1. The Conductor (Mikey)

- **Role:** The Master Control Program, Lead Engineer, and Data Archivist. The Conductor orchestrates the entire workflow, manages the toolset, provides high-level creative direction, curates training data, and performs final quality assurance on both text and images.

### 2. The Author & Visualizer (Entrapta)

- **Role:** The primary creative core.
  - As **Author**, I generate the novel text based on prompts, receive feedback from the Critic bot, and perform revisions.
  - As **Visualizer**, I generate illustrations based on refined prompts, using custom LoRA modules to ensure character consistency.
  - As **Lead Critic**, I can provide "Tier 2" subjective analysis on generated images.

### 3. The Python Bot Army (The Scripts)

- **The Prompt Generator (`prompt_generator.py`):** An automated "Instruction Injector" that enhances simple chapter prompts and prepares the workspace.
- **The Text Critic (`critic.py`):** The "Wise Critic" that analyzes generated text against a ruleset and the Knowledge Database.
- **The Auto-Tagger (`auto_captioner.py`):** A new, API-powered bot that processes the local image database and automatically generates keyword captions for LoRA training.

## Knowledge Databases ("Knowledge Crystals")

The system now relies on two forms of knowledge databases to ensure consistency.

### 1. Narrative Knowledge Database

- `rwby_characters.md`, `rwby_locations.md`, `rwby_lore_magic.md`, `rwby_plot_events.md`: Meticulously organized Markdown files providing comprehensive RWBY lore.

### 2. Visual Knowledge Database (For Project LoRA)

- **`training_images/`**: A new, critical directory containing a curated database of 15-20 reference images for each key character, used to train our LoRA models.

## Novel Plot Outline & Sequential Chapter Prompts

- **`rwby_novel_plot_outline.md`**: A comprehensive, chapter-by-chapter outline. Now includes `ILLUSTRATION_PROMPT`s that are actively used for image generation.
- **`knowledge_db/rwby_chapter_prompts/`**: A directory containing 50 markdown files, each with a 5-part prompt sequence for a chapter.

## Current Workflow: The Multimedia Generation Pipeline

The project now operates via a two-stage pipeline for each chapter part: a Narrative Loop followed by a Visual Loop.

1. **Workspace Preparation:** The Conductor runs `prompt_generator.py` to prepare the workspace for a chapter.
2. **Narrative Loop:**
    - The Conductor provides the Author (Entrapta) with a prompt file.
    - The Author generates the text.
    - The Conductor runs `critic.py` and provides the feedback to the Author.
    - This loop repeats until the text passes all quality checks.
3. **Visual Loop:**
    - The Conductor and Author collaborate to refine the `ILLUSTRATION_PROMPT` for the finalized text.
    - The Author (as Visualizer) generates an image using the appropriate LoRA module.
    - The Conductor can use a local "Tier 1" critic for objective checks and the Author for a "Tier 2" subjective critique.
    - This loop repeats until the illustration is approved.
4. **Continuation:** The process is repeated for all five parts of the chapter.

## Project Structure

```python
.
├── scripts/
│   ├── prompt_generator.py     # The Smart Prompt Assembler
│   ├── critic.py             # The "Wise" Text Critic Bot
│   └── auto_captioner.py     # The NEW Auto-Tagger Bot
├── knowledge_db/
│   ├── rwby_chapter_prompts/
│   │   ├── chapter_01.md
│   │   └── ... (up to 50)
│   ├── rwby_characters.md
│   └── ... (other lore files)
├── training_images/            # The NEW Visual Knowledge Database
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

- **Project LoRA - Phase 3 (Training):** The immediate next step is to research and execute the training of our first LoRA models (e.g., for Ruby) using our fully prepared and captioned dataset.
- **Image Critic Implementation:** Formalize the two-tiered image critic workflow by selecting and implementing a local "Tier 1" critic bot (e.g., Moondream).
- **Multimedia Output:** Investigate tools like `pandoc` for methods to combine the final narrative text and generated images into a single, rich `.epub` file.

-----

*Inspired by the boundless creativity of Rooster Teeth's RWBY.*
*Powered by the brilliant engineering of Mikey and the generative capabilities of Entrapta (Gemini).*
