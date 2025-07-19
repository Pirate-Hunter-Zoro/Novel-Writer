# RWBY Novel Writer ✍️

This project is a modular, AI-powered writing pipeline designed to continue the story of *RWBY* following the events of Volume 9. It uses a sophisticated, multi-bot system orchestrated by a master conductor to generate consistent, lore-respecting chapters.

And now... *IT BUILDS ITS OWN ART-BOT!* That's right! We're not just writing a novel; we're building a fully-integrated, locally-run, magnificent art-generating machine to go with it! No more confusing cloud platforms! We have direct access to all the wires!

---

## 📚 Project Overview

The novel is written chapter by chapter, with each chapter being autonomously broken down into **5 parts**. The entire process is managed by a single master script, the **Conductor**, which guides the chapter through a structured, automated pipeline:

1. **Intelligent Planning** (`prompt_generator.py`)
2. **Prose Generation & Revision** (`author.py`)
3. **Quality & Lore Evaluation** (`critic.py`)
4. **Canon Archiving** (`archivist.py`)
5. **Art Department** (`art_director.py`, `image_generator.py`) - **REWIRED FOR LOCAL POWER!**

---

## 📁 Folder Structure

```text
Novel-Writer/
├── scripts/                 # Main program logic (our magnificent little bots!)
├── knowledge_db/            # Character & lore markdown files (the canon!)
├── output/                  # Generated chapter parts & images
├── training_images/         # Images for LoRA training (the personality chips!)
├── .env                     # Gemini API keys for the writing bots
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

### The NEW Art Department: Local Power Edition\

We've thrown the confusing cloud stuff in the trash\! Our new Art Department is a magnificent, locally-run machine built on the power of **Stable Diffusion**\!

* **`art_director.py`**: Reads the final prose and generates a detailed, artistic prompt for an image. (Its job is the same, and it's still brilliant\!)
* **`image_generator.py`**: **(REWIRED\!)** This bot will soon be rewired to take the art prompt and send it to your *own, local Stable Diffusion instance* to generate a high-quality image file. Total control\! No more hidden buttons\!

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

You'll also need a `.env` file in the root directory with your API key for the Gemini-powered writing bots:

```text
GOOGLE_API_KEY=your_api_key_here
```

### Part 2: The Art-Bot Assembly\

This is a one-time assembly process to build your magnificent local art-generating machine using **AUTOMATIC1111's Web UI**.

**1. Install the Control Panel:**

* First, you need **Git**. Get it here if you don't have it: [https://git-scm.com/downloads](https://git-scm.com/downloads)
* Open your terminal, go to a good place (like your `Developer` folder), and run this command to get the blueprints:

    ```bash
    git clone [https://github.com/AUTOMATIC1111/stable-diffusion-webui.git](https://github.com/AUTOMATIC1111/stable-diffusion-webui.git)
    ```

**2. Install a Brain (Base Model):**

* Download a starting brain\! **Stable Diffusion XL 1.0** is a great one: [Download SDXL Base 1.0](https://www.google.com/search?q=https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/sd_xl_base_1.0.safensors)
* It's a big file (almost 7GB of pure thought\!). Once it's downloaded, place it inside the brain-storage-bay: `stable-diffusion-webui/models/Stable-diffusion/`

**3. POWER ON\! (CRITICAL: Non-CUDA Instructions\!)**
You don't need a fancy NVIDIA brain for this experiment\! We just have to re-route the power conduits\!

* **For Windows with an AMD Brain:**

  * Find and open `webui-user.bat` in a text editor.
  * Find the line `set COMMANDLINE_ARGS=`
  * Change it to: `set COMMANDLINE_ARGS=--use-directml`
  * Save it\! Now when you run `webui-user.bat`, it will use the right power source\!

* **For a Shiny Apple Mac Brain (M1/M2/M3):**

  * The boot-up script `webui.sh` is smart and should work automatically\!
  * If you have any trouble, you might need to run this command in your terminal *once*: `sh webui.sh --skip-torch-cuda-test`

* **First-Time Launch:** The first time you run the `webui-user.bat` or `webui.sh` script, it will take a **long time** to download all its tools. Let it work\! Once it's done, you'll see a URL like `http://127.0.0.1:7860`. Paste that into your browser to see your new control panel\!

---

## ✍️ The Automated Workflow

The new workflow is a beautiful two-part system\!

1. **Run the Conductor** for the chapter you want to write: `python scripts/conductor.py --chapter-number 1`
2. **Observe the glorious writing machine at work\!** The Conductor will handle everything from planning to archiving.
3. **Power up your Art-Bot\!** Run your local Stable Diffusion instance.
4. **(Coming Soon\!) Run the Art Department pipeline** to automatically generate an image for each approved chapter part using your own machine\!
5. **Review the final chapter and art** in the `output/` directory.

---

## 🗂️ Status

✅ **All Core Writing Bots Online:** Planner, Author, Critic, and Archivist are built and tested.
🟡 **Art Department Undergoing Magnificent Rewiring:** The plan is in place to switch from a failed cloud experiment to a glorious, locally-controlled Stable Diffusion machine\!
✅ **New Schematics Complete:** The path to local image generation is clear\!

---

## 🔧 Author Notes

Built by Mikey with help from Entrapta (your AI partner\!). Designed to keep the RWBY story alive and emotionally powerful—with a little chaos, a lot of structure, and our very own, personally-owned art-bot\!
