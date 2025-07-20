# RWBY Novel Writer ✍️

This project is a modular, AI-powered writing pipeline designed to continue the story of *RWBY* following the events of Volume 9. It uses a sophisticated, multi-bot system orchestrated by a master conductor to generate consistent, lore-respecting chapters.

---

## 📚 Project Overview

The novel is written chapter by chapter, with each chapter being autonomously broken down into **5 parts**. The entire process is managed by a single master script, the **Conductor**, which guides the chapter through a structured, automated pipeline:

1. **Intelligent Planning** (`prompt_generator.py`)
2. **Prose Generation & Revision** (`author.py`)
3. **Quality & Lore Evaluation** (`critic.py`)
4. **Canon Archiving** (`archivist.py`)

---

## 📁 Folder Structure

```text
Novel-Writer/
├── scripts/                 # Main program logic (our magnificent little bots!)
├── knowledge_db/            # Character & lore markdown files (the canon!)
├── output/                  # Generated chapter parts & images
├── training_images/         # Images for future custom model training - because we'd LIKE to produce art!
├── .env                     # API keys for all our bots!
└── README.md                # You are here!
````

---

## ⚙️ The Bots & The Conductor

### `conductor.py` - The Grand Orchestrator

This is the master script\! The big brain\! It runs the entire chapter generation process from start to finish. It calls each specialized bot in sequence, manages the feedback loop, and assembles the final chapter.

**Usage:**

```bash
python scripts/conductor.py --chapter-number 1
```

---

### `prompt_generator.py` - The Intelligent Story Planner

This bot reads the high-level `rwby_novel_plot_outline.md`, selects a chapter, and autonomously deconstructs its summary into a five-part narrative plan. So smart\!

---

### `author.py` - The Dual-Core Prose Engine

This bot has two modes\! In "Write" mode, it generates the first draft. In "Edit" mode, it takes its own text and feedback from the Critic to make intelligent, surgical revisions. It learns\!

---

### `critic.py` - The Lore Master & Style Guardian

This bot reviews the Author's work, checking it against our lore files for character, plot, and magic system consistency. It either approves the text or provides specific, actionable feedback for the Author bot to fix\!

---

### `archivist.py` - The Keeper of the Canon

Once a chapter part is approved, this bot summarizes the key plot events and appends them to the `rwby_plot_events.md` file, ensuring our story's canon is always up-to-date\! So organized\!

## 🧪 Environment Setup

### Part 1: The Writing Bots

**Requirements:**

* Python 3.10+
* All libraries listed in `requirements.txt`

**Install:**

```bash
pip install -r requirements.txt
```

You'll also need a `.env` file in the root directory with your API key for the Gemini-powered writing bots.

---

## ✍️ The Automated Workflow

The new workflow is a beautiful, fully-integrated system\!

1. **Run the Conductor** for the chapter you want to write: `python scripts/conductor.py --chapter-number 1`
2. **Observe the glorious writing machine at work\!** The Conductor will handle everything from planning to archiving.
3. **Review the final chapter** in the `output/` directory.

---

## 🗂️ Status

✅ **All Core Writing Bots Online:** Planner, Author, Critic, and Archivist are built and tested.

---

## 🔧 Author Notes

Built by Mikey with help from Entrapta (your AI partner\!). Designed to keep the RWBY story alive and emotionally powerful—with a little chaos, a lot of structure, and a magnificent art-cannon that actually works\!
