# 🚀 AI Content Engine

> **Ignite Ideas. Launch Instantly.**

Turn concepts into polished marketing assets in minutes. Built for creative entrepreneurs, solopreneurs, marketers, and indie founders.

---

## ✨ What It Does

| Asset | Description | Technique |
|---|---|---|
| **Taglines** | Two distinct, audience-tuned tagline variants | Few-shot prompting |
| **Blog Introduction** | 200-word hook that weaves your chosen tagline in naturally | Role-based prompting |
| **Social Posts** | Twitter, Instagram, and LinkedIn copy ready to post | Structured JSON output prompting |
| **Hero Image** | AI-generated product visual (DALL-E 3 via OpenRouter) | Tone-driven visual prompt engineering |
| **Campaign Video** | Image-to-video cinematic motion render (RunwayML) | Cinematic motion prompting |
| **Export Suite** | Single `.zip` download of all generated assets | — |

---

## 🧰 Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io)
- **Text Gen:** OpenRouter (LLaMA 3.3 70B Instruct)
- **Image Gen:** OpenRouter → DALL-E 3
- **Video Gen:** RunwayML (gen4_turbo)
- **Prompt Library:** `image_prompts.py` — premium Grok Imagine / Midjourney / DALL-E 3 prompts

---

## 🏗️ Project Structure

```
ai-content-engine/
├── app.py              # Streamlit UI — campaign generator
├── text_gen.py         # Tagline, blog intro, social post generation
├── image_gen.py        # Hero image generation (DALL-E 3 via OpenRouter)
├── image_prompts.py    # Premium prompt library for hero visuals
├── video_gen.py        # Campaign video rendering (RunwayML)
├── config.py           # Centralised API key & model config
├── requirements.txt    # Python dependencies
├── .env                # Your API keys (git-ignored)
└── README.md           # This file
```

---

## 🚦 Quick Start

### 1. Clone & enter the project

```bash
git clone <your-repo-url>
cd ai-content-engine
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API keys

Create a `.env` file in the `ai-content-engine/` directory:

```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx
RUNWAY_API_KEY=xxxxxxxxxxxx
```

### 4. Launch the app

```bash
streamlit run app.py
```

Open the URL shown in your terminal (typically `http://localhost:8501`).

---

## 🎨 Grok Imagine / Premium Image Prompts

The `image_prompts.py` module ships with a world-class master prompt optimised for **Grok Imagine**, DALL-E 3, Midjourney, and Stable Diffusion. It paints a cinematic, ultra-modern isometric view of the AI Content Engine as a floating UI launchpad in a vibrant cosmic space.

### Quick copy-paste prompts

```python
from image_prompts import get_prompt_variations

variants = get_prompt_variations()

# Default — dark cosmic glassmorphism
print(variants["default (dark premium)"])

# Light theme — cream & rose-gold
print(variants["light theme"])

# With motion — animated floating elements
print(variants["with motion"])

# Light + motion
print(variants["light + motion"])
```

Run the module directly to see all variants:

```bash
python ai-content-engine/image_prompts.py
```

### Prompt variations at a glance

| Variant | Mood | Best for |
|---|---|---|
| `default (dark premium)` | Cosmic dark, neon teal/magenta/gold | Standard hero visual |
| `light theme` | Cream & rose-gold, airy glassmorphism | Lighter brand contexts |
| `with motion` | Adds animated 3D elements & energy lines | Grok Imagine / Pika / Runway |
| `light + motion` | Light background + animated elements | Bright animated hero |

---

## 📦 Export

After generating a campaign, click **⬇️ Export Suite (.zip)** to download a ZIP containing:

- `campaign_copy.txt` — Tagline, blog intro, and all social posts
- `hero_image.png` — The generated hero image (if available)

---

## 🤝 Target Audience

- **Creative entrepreneurs** — Launch branding micro-campaigns
- **Solopreneurs** — Create polished marketing copy in minutes
- **Marketers** — Iterate fast on messaging and visuals
- **Indie founders** — Ship landing page assets without a design team

---

## 📄 License

MIT — free to use, modify, and share.