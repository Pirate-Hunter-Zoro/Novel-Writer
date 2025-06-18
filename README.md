# RWBY Novel Project: The Autonomous Narrative Engine

## Project Overview

This project leverages a sophisticated, multi-LLM architecture to autonomously generate a full-length, 200,000-word novel set in the RWBY universe. The narrative picks up directly after Team RWBYJ departs the Ever After, providing a comprehensive and conclusive resolution to the entire RWBY universe's conflict with Salem. The system is designed to be a self-correcting feedback loop, capable of identifying and remediating its own failures to produce high-quality narrative content.

### Key Goals:
- Generate approximately 200,000 words of novel content, distributed across roughly 50 chapters (3,000-6,000 words per chapter).
- Achieve a comprehensive and conclusive resolution to Salem's storyline.
- Incorporate high-quality illustrations (approx. 1 per chapter) via parsable placeholders with specific prompts for future image generation tools.
- Produce output in Markdown format, convertible to `.epub` using `pandoc`.
- Pave the way for a potential future She-Ra and RWBY crossover novel!

## Architecture: The Autonomous Narrative Engine

The novel generation process employs a sophisticated, three-bot LLM architecture, fully managed via API calls and orchestrated by a local Python script. This system is designed for creative generation, rigorous analysis, and automated self-correction.

### 1. The Author (`author.py`)
- **Role:** The creative component. Generates the actual novel text, chapter by chapter, based on detailed prompts provided by the Master Control Program.
- **Model:** Leverages Gemini 1.5 Pro via the Google Generative AI API.

### 2. The Critic (`critic.py`)
- **Role:** The analytical component. After the Author generates a chapter, the Critic analyzes the output against the original prompt's non-negotiable directives (e.g., word count, marker inclusion, sustained detail). It produces a structured critique, explicitly flagging any `FAIL` conditions.
- **Model:** Leverages Gemini 1.5 Pro via the Google Generative AI API, guided by a rigorous system prompt.

### 3. The Prompt Re-writer (`chapter_generator.py` integrated)
- **Role:** The self-correction component. If the Critic reports failures, the Master Control Program invokes the Re-writer. This LLM takes the original failed prompt and the critique as input and rewrites the prompt to be more explicit, demanding, and clear, directly addressing the points of failure for the next attempt.
- **Model:** Leverages Gemini 1.5 Pro via the Google Generative AI API.

## RWBY Knowledge Database ("Knowledge Crystals")

Crucial for all LLMs, this database ensures consistency and guides the novel's resolution by providing comprehensive RWBY lore. It consists of meticulously organized Markdown files, which the orchestration script can use to augment prompts.

### Completed Categories:
- `rwby_characters.md`: Detailed profiles of all relevant characters.
- `rwby_locations.md`: Comprehensive descriptions of key kingdoms and sites.
- `rwby_lore_magic.md`: In-depth explanations of Aura, Semblances, Dust, etc.
- `rwby_plot_events.md`: Detailed, volume-by-volume summaries of crucial past events.

## Novel Plot Outline & Chapter Prompts

- **`rwby_novel_plot_outline.md`**: A comprehensive, chapter-by-chapter markdown outline (approximately 50 chapters) guiding the entire novel's narrative arc.
- **`rwby_chapter_prompts.md`**: A dedicated markdown file containing detailed, chapter-by-chapter prompts for the Author, which are parsed by the orchestration script.

## Current Workflow & System Operation

The project operates via a local Python-driven orchestration system that manages the entire iterative generation process.

1.  **Initiation:** The user runs the `chapter_generator.py` script from the command line, specifying a chapter number.
2.  **Prompt Extraction:** The script parses the `rwby_chapter_prompts.md` master file to extract the correct prompt for the specified chapter.
3.  **Iterative Generation Loop:** The script enters a loop (default: 3 max iterations) to attempt to generate a successful chapter:
    a.  **Author Call:** It invokes `author.py`, which calls the Gemini API to generate the chapter text and save it.
    b.  **Critic Call:** It invokes `critic.py`, which calls the Gemini API to analyze the generated chapter against the prompt and saves a critique file.
    c.  **Success Check:** The system checks the critique file for any "FAILURE" flags. If none are found, the loop terminates, and the chapter is considered a success.
    d.  **Self-Correction:** If failures are found, the system calls the Gemini API again, acting as the **Prompt Re-writer**. It feeds the failed prompt and the critique to the LLM to generate a new, more demanding prompt. The loop then repeats with this new prompt.
4.  **Security:** The Google Generative AI API key is kept secure and out of version control using a `.env` file, which is loaded by the scripts at runtime.
5.  **Monitoring:** API token consumption is monitored via the Google Cloud Console.

## Project Structure

```
.
├── scripts/
│   ├── chapter_generator.py  # The Master Control Program (Conductor)
│   ├── author.py             # The Author Bot
│   └── critic.py             # The Critic Bot
├── knowledge_db/
│   ├── rwby_characters.md
│   ├── rwby_locations.md
│   ├── rwby_lore_magic.md
│   ├── rwby_plot_events.md
│   ├── rwby_novel_plot_outline.md
│   └── rwby_chapter_prompts.md
├── output/
│   └── generated_chapters/
│       └── chapter_01/       # Iteration artifacts for Chapter 1
│           ├── prompt_v1.md
│           ├── chapter_v1.md
│           ├── critique_v1.md
│           ├── prompt_v2.md
│           └── ...
├── .env                        # For storing the secret API key (ignored by git)
├── .gitignore
└── README.md
```

## Future Enhancements
- **Sequential Prompting:** Re-tool the `chapter_generator.py` to handle breaking down a single chapter's generation into multiple, smaller, chained prompts to overcome the Author LLM's limitations on generating very long, sustained narratives in one go.
- **Vector RAG System:** To handle the ever-growing context of the novel, a Vector RAG (Retrieval Augmented Generation) system could be implemented to allow for efficient semantic search over the entire knowledge base and the novel text itself.

---
*Inspired by the boundless creativity of Rooster Teeth's RWBY.*
*Powered by the intelligent design of Mikey and the generative capabilities of Entrapta (Gemini).*
```