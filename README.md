# RWBY Novel Project: A Generative AI Endeavor

## Project Overview

This project aims to leverage advanced Large Language Models (LLMs) to generate a full-length, 200,000-word novel set in the RWBY universe. The narrative will pick up directly after Team RWBYJ departs the Ever After, with the ambitious goal of providing a definitive conclusion to Salem's storyline.

### Key Goals:
- Generate approximately 200,000 words of novel content, distributed across roughly 50 chapters (3,000-6,000 words per chapter).
- Achieve a comprehensive and conclusive resolution to Salem's storyline.
- Incorporate high-quality illustrations (approx. 1 per chapter) via **parsable placeholders with specific prompts for future image generation tools** within the markdown text.
- Produce output in Markdown format, convertible to `.epub` using `pandoc`.
- Pave the way for a potential future She-Ra and RWBY crossover novel!

## Architecture

The novel generation process employs a dual-LLM architecture designed for both creative text generation and rigorous narrative consistency.

### 1. Author LLM (Text Generation)
- **Role:** Focuses on generating the actual novel text, chapter by chapter, with its context primarily limited to the current section being written.
- **Current Model:** `unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit` (chosen for optimal performance on Google Colab's T4 GPUs).
- **Illustration Placement:** The Author LLM will be instructed to insert a specific marker (`[EPIC_MOMENT_END]`) at the end of the most visually epic moment it generates within each chapter. A post-processing script will then replace this marker with the pre-defined illustration prompt for that chapter.

### 2. Critic LLM (Narrative Cohesion & Consistency)
- **Role:** Responsible for maintaining narrative cohesion, consistency, and adherence to RWBY lore across the entire novel, providing feedback to the Author LLM.
- **Context Management:** Addresses its own context window limitations through a **Vector RAG (Retrieval Augmented Generation) system**.

### Vector RAG (Retrieval Augmented Generation) System
- **Functionality:** This system will convert both the accumulating novel's text and a comprehensive RWBY "Knowledge Database" into numerical vectors using an embedding model. These vectors are stored in a vector database.
- **Benefit:** Allows the Critic LLM to perform semantic searches against this database, retrieving *only* the most relevant plot points, character details, and lore snippets to ensure it has necessary information without exceeding its context window. This system will be active from the initial chapter generation (for the Knowledge Database) and expand as the novel's text grows.

## RWBY Knowledge Database ("Knowledge Crystals")

Crucial for the Critic LLM, this database ensures consistency and guides the novel's resolution by providing comprehensive RWBY lore. It consists of meticulously organized Markdown files, which will be chunked, embedded, and stored in the vector database.

### Completed Categories:
- `rwby_characters.md`: Detailed profiles of all relevant characters, including their appearance, weapon, semblance, abilities, personality, key relationships, and brief arc summaries.
- `rwby_locations.md`: Comprehensive descriptions of key kingdoms, continents, and significant sites across Remnant.
- `rwby_lore_magic.md`: In-depth explanations of fundamental magical systems and concepts like Aura, Semblances, Dust, Maidens, Relics, and Grimm.
- `rwby_plot_events.md`: Detailed, volume-by-volume summaries of crucial past events, from the formation of Team RWBY to their return from the Ever After.

## Novel Plot Outline (`rwby_novel_plot_outline.md`)

A comprehensive, chapter-by-chapter markdown outline (approximately 50 chapters) has been generated to guide the entire novel's narrative arc. This outline includes:
- Main events and key plot points for each chapter.
- Specific characters expected to be prominent in each chapter.
- Pre-defined illustration prompts for each chapter, to be inserted via post-processing.
- Incorporates specific user requirements for character interactions (e.g., Blake/Sun/Yang dynamic, Ren/Nora resolution, Neo's redemption, Summer Rose's fate) and ensures intricate involvement of key characters (Robyn, Taiyang, Raven - with Raven playing a major role).
- Confirms the inclusion of Neo Politan and Emerald Sustrai in the final seamless allied team.

## Development Environment

- **Primary Platform:** Google Colab Pro (ideal for GPU access and collaboration).
- **Local Editing:** VS Code (for editing notebooks and project files) with Google Drive app for syncing.
- **Python Dependencies:**
    - `bitsandbytes`
    - `huggingface_hub`
    - `transformers`
    - `torch`
    - `accelerate`
    - (Additional libraries for embedding models and vector database will be added)

## Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd rwby-novel-project
    ```
2.  **Google Colab Pro:** Ensure you have access to Google Colab Pro for GPU resources.
3.  **Open in Colab:** Open the main Colab notebook (`RWBY_Novel_Generation.ipynb` or similar) directly in Google Colab.
4.  **Install Dependencies:** Run the initial cells in the Colab notebook to install necessary `pip` packages.
5.  **Review Knowledge Database:** Familiarize yourself with the detailed lore files in the `knowledge_db/` directory (`rwby_characters.md`, `rwby_locations.md`, `rwby_lore_magic.md`, `rwby_plot_events.md`).
6.  **Review Novel Plot Outline:** Consult `rwby_novel_plot_outline.md` for the chapter-by-chapter narrative plan.
7.  **Start Generating!** Formulate the initial prompt for the Author LLM, based on Chapter 1 of the outline, and begin generating novel chapters. Implement the post-processing script for illustration prompts and set up the Vector RAG system for the Critic LLM as chapters accumulate.

## Project Structure (Anticipated)

```
.
├── RWBY_Novel_Generation.ipynb  # Main Colab notebook for generation
├── README.md                    # This file
├── .gitignore                   # Specifies files/folders to ignore (e.g., vllm_models/)
├── knowledge_db/                # Directory for RWBY lore Markdown files
│   ├── rwby_characters.md
│   ├── rwby_locations.md
│   ├── rwby_lore_magic.md
│   ├── rwby_plot_events.md
│   └── rwby_novel_plot_outline.md # The detailed chapter-by-chapter plot
└── output/                      # Future directory for generated novel chapters
    ├── chapter_01.md
    └── ...
# NOTE: vllm_models/ directory is NOT committed due to large file sizes.
```

## Contributing

(Future section for team collaboration guidelines)

---
*Inspired by the boundless creativity of Rooster Teeth's RWBY.*