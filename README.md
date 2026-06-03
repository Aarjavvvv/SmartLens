# 🔍 SmartLens — Contextual Image Caption Generator

> Generate rich, diverse captions for any image — with multilingual support and BLEU evaluation. Runs fully offline. No API key needed.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![HuggingFace](https://img.shields.io/badge/HuggingFace-BLIP-yellow?logo=huggingface)
![Gradio](https://img.shields.io/badge/UI-Gradio-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **BLIP Model** | State-of-the-art vision-language model by Salesforce |
| 🖼️ **3 Diverse Captions** | Greedy + diverse beam search for varied descriptions |
| 🌐 **Hindi Translation** | Translates best caption to Hindi (free, no API) |
| 📊 **BLEU Evaluation** | Quantitative caption quality scoring |
| 🎛️ **Gradio Web UI** | Clean, interactive interface — launch with one command |
| ⚡ **No Dataset Needed** | Fully pretrained — works on any image immediately |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/SmartLens.git
cd SmartLens
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3a. Run the Web App
```bash
python app.py
```
Then open **http://localhost:7860** in your browser.

### 3b. Run the Notebook
```bash
jupyter notebook SmartLens_Notebook.ipynb
```

---

## 🏗️ Architecture

```
Input Image
     │
     ▼
┌─────────────────────────────┐
│  BLIP Vision Encoder        │  ← ViT-B/16 (Vision Transformer)
│  (Image → Feature vectors)  │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  BLIP Language Decoder      │  ← GPT-style transformer
│  (Features → Caption text)  │
└─────────────┬───────────────┘
              │
     ┌────────┴─────────┐
     ▼                  ▼
Greedy Caption    Diverse Beam Search
(Best / most      (2 alternative
 confident)        captions)
     │
     ▼
Hindi Translation (deep-translator)
     │
     ▼
BLEU Score (vs. reference caption)
```

---

## 📸 Sample Output

**Input:** Photo of a dog playing in a park  
**Caption 1 (Greedy):** *"a dog playing with a ball in a green park"*  
**Caption 2 (Beam):** *"a brown dog running on grass with a toy"*  
**Caption 3 (Beam):** *"a dog enjoying outdoor playtime in a sunny field"*  
**Hindi:** *"एक कुत्ता हरे पार्क में गेंद के साथ खेल रहा है"*  
**BLEU-4:** 0.42

---

## 📂 Project Structure

```
SmartLens/
├── app.py                    # Gradio web application
├── caption_engine.py         # Core model loading + inference
├── SmartLens_Notebook.ipynb  # Full walkthrough notebook
├── requirements.txt
├── samples/                  # Sample images for demo
└── README.md
```

---

## 🧠 Model Details

**BLIP** (Bootstrapping Language-Image Pre-training) is a vision-language model developed by Salesforce Research. It uses:
- A **Vision Transformer (ViT)** as the image encoder
- A **causal language model** as the text decoder  
- Pre-trained on 129M image-text pairs from the web

Reference: [BLIP: Bootstrapping Language-Image Pre-training (ICML 2022)](https://arxiv.org/abs/2201.12086)

---

## 🔧 Tech Stack

- `transformers` — BLIP model from HuggingFace
- `torch` — PyTorch for inference
- `gradio` — Interactive web UI
- `deep-translator` — Free Hindi translation
- `nltk` — BLEU score computation
- `Pillow` — Image preprocessing

---

## 📄 License

MIT License — free to use, modify, and distribute.
