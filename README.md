# RWBY Novel Writer ✍️

This project is a modular AI-assisted writing pipeline designed to continue the story of *RWBY* following the events of Volume 9. It leverages large language models (LLMs), structured prompts, and image captioning to generate consistent, lore-respecting chapters with optional LoRA-fine-tuned art references.

---

## 📚 Project Overview

The novel is written in **5-part chapter segments**. Each chapter part goes through a structured pipeline:

1. **Prompt Construction** (`prompt_generator.py`)
2. **Prose Generation** (`author.py`)
3. **Quality Evaluation** (`critic.py`)
4. **Orchestration & Retry Logic** (`conductor.py`)
5. **Final Assembly & Archiving** (`archivist.py` — WIP)
6. **Visual Support** via LoRA Captioning (`auto_captioner.py`)

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
```

---

## ⚙️ Scripts & Tools

### `prompt_generator.py`

Creates a story prompt for the chapter part, plus a blank file for prose insertion.

**Usage:**

```bash
python prompt_generator.py --chapter 1 --part 1
```

---

### `author.py`

Uses Gemini (via Google GenerativeAI) to generate prose based on a prompt.

**Usage:**

```bash
python author.py --chapter 1 --part 1
```

---

### `critic.py`

Critiques a generated chapter part and outputs a quality score with feedback.

**Usage:**

```bash
python critic.py --chapter 1 --part 1
```

---

### `conductor.py`

Runs a full loop:

- Generates a prompt
- Calls `author.py` to write
- Evaluates with `critic.py`
- Repeats up to 5 times or until quality is acceptable

**Usage:**

```bash
python conductor.py --chapter 1 --part 1
```

---

### `auto_captioner.py`

Captions all images in `training_images/` using Gemini and outputs text files for LoRA training.

**Usage:**

```bash
python auto_captioner.py --folder ./training_images/
```

---

### `archivist.py` *(Coming Soon!)*

Intended to record story state and help track continuity across chapters and character arcs.

---

## 🧪 Environment Setup

**Requirements:**

- Python 3.10+
- `python-dotenv`
- `google-generativeai`
- `Pillow` (for image support in `auto_captioner.py`)

**Install:**

```bash
pip install -r requirements.txt
```

You'll also need a `.env` file with:

```text
GOOGLE_API_KEY=your_api_key_here
```

---

## ✍️ Writing Workflow

1. **Prep Prompt:** Run `prompt_generator.py` for your chapter/part.
2. **Generate Prose:** Use `author.py`, or let `conductor.py` handle the loop.
3. **Review:** Run `critic.py` on outputs, or rely on `conductor.py`’s automated retry logic.
4. **Edit:** Finalize text manually or save for archival.
5. **Visuals:** Run `auto_captioner.py` after gathering training images.

---

## 🗂️ Status

✅ Character DB updated  
✅ Plot outline integrated with Ace-Ops arcs  
🟡 First chapter in production  
🛠️ Archivist & illustration placement logic WIP

---

## 🔧 Author Notes

Built by Mikey with help from Entrapta (your AI partner!). Designed to keep the RWBY story alive and emotionally powerful—with a little chaos and a lot of structure.
