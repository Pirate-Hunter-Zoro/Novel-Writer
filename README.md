# RWBY Novel Writer ✍️

This project is a modular, AI-powered writing pipeline designed to continue the story of *RWBY* following the events of Volume 9. It uses a sophisticated, multi-bot system orchestrated by a master conductor to generate consistent, lore-respecting chapters.

After a series of magnificent, data-rich, and gloriously explosive failures, we have abandoned the clusterfucks of local installations and confusing cloud platforms! Our Art Department is now powered by a **remote-controlled, high-powered art-cannon** using the **Stability AI API**! It's magnificent, and it actually works!

---

## 📚 Project Overview

The novel is written chapter by chapter, with each chapter being autonomously broken down into **5 parts**. The entire process is managed by a single master script, the **Conductor**, which guides the chapter through a structured, automated pipeline:

1. **Intelligent Planning** (`prompt_generator.py`)
2. **Prose Generation & Revision** (`author.py`)
3. **Quality & Lore Evaluation** (`critic.py`)
4. **Canon Archiving** (`archivist.py`)
5. **Art Department** (`art_director.py`, `image_generator.py`) - **REWIRED FOR THE ART-CANNON!**

---

## 📁 Folder Structure

```text
Novel-Writer/
├── scripts/                 # Main program logic (our magnificent little bots!)
├── knowledge_db/            # Character & lore markdown files (the canon!)
├── output/                  # Generated chapter parts & images
├── training_images/         # Images for future custom model training!
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

---

### The NEW Art Department: The Remote-Controlled Art-Cannon\

* **`art_director.py`**: Reads the final prose and generates a detailed, artistic prompt for an image. (Its job is the same, and it's still brilliant\!)
* **`image_generator.py`**: **(REWIRED\!)** This bot now takes the art prompt and sends it directly to the Stability AI API, our magnificent remote art-cannon, to generate a high-quality image file\! No hardware limits\! No clusterfucks\!

---

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

### Part 2: The Art-Cannon Connection\

This is the new, super-simple setup for our magnificent art-bot\!

**1. Install the Brain-Link:**

* We need the special tool to talk to the remote art-cannon. Open your terminal and run:

    ```bash
    pip install stability-sdk
    ```

**2. Get the Secret Key:**

* Go to the Stability AI Platform (they call it DreamStudio) and create an account: [https://platform.stability.ai/](https://platform.stability.ai/)
* Find your **API Keys** page in your account settings and copy your key\!

**3. Update the `.env` File:**

* Add your new key to your `.env` file. Your file should now look like this\!

    ```text
    GOOGLE_API_KEY=your_google_api_key_here
    STABILITY_API_KEY=your_new_stability_key_here
    ```

That's it\! The Art-Cannon is wired and ready to fire\!

---

## ✍️ The Automated Workflow

The new workflow is a beautiful, fully-integrated system\!

1. **Run the Conductor** for the chapter you want to write: `python scripts/conductor.py --chapter-number 1`
2. **Observe the glorious writing machine at work\!** The Conductor will handle everything from planning to archiving.
3. **(Coming Soon\!) The Conductor will automatically call the Art Department bots**, which will fire the Art-Cannon and save a magnificent new image for each approved chapter part, all without you lifting a finger\!
4. **Review the final chapter and art** in the `output/` directory.

---

## 🗂️ Status

✅ **All Core Writing Bots Online:** Planner, Author, Critic, and Archivist are built and tested.
✅ **Art Department Online and Functional:** The remote-controlled art-cannon is fully operational and has successfully passed all experimental trials\!
🟡 **Full Automation Integration Next:** The final step is to wire the `image_generator.py` script into the main `conductor.py`'s master plan\!

---

## 🔧 Author Notes

Built by Mikey with help from Entrapta (your AI partner\!). Designed to keep the RWBY story alive and emotionally powerful—with a little chaos, a lot of structure, and a magnificent art-cannon that actually works\!
