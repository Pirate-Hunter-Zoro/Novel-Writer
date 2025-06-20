# RWBY Novel Project: The Autonomous Narrative Engine

## Project Overview

This project leverages a sophisticated, multi-LLM architecture to autonomously generate a full-length, 200,000-word novel set in the RWBY universe. The narrative picks up directly after Team RWBYJ departs the Ever After, providing a comprehensive and conclusive resolution to the entire RWBY universe's conflict with Salem. The initial creative phase of outlining the 50-chapter plot and engineering the detailed, sequential chapter prompts is now complete. The system is designed as a self-correcting feedback loop, capable of identifying and remediating its own failures to produce high-quality narrative content.

### Key Goals:
- Generate approximately 200,000 words of novel content, distributed across 50 chapters (3,000-6,000 words per chapter).
- Achieve a comprehensive and conclusive resolution to Salem's storyline.
- Incorporate high-quality illustrations (approx. 1 per micro-prompt, ~5 per chapter) via parsable placeholders with specific prompts for future image generation tools.
- Produce output in Markdown format, convertible to `.epub` using `pandoc`.
- Pave the way for a potential future She-Ra and RWBY crossover novel!

## Architecture: The Autonomous Narrative Engine

The novel generation process employs a sophisticated, three-bot LLM architecture, fully managed via API calls and orchestrated by a local Python script. This system is designed for creative generation, rigorous analysis, and automated self-correction.

### 1. The Author (`author.py`)
- **Role:** The creative component. Generates the actual novel text, section by section, based on a sequence of detailed prompts provided by the Master Control Program.
- **Model:** Leverages Gemini 1.5 Pro via the Google Generative AI API.

### 2. The Critic (`critic.py`)
- **Role:** The analytical component. After the Author generates a full chapter, the Critic analyzes the output against a set of rules and, critically, the project's Knowledge Database. It produces a structured critique, explicitly flagging any `FAIL` conditions related to lore inconsistency, character voice drift, or quality pacing.
- **Model:** Leverages Gemini 1.5 Pro via the Google Generative AI API, guided by a rigorous system prompt.

### 3. The Prompt Re-writer (`chapter_generator.py` integrated)
- **Role:** The self-correction component. If the Critic reports failures, the Master Control Program invokes the Re-writer. This LLM takes the original failed prompt sequence and the critique as input and rewrites the prompts to be more explicit, demanding, and clear, directly addressing the points of failure for the next attempt.
- **Model:** Leverages Gemini 1.5 Pro via the Google Generative AI API.

## RWBY Knowledge Database ("Knowledge Crystals")

Crucial for all LLMs, this database ensures consistency and guides the novel's resolution by providing comprehensive RWBY lore. It consists of meticulously organized Markdown files, which the orchestration script can use to augment prompts.

### Completed Categories:
- `rwby_characters.md`: Detailed profiles of all relevant characters.
- `rwby_locations.md`: Comprehensive descriptions of key kingdoms and sites.
- `rwby_lore_magic.md`: In-depth explanations of Aura, Semblances, Dust, etc.
- `rwby_plot_events.md`: Detailed, volume-by-volume summaries of crucial past events.

## Novel Plot Outline & Sequential Chapter Prompts

- **`rwby_novel_plot_outline.md`**: A comprehensive, chapter-by-chapter markdown outline (approximately 50 chapters) guiding the entire novel's narrative arc.
- **`sequential_prompts/`**: A dedicated directory containing 50 markdown files, one for each chapter. Each file contains a detailed, 5-part sequential prompt sequence. This architecture was designed to overcome the Author LLM's limitations by breaking down the generation of a long chapter into smaller, chained, high-detail sections.

## Current Workflow & System Operation

The project operates via a local Python-driven orchestration system that manages the entire sequential generation process.

1.  **Initiation:** The user runs the `chapter_generator.py` script from the command line, specifying a chapter number.
2.  **Prompt Loading:** The script loads the entire multi-part prompt file for the specified chapter from the `sequential_prompts/` directory.
3.  **Sequential Generation Loop:** The script iterates through the 5 prompts (A-E) for that chapter:
    a.  **Author Call:** It invokes `author.py`, feeding it the specific micro-prompt for the current section **and the full text of all previously generated sections** as context.
    b.  **Stitching:** The script saves the newly generated section and appends it to a master chapter file.
4.  **Post-Generation Analysis (Future Implementation):** After a full chapter is stitched together, the `critic.py` bot will be invoked to analyze the complete chapter for lore consistency and quality against the Knowledge Database. If failures are detected, the **Prompt Re-writer** will be engaged to improve the prompt sequence for a subsequent attempt.
5.  **Security:** The Google Generative AI API key is kept secure and out of version control using a `.env` file, which is loaded by the scripts at runtime.
6.  **Monitoring:** API token consumption is monitored via the Google Cloud Console.

## Project Structure

```

.
├── scripts/
│   ├── chapter_generator.py  # The Master Control Program (Conductor)
│   ├── author.py             # The Author Bot
│   └── critic.py             # The Critic Bot
├── knowledge_db/
│   ├── sequential_prompts/     # NEW directory for refactored prompts
│   │   ├── chapter_01.md
│   │   ├── chapter_02.md
│   │   └── ... (up to 50)
│   ├── rwby_characters.md
│   ├── rwby_locations.md
│   ├── rwby_lore_magic.md
│   ├── rwby_plot_events.md
│   └── rwby_novel_plot_outline.md
├── output/
│   └── generated_chapters/
│       └── chapter_01.md       # Final stitched chapter output
├── .env                        # For storing the secret API key (ignored by git)
├── .gitignore
└── README.md

```

## Future Enhancements
- **Lore-Aware Critic (HIGH PRIORITY):** The next major development task. Upgrade `critic.py` to dynamically load and parse the entire Knowledge Database. The Critic will then perform automated checks against the generated text to ensure consistency with established characters, lore, magic systems, and plot events, flagging any contradictions for the Re-writer.
- **Vector RAG System:** To handle the ever-growing context of the novel, a Vector RAG (Retrieval Augmented Generation) system could be implemented to allow for efficient semantic search over the entire knowledge base and the novel text itself.

---
*Inspired by the boundless creativity of Rooster Teeth's RWBY.*
*Powered by the intelligent design of Mikey and the generative capabilities of Entrapta (Gemini).*