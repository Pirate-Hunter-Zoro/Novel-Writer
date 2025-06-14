# RWBY Novel Project: A Generative AI Endeavor

## Project Overview

This project aims to leverage advanced Large Language Models (LLMs) to generate a full-length, 200,000-word novel set in the RWBY universe. The narrative will pick up directly after Team RWBYJ departs the Ever After, with the ambitious goal of providing a definitive conclusion to Salem's storyline.

### Key Goals:
- Generate approximately 200,000 words of novel content.
- Achieve a comprehensive and conclusive resolution to the conflict with Salem.
- Incorporate high-quality illustrations (approx. 1 per 1000 words) via parsable placeholders and image generation prompts within the text.
- Produce output in Markdown format, convertible to `.epub` using `pandoc`.
- Pave the way for a potential future She-Ra and RWBY crossover novel!

## Architecture

The novel generation process employs a dual-LLM architecture designed for both creative text generation and rigorous narrative consistency.

### 1. Author LLM (Text Generation)
- **Role:** Focuses on generating the actual novel text, chapter by chapter.
- **Context Management:** Its context is primarily limited to the current section being written.
- **Current Model:** `unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit` (chosen for optimal performance on Google Colab's T4 GPUs).
- **Previous Attempt:** Initially attempted `unsloth/Meta-Llama-3.1-70B-Instruct-bnb-4bit` but encountered VRAM limitations (70B 4-bit model requires ~35GB, T4 GPU has 16GB).

### 2. Critic LLM (Narrative Cohesion & Consistency)
- **Role:** Responsible for maintaining narrative cohesion, consistency, and adherence to RWBY lore across the entire novel. Provides feedback to the Author LLM.
- **Context Management:** Addresses its own context window limitations through a Vector RAG (Retrieval Augmented Generation) system.

### Vector RAG (Retrieval Augmented Generation) System
- **Functionality:** Converts the novel's text and a comprehensive RWBY "Knowledge Database" into numerical vectors using an embedding model. These vectors are stored in a vector database.
- **Benefit:** Allows the Critic LLM to perform semantic searches against this database, retrieving only the most relevant plot points and details to ensure it has necessary information without exceeding its context window.

## RWBY Knowledge Database ("Knowledge Crystals")

Crucial for the Critic LLM, this database ensures consistency and guides the novel's resolution by providing comprehensive RWBY lore. It consists of organized Markdown files, which will be chunked, embedded, and stored in the vector database.

### Proposed Categories:
- `rwby_characters.md`: Key characters, semblances, weapons, backstories, relationships.
- `rwby_locations.md`: Kingdoms, Academies, significant sites, the Ever After, Salem's domain.
- `rwby_lore_magic.md`: Dust, Aura, Semblances, Relics, Maidens, Silver Eyes, Gods, Grimm, history.
- `rwby_plot_events.md`: Summaries of crucial events from past volumes (Beacon, Haven, Atlas, Ever After).

## Development Environment

- **Primary Platform:** Google Colab Pro (ideal for GPU access and collaboration).
- **Local Editing:** VS Code (for editing notebooks and project files) with Google Drive app for syncing.
- **Python Dependencies:**
    - `bitsandbytes`
    - `huggingface_hub`
    - `transformers`
    - `torch`
    - `accelerate`
    - (Additional libraries for embeddings and vector database will be added)

## Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd rwby-novel-project
    ```
2.  **Google Colab Pro:** Ensure you have access to Google Colab Pro for GPU resources.
3.  **Open in Colab:** Open the main Colab notebook (`RWBY_Novel_Generation.ipynb` or similar) directly in Google Colab.
4.  **Install Dependencies:** Run the initial cells in the Colab notebook to install necessary `pip` packages.
5.  **Prepare Knowledge Database:** Populate the Markdown files in the `knowledge_db/` directory (e.g., `rwby_characters.md`, `rwby_locations.md`, etc.) with relevant RWBY lore.
6.  **Start Generating!** Follow the instructions within the Colab notebook to begin generating novel chapters.

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
│   └── rwby_plot_events.md
└── output/                      # Future directory for generated novel chapters
    ├── chapter_01.md
    └── ...
# NOTE: vllm_models/ directory is NOT committed due to large file sizes.
```

## Contributing

(Future section for team collaboration guidelines)

---
*Inspired by the boundless creativity of Rooster Teeth's RWBY.*
```