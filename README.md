# RWBY Novel Writer ✍️

This project is a modular, AI-powered writing pipeline designed to continue the story of *RWBY* following the events of Volume 9. It uses a sophisticated, multi-bot system orchestrated by a master conductor to generate consistent, lore-respecting chapters.

---

## 📚 Project Overview

The novel is written chapter by chapter, with each chapter being autonomously broken down into **5 parts**. The entire process is managed by a single master script, the **Conductor**, which guides the chapter through a structured, automated pipeline:

1.  **Intelligent Planning** (`prompt_generator.py`)
2.  **Prose Generation & Revision** (`author.py`)
3.  **Quality & Lore Evaluation** (`critic.py`)
4.  **Canon Archiving** (`archivist.py`)
5.  **(Optional) Visual Support** via LoRA Captioning (`auto_captioner.py`)

---

## 📁 Folder Structure

```text
Novel-Writer/
├── scripts/                 # Main program logic (see below)
├── knowledge_db/           # Character & lore markdown files
├── output/                 # Generated chapter parts & logs
├── training_images/        # Images for LoRA training
├── .env                    # Gemini API keys and environment vars
└── README.md               # You are here!
````

-----

## ⚙️ The Bots & The Conductor

### `conductor.py` - The Grand Orchestrator

This is the master script. It runs the entire chapter generation process from start to finish. It calls each specialized bot in sequence, manages the feedback loop, and assembles the final chapter.

**Usage:**

```bash
python scripts/conductor.py --chapter-number 1
```

-----

### `prompt_generator.py` - The Intelligent Story Planner

This bot reads the high-level `rwby_novel_plot_outline.md`, selects a chapter, and autonomously deconstructs its summary into a five-part narrative plan. It no longer writes files; it provides the plan directly to the Conductor.

-----

### `author.py` - The Dual-Core Prose Engine

This bot has two modes. In "Write" mode, it takes a prompt from the Planner and generates the first draft. In "Edit" mode, it takes its own text and feedback from the Critic to make intelligent, surgical revisions.

-----

### `critic.py` - The Lore Master & Style Guardian

This bot reviews the Author's work. It uses a precision-guided knowledge retrieval system to check the text against our lore files for character, plot, and magic system consistency. It either approves the text or provides specific, actionable feedback.

-----

### `archivist.py` - The Keeper of the Canon

Once a chapter part is approved by the Critic, this bot reads the text, intelligently summarizes the key plot events, and appends them to the `rwby_plot_events.md` file, ensuring our story's canon is always up-to-date.

-----

### `auto_captioner.py` - The LoRA Trainer's Assistant

A utility script for the visual side of the project. It uses Gemini to analyze images in the `training_images/` folder and generates descriptive text files for LoRA training.

-----

## 🧪 Environment Setup

**Requirements:**

- Python 3.10+
- `python-dotenv`
- `google-generativeai`

**Install:**

```bash
pip install -r requirements.txt
```

You'll also need a `.env` file in the root directory with your API key:

```text
GOOGLE_API_KEY=your_api_key_here
```

-----

## ✍️ The New Automated Workflow

The old multi-step manual process is obsolete\! The new workflow is beautifully simple:

1. **Ensure your `rwby_novel_plot_outline.md` is ready.**
2. **Run the Conductor** for the chapter you want to write:

    ```bash
    python scripts/conductor.py --chapter-number 1
    ```

3. **Observe the glorious machine at work\!** The Conductor will handle the entire planning, writing, critiquing, editing, and archiving process.
4. **Review the final chapter** in the `output/generated_chapters/` directory.

-----

## 🗂️ Status

✅ **All Core Bots Online:** Planner, Author, Critic, and Archivist are built and tested.  
✅ **Fully Automated Pipeline:** The Conductor is operational and integrates all bots.  
✅ **Intelligent Systems:** Bots use targeted data retrieval and AI-driven planning.  
🟡 **Ready for First Full Chapter Generation\!**

-----

## 🔧 Author Notes

Built by Mikey with help from Entrapta (your AI partner\!). Designed to keep the RWBY story alive and emotionally powerful—with a little chaos and a lot of structure.
