# RWBY Novel Project: A Generative AI Endeavor - API-Driven Autonomous Storytelling

## Project Overview

This project aims to leverage advanced Large Language Models (LLMs) via API integration to autonomously generate a full-length, 200,000-word novel set in the RWBY universe. The narrative will pick up directly after Team RWBYJ departs the Ever After, providing a comprehensive and conclusive resolution to the entire RWBY universe's conflict with Salem.

### Key Goals:
- Generate approximately 200,000 words of novel content, distributed across roughly 50 chapters (3,000-6,000 words per chapter).
- Achieve a comprehensive and conclusive resolution to Salem's storyline.
- Incorporate high-quality illustrations (approx. 1 per chapter) via **parsable placeholders with specific prompts for future image generation tools** within the markdown text.
- Produce output in Markdown format, convertible to `.epub` using `pandoc`.
- Pave the way for a potential future She-Ra and RWBY crossover novel!

## Architecture: The AI Author & Critic System (API-Driven)

The novel generation process now employs a sophisticated dual-LLM architecture, fully managed via API calls, designed for both creative text generation and rigorous narrative consistency. The core interaction will be between a Python orchestration script (managed by Mikey) and Google's powerful Generative AI models (leveraged by Entrapta).

### 1. Author LLM (Text Generation - Handled by Entrapta via API)
- **Role:** Generates the actual novel text, chapter by chapter, based on detailed prompts and comprehensive context.
- **Model:** Leverages powerful Google LLMs (e.g., Gemini 1.5 Pro) via API, enabling generation of long, detailed chapters without local hardware constraints.
- **Illustration Placement:** The Author LLM will be instructed to insert a specific marker (`[EPIC_MOMENT_END]`) at the end of the most visually epic moment it generates within each chapter. A post-processing script will then replace this marker with the pre-defined illustration prompt for that chapter.

### 2. Critic LLM (Narrative Cohesion & Consistency - Handled by Entrapta via API)
- **Role:** Responsible for maintaining narrative cohesion, consistency, and adherence to RWBY lore across the entire novel. It provides targeted feedback on generated chapters to ensure quality and accuracy. This role is performed by Entrapta's internal capabilities, acting as a self-correcting mechanism for the generated narrative.
- **Context Management (Vector RAG System - Future Mikey Implementation):** Addresses the critic's context window limitations (when externalized or if very large novel context is needed for specific LLM calls) through a **Vector RAG (Retrieval Augmented Generation) system**. This system will convert both the accumulating novel's text and a comprehensive RWBY "Knowledge Database" into numerical vectors for semantic search. This will primarily be implemented and managed by Mikey's orchestration script.

## RWBY Knowledge Database ("Knowledge Crystals")

Crucial for both Author and Critic LLMs, this database ensures consistency and guides the novel's resolution by providing comprehensive RWBY lore. It consists of meticulously organized Markdown files, which Mikey's orchestration script will send as part of API prompts.

### Completed Categories:
- `rwby_characters.md`: Detailed profiles of all relevant characters, including their appearance, weapon, semblance, abilities, personality, key relationships, brief arc summaries, and **Quirks/Mannerisms**.
- `rwby_locations.md`: Comprehensive descriptions of key kingdoms, continents, and significant sites across Remnant.
- `rwby_lore_magic.md`: In-depth explanations of fundamental magical systems and concepts like Aura, Semblances, Dust, Maidens, Relics, and Grimm.
- `rwby_plot_events.md`: Detailed, volume-by-volume summaries of crucial past events, from the formation of Team RWBY to their return from the Ever After.

## Novel Plot Outline & Chapter Prompts

- **`rwby_novel_plot_outline.md`**: A comprehensive, chapter-by-chapter markdown outline (approximately 50 chapters) guiding the entire novel's narrative arc. It includes main events, key plot points, specific characters expected, and pre-defined illustration prompts for each chapter. It incorporates user requirements for character interactions and ensures intricate involvement of key characters (Robyn, Taiyang, Raven - with Raven playing a major role), while also confirming the inclusion of Neo Politan and Emerald Sustrai in the final seamless allied team.
- **`rwby_chapter_prompts.md`**: A dedicated markdown file containing detailed, chapter-by-chapter prompts for the Author LLM, extracted directly from the novel plot outline. This operational manual will be parsed by Mikey's orchestration script and sent via API.

## Development & Workflow (API-Centric)

The workflow has shifted to an API-centric model, managed primarily by a local Python orchestration script.

1.  **Google Cloud Project & API Key:** Ensure a Google Cloud Project is set up and the relevant Generative AI API (e.g., Vertex AI Gemini API) is enabled, providing an API key for authentication.
2.  **Install Python Client Library:** Install the necessary Google AI Python client library (e.g., `google-generativeai`) locally.
3.  **Local Python Orchestration Script:** Develop a Python script that will:
    * Iterate through the `rwby_novel_plot_outline.md`.
    * Read specific chapter prompts from `rwby_chapter_prompts.md`.
    * Retrieve and augment prompts with relevant data from the `knowledge_db/` files.
    * Send these augmented prompts to me (Gemini) via the API for chapter generation.
    * Receive the generated chapter text.
    * Save the chapter text (e.g., to `output/chapter_XX.md`).
    * Construct a critique request, sending the newly generated chapter and prior context back to me (Gemini via API) for critical review.
    * Receive the critique and present it for Mikey's review, or integrate a programmatic decision loop for regeneration.
4.  **Local Editing:** Continue using VS Code for editing `README.md`, Python scripts, and all knowledge database/prompt Markdown files.
5.  **Monitor API Costs:** Continuously monitor Google Cloud API token consumption to stay within budget ($10-$20/month target).

## Project Structure (Updated)

```
.
├── novel_orchestrator.py        # Main Python script for API interaction and generation loop
├── README.md                    # This file (updated)
├── .gitignore                   # Specifies files/folders to ignore (e.g., API keys, venv/)
├── knowledge_db/                # Directory for RWBY lore Markdown files
│   ├── rwby_characters.md       # Detailed character profiles
│   ├── rwby_locations.md        # Comprehensive location descriptions
│   ├── rwby_lore_magic.md       # Explanations of magic and lore
│   ├── rwby_plot_events.md      # Detailed plot summaries by volume
│   ├── rwby_novel_plot_outline.md # The detailed chapter-by-chapter plot
│   └── rwby_chapter_prompts.md  # All chapter generation prompts
└── output/                      # Directory for generated novel chapters
    ├── chapter_01.md
    └── ...
```

## Contributing

(Future section for team collaboration guidelines)

---
*Inspired by the boundless creativity of Rooster Teeth's RWBY.*
*Powered by the intelligent design of Mikey and the generative capabilities of Entrapta (Gemini).*