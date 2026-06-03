"""
SmartLens - Gradio Web Application
Run: python app.py
Then open http://localhost:7860 in your browser.
"""

import gradio as gr
from PIL import Image
from caption_engine import generate_captions, translate_to_hindi


# ─── Core inference function ───────────────────────────────────────────────────
def analyze_image(image, translate: bool):
    if image is None:
        return "Please upload an image.", "", "", ""

    pil_image = Image.fromarray(image)
    captions = generate_captions(pil_image, num_captions=3)

    # Pad in case fewer captions returned
    while len(captions) < 3:
        captions.append("—")

    if translate:
        hindi = translate_to_hindi(captions[0])
    else:
        hindi = "Enable Hindi translation above to see this."

    return captions[0], captions[1], captions[2], hindi


# ─── Gradio UI ─────────────────────────────────────────────────────────────────
with gr.Blocks(
    title="SmartLens – AI Image Caption Generator",
    theme=gr.themes.Soft(primary_hue="indigo", neutral_hue="slate"),
    css="""
    #title { text-align: center; margin-bottom: 0.5em; }
    #subtitle { text-align: center; color: #6366f1; margin-bottom: 1.5em; }
    .caption-box textarea { font-size: 1.05em !important; }
    """,
) as demo:

    gr.Markdown("# 🔍 SmartLens", elem_id="title")
    gr.Markdown(
        "**Contextual Image Caption Generator** · Powered by BLIP (Salesforce) · "
        "Runs fully offline · No API key needed",
        elem_id="subtitle",
    )

    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(label="Upload Image", type="numpy", height=320)
            translate_toggle = gr.Checkbox(label="🌐 Also translate best caption to Hindi", value=True)
            submit_btn = gr.Button("✨ Generate Captions", variant="primary", size="lg")

        with gr.Column(scale=1):
            gr.Markdown("### Generated Captions")
            cap1 = gr.Textbox(label="🥇 Best Caption (Greedy)", elem_classes="caption-box")
            cap2 = gr.Textbox(label="🥈 Alternative Caption 1", elem_classes="caption-box")
            cap3 = gr.Textbox(label="🥉 Alternative Caption 2", elem_classes="caption-box")
            hindi_out = gr.Textbox(label="🇮🇳 Hindi Translation (Best Caption)", elem_classes="caption-box")

    submit_btn.click(
        fn=analyze_image,
        inputs=[image_input, translate_toggle],
        outputs=[cap1, cap2, cap3, hindi_out],
    )

    gr.Examples(
        examples=[["samples/dog.jpg"], ["samples/city.jpg"]],
        inputs=[image_input],
        label="Try sample images",
    )

    gr.Markdown(
        "---\n"
        "**How it works:** BLIP (Bootstrapping Language-Image Pre-training) by Salesforce "
        "uses a Vision Transformer encoder paired with a language model decoder. "
        "Beam search generates diverse, high-quality captions from a single image."
    )

if __name__ == "__main__":
    demo.launch(share=False)
