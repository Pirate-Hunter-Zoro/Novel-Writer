# RWBY Novel Writer ✍️

This project is a modular, AI-powered writing pipeline designed to continue the story of *RWBY* following the events of Volume 9. It uses a sophisticated, multi-bot system orchestrated by a master conductor to generate consistent, lore-respecting chapters, complete with an integrated pipeline for fine-tuning custom art models.

---

## 📚 Project Overview

The novel is written chapter by chapter, with each chapter being autonomously broken down into **5 parts**. The entire process is managed by a single master script, the **Conductor**, which guides the chapter through a structured, automated pipeline:

1. **Intelligent Planning** (`prompt_generator.py`)
2. **Prose Generation & Revision** (`author.py`)
3. **Quality & Lore Evaluation** (`critic.py`)
4. **Canon Archiving** (`archivist.py`)
5. **Art Department** (`art_director.py`, `image_generator.py`)
6. **AI Model Training** (`kohya_ss/` submodule)

---

## 📁 Folder Structure

```text
Novel-Writer/
├── scripts/                 # Main program logic (see below)
├── knowledge_db/           # Character & lore markdown files
├── output/                 # Generated chapter parts & images
├── training_images/        # Images for LoRA training
├── kohya_ss/               # The fine-tuning GUI and scripts
├── .env                    # Gemini API keys and environment vars
└── README.md               # You are here!
````

---

## ⚙️ The Bots & The Conductor

### `conductor.py` - The Grand Orchestrator

This is the master script. It runs the entire chapter generation process from start to finish. It calls each specialized bot in sequence, manages the feedback loop, and assembles the final chapter.

**Usage:**

```bash
python scripts/conductor.py --chapter-number 1
```

---

### `prompt_generator.py` - The Intelligent Story Planner

This bot reads the high-level `rwby_novel_plot_outline.md`, selects a chapter, and autonomously deconstructs its summary into a five-part narrative plan.

---

### `author.py` - The Dual-Core Prose Engine

This bot has two modes. In "Write" mode, it generates the first draft. In "Edit" mode, it takes its own text and feedback from the Critic to make intelligent, surgical revisions.

---

### `critic.py` - The Lore Master & Style Guardian

This bot reviews the Author's work, checking it against our lore files for character, plot, and magic system consistency. It either approves the text or provides specific, actionable feedback.

---

### `archivist.py` - The Keeper of the Canon

Once a chapter part is approved, this bot summarizes the key plot events and appends them to the `rwby_plot_events.md` file, ensuring our story's canon is always up-to-date.

---

### The Art Department\

* **`art_director.py`**: Reads the final prose and generates a detailed, artistic prompt for an image.
* **`image_generator.py`**: Takes the art prompt and uses Google's Vertex AI to generate a high-quality image file.

---

### `kohya_ss/` - The AI Training Lab

This is a complete, integrated version of **Kohya's GUI**, the powerful toolkit used for fine-tuning our custom LoRA models. After using `auto_captioner.py` to prepare our `training_images/`, this is the laboratory where we build the specialized "RWBY-brain" for our Image Crafter bot. (Note: Requires a powerful NVIDIA GPU with CUDA.)

---

## 🧪 Environment Setup

**Requirements:**

* Python 3.10+
* All libraries listed in `requirements.txt`

**Install:**

```bash
pip install -r requirements.txt
```

You'll also need a `.env` file in the root directory with your API key and Project ID:

```text
GOOGLE_API_KEY=your_api_key_here
GCP_PROJECT_ID=your-gcp-project-id-here
```

### **CRITICAL: Google Cloud Authentication**

Our `image_generator.py` needs to talk to Google's Vertex AI, which requires a special security handshake\! You must do this **one time** on any machine you run the project on.

**1. Install the Google Cloud CLI:**

* **macOS:** `brew install --cask google-cloud-sdk`
* **Windows:** Download and run the installer from [Google Cloud SDK Installer for Windows](https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe).

**2. Run the Authentication Command:**
After installing, **close and reopen your terminal**, then run this magic command:

```bash
gcloud auth application-default login
```

This will open a browser, ask you to log in to your Google account, and give your computer the secret security badge it needs\!

---

## ✍️ The Automated Workflow

The new workflow is beautifully simple:

1. **Run the Conductor** for the chapter you want to write: `python scripts/conductor.py --chapter-number 1`
2. **Observe the glorious machine at work\!** The Conductor will handle everything from planning to archiving.
3. **(Coming Soon\!) Run the Art Department pipeline** to generate an image for each approved chapter part\!
4. **Review the final chapter and art** in the `output/` directory.

---

## 🗂️ Status

✅ **All Core Bots Online:** Planner, Author, Critic, and Archivist are built and tested.
✅ **Art Department Assembled:** Art Director and Image Crafter are built and tested.
✅ **Full Authentication Protocol Established.**
🟡 **Ready for First Full Chapter Generation\!**

---

## 🔧 Author Notes

Built by Mikey with help from Entrapta (your AI partner\!). Designed to keep the RWBY story alive and emotionally powerful—with a little chaos and a lot of structure.
