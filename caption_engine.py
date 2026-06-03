"""
SmartLens - Caption Engine
Uses BLIP (Bootstrapping Language-Image Pre-training) from Salesforce via HuggingFace.
No API key required. Runs 100% locally after first download.
"""

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# ─── Load model once at startup ───────────────────────────────────────────────
MODEL_NAME = "Salesforce/blip-image-captioning-base"

print("Loading BLIP model (first run downloads ~1GB, cached after)...")
processor = BlipProcessor.from_pretrained(MODEL_NAME)
model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()
print(f"Model loaded on {device} ✓")


# ─── Caption generation ────────────────────────────────────────────────────────
def generate_captions(image: Image.Image, num_captions: int = 3) -> list[str]:
    """
    Generate multiple diverse captions for an image using beam search + sampling.
    Returns a list of caption strings.
    """
    import time
    image = image.convert("RGB")
    inputs = processor(image, return_tensors="pt").to(device)

    captions = []
    total_start = time.time()

    # Caption 1: Greedy / most confident caption
    print("  [1/3] Generating greedy caption...", flush=True)
    t = time.time()
    with torch.no_grad():
        greedy_ids = model.generate(**inputs, max_new_tokens=50)
    captions.append(processor.decode(greedy_ids[0], skip_special_tokens=True))
    print(f"        Done in {time.time()-t:.2f}s → "{captions[0]}"", flush=True)

    # Caption 2: Beam search (most probable sequence)
    print("  [2/3] Beam search (5 beams)...", flush=True)
    t = time.time()
    with torch.no_grad():
        beam_ids = model.generate(
            **inputs,
            num_beams=5,
            num_return_sequences=1,
            max_new_tokens=60,
        )
    cap = processor.decode(beam_ids[0], skip_special_tokens=True)
    if cap not in captions:
        captions.append(cap)
    print(f"        Done in {time.time()-t:.2f}s → "{cap}"", flush=True)

    # Caption 3: Sampling with temperature for variety
    print("  [3/3] Temperature sampling (top_p=0.9)...", flush=True)
    t = time.time()
    with torch.no_grad():
        sample_ids = model.generate(
            **inputs,
            do_sample=True,
            top_p=0.9,
            temperature=1.2,
            max_new_tokens=60,
        )
    cap = processor.decode(sample_ids[0], skip_special_tokens=True)
    if cap not in captions:
        captions.append(cap)
    print(f"        Done in {time.time()-t:.2f}s → "{cap}"", flush=True)

    print(f"  Total inference time: {time.time()-total_start:.2f}s", flush=True)
    return captions[:num_captions]


def translate_to_hindi(text: str) -> str:
    """
    Translate English caption to Hindi using deep_translator (free, no API key).
    Falls back gracefully if translation fails.
    """
    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source="en", target="hi").translate(text)
        return translated
    except Exception as e:
        return f"(Translation unavailable: {e})"
