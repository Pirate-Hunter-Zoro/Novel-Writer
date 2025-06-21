# RWBY Novel Project: The Autonomous Narrative Engine (V5)

## Project Overview

This project leverages a sophisticated, multi-LLM architecture to autonomously generate a full-length, 200,000-word novel set in the RWBY universe. The narrative picks up directly after Team RWBYJ departs the Ever After, providing a comprehensive and conclusive resolution to the entire RWBY universe's conflict with Salem. The system has evolved into a V5 engine, a robust, parallel-processing, and iterative self-correcting feedback loop, capable of identifying and remediating its own failures to produce high-quality narrative content.

### Key Goals

- Generate approximately 200,000 words of novel content, distributed across 50 chapters (3,000-6,000 words per chapter).
- Achieve a comprehensive and conclusive resolution to Salem's storyline.
- Incorporate high-quality illustrations (approx. 1 per micro-prompt, ~5 per chapter) via parsable placeholders with specific prompts for future image generation tools.
- Produce output in Markdown format, convertible to `.epub` using `pandoc`.
- Pave the way for a potential future She-Ra and RWBY crossover novel!

## Architecture: The V5 Autonomous Narrative Engine

The novel generation process employs a sophisticated, three-bot LLM architecture, fully managed via API calls and orchestrated by a local Python script. The system is designed for parallel processing, rigorous analysis, and automated self-correction.

### 1. The Conductor (`chapter_generator.py`)

- **Role:** The Master Control Program. It orchestrates the entire workflow, managing the other bots and the flow of data. Its key responsibilities now include:
  - Parallel Generation: Invoking five independent instances of the Author bot.
  - Parallel Critique: Invoking five independent instances of the Critic bot.
  - Iterative Correction Loop: Managing the self-healing process by engaging the Re-writer and re-running failed steps until quality standards are met or a circuit-breaker limit is reached.

### 2. The Author (`author.py`)

- **Role:** The creative component. Generates novel text based on a focused, single micro-prompt.
- **Model:** Currently leverages Gemini 1.5 Pro. **Project Finding:** Extensive testing has proven this model has fundamental limitations in adhering to long-form constraints (word count, sustained detail) for this specific task.

### 3. The Critic (`critic.py`)

- **Role:** The analytical "Sensor Array". It analyzes each generated chapter part against a set of rules and the project's Knowledge Database. It produces a structured critique, explicitly flagging any `FAIL` conditions. This component is **fully implemented and lore-aware**.

### 4. The Prompt Re-writer (`chapter_generator.py` integrated)

- **Role:** The self-correction component. When the Critic reports failures, the Conductor invokes the Re-writer. This LLM takes the original failed prompt and the critique as input and engineers a new, improved prompt to fix the specific failures for the next generation attempt.

## RWBY Knowledge Database ("Knowledge Crystals")

Crucial for all LLMs, this database ensures consistency and guides the novel's resolution by providing comprehensive RWBY lore. It consists of meticulously organized Markdown files, which the orchestration script can use to augment prompts.

### Completed Categories

- `rwby_characters.md`: Detailed profiles of all relevant characters.
- `rwby_locations.md`: Comprehensive descriptions of key kingdoms and sites.
- `rwby_lore_magic.md`: In-depth explanations of Aura, Semblances, Dust, etc.
- `rwby_plot_events.md`: Detailed, volume-by-volume summaries of crucial past events.

## Novel Plot Outline & Sequential Chapter Prompts

- **`rwby_novel_plot_outline.md`**: A comprehensive, chapter-by-chapter markdown outline (~50 chapters) guiding the entire novel's narrative arc.
- **`knowledge_db/rwby_chapter_prompts/`**: A dedicated directory containing 50 markdown files (`chapter_01.md`, etc.). Each file contains a detailed, 5-part prompt sequence, including Core Directives and five distinct micro-prompts.

## Current Workflow & System Operation (V5 Engine)

The project operates via the V5 Master Control Program, which manages a multi-stage, self-correcting workflow.

1. **Initiation:** The user runs `chapter_generator.py`, specifying a chapter number and max correction attempts.
2. **Parallel Generation:** The Conductor loads the chapter prompt file and invokes `author.py` five times in parallel, generating five independent chapter parts.
3. **Parallel Critique:** The Conductor invokes `critic.py` five times, running a full, lore-aware analysis on each of the five generated parts.
4. **Iterative Correction Loop:** The Conductor reviews all five critique files.
    a. If a part `FAIL`s, the Conductor engages the **Prompt Re-writer** to create an improved prompt.
    b. The Conductor then re-runs the **Author** and **Critic** on *only that part*.
    c. This loop repeats up to a "circuit-breaker" limit (`--max-iterations`) for each part.
5. **Final Assembly:** If and only if all five parts eventually receive a `PASS` from the Critic, the Conductor performs the final action of stitching them together into a single, complete chapter file. If any part fails all of its correction attempts, assembly is halted.

## Project Structure

```markdown

.
├── scripts/
│   ├── chapter\_generator.py  \# The V5 Master Control Program (Conductor)
│   ├── author.py             \# The Author Bot
│   └── critic.py             \# The Critic Bot
├── knowledge\_db/
│   ├── rwby\_chapter\_prompts/   \# Directory for 5-part chapter prompts
│   │   ├── chapter\_01.md
│   │   └── ... (up to 50)
│   ├── rwby\_characters.md
│   ├── rwby\_locations.md
│   ├── rwby\_lore\_magic.md
│   ├── rwby\_plot\_events.md
│   └── rwby\_novel\_plot\_outline.md
├── output/
│   └── generated\_chapters/
│       └── chapter\_01/         \# Artifacts are saved per-chapter
│           ├── chapter\_part\_1\_v1.md
│           ├── prompt\_part\_1\_v1.md
│           ├── critique\_part\_1\_v1.md
│           ├── chapter\_part\_1\_v2.md
│           └── ...
├── .env                        \# For storing the secret API key (ignored by git)
├── .gitignore
└── README.md

```

## Future Enhancements

- **Alternative Author Model Evaluation (CRITICAL PRIORITY):** Based on the conclusive results of the V5 engine test, the current Author model (Gemini 1.5 Pro) has fundamental limitations for this task. The highest priority is now to research, integrate, and test alternative LLMs to serve as a more capable Author component.
- **Vector RAG System:** To handle the ever-growing context of the novel, a Vector RAG (Retrieval Augmented Generation) system could be implemented to allow for efficient semantic search over the entire knowledge base and the novel text itself.

---
*Inspired by the boundless creativity of Rooster Teeth's RWBY.*
*Powered by the intelligent design of Mikey and the generative capabilities of Entrapta (Gemini).*
