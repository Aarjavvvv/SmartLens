"""
SmartLens - Gradio Web Application (Redesigned UI)
Run: python app.py
Then open http://localhost:7860
"""

import gradio as gr
from PIL import Image
from caption_engine import generate_captions, translate_to_hindi


def analyze_image(image, translate: bool):
    if image is None:
        return "Please upload an image.", "", "", ""
    pil_image = Image.fromarray(image)
    captions = generate_captions(pil_image, num_captions=3)
    while len(captions) < 3:
        captions.append("—")
    hindi = translate_to_hindi(captions[0]) if translate else "Enable Hindi translation to see this."
    return captions[0], captions[1], captions[2], hindi


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root & page ── */
body, .gradio-container {
    background: #F0EDE6 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.gradio-container { max-width: 1100px !important; margin: 0 auto !important; padding: 0 2rem !important; }

/* ── Hide default gradio header chrome ── */
footer { display: none !important; }
.gr-prose h1, .gr-prose h2, .gr-prose h3 { font-family: 'Syne', sans-serif !important; }

/* ── Hero header ── */
#smartlens-header {
    padding: 3.5rem 0 1.5rem;
    border-bottom: 1.5px solid #C8C3B8;
    margin-bottom: 2.5rem;
}
#smartlens-header p { margin: 0; }
#smartlens-header .eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8A8479;
    margin-bottom: 0.6rem;
}
#smartlens-header h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.8rem, 6vw, 4.8rem) !important;
    font-weight: 800 !important;
    line-height: 1.0 !important;
    color: #1A1916 !important;
    letter-spacing: -0.03em;
    margin: 0 0 1rem !important;
}
#smartlens-header .sub {
    font-size: 14px;
    color: #6B6860;
    font-weight: 300;
    letter-spacing: 0.02em;
}

/* ── Upload zone ── */
.upload-zone .wrap { 
    border: 1.5px dashed #B8B3A8 !important;
    border-radius: 4px !important;
    background: #EAE7DF !important;
    transition: border-color 0.2s, background 0.2s;
}
.upload-zone .wrap:hover {
    border-color: #1A1916 !important;
    background: #E4E1D8 !important;
}
.upload-zone img { border-radius: 4px !important; }

/* ── Section label ── */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8A8479;
    margin-bottom: 1rem;
    display: block;
}

/* ── Caption cards (textboxes) ── */
.caption-card textarea,
.caption-card input {
    background: #FFFFFF !important;
    border: 1px solid #D8D3CB !important;
    border-radius: 4px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    color: #1A1916 !important;
    padding: 14px 16px !important;
    line-height: 1.6 !important;
    box-shadow: none !important;
    transition: border-color 0.2s;
}
.caption-card textarea:focus, .caption-card input:focus {
    border-color: #1A1916 !important;
    outline: none !important;
}
.caption-card label span {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #8A8479 !important;
}

/* ── Hindi card accent ── */
.hindi-card textarea {
    border-left: 3px solid #1A1916 !important;
    background: #F5F2EB !important;
    font-style: italic !important;
}

/* ── Generate button ── */
#generate-btn {
    background: #1A1916 !important;
    color: #F0EDE6 !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 14px 28px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background 0.2s, transform 0.1s;
    margin-top: 0.75rem !important;
}
#generate-btn:hover { background: #333028 !important; }
#generate-btn:active { transform: scale(0.985); }

/* ── Checkbox ── */
.translate-check label span {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: #4A4840 !important;
}
.translate-check input[type=checkbox] { accent-color: #1A1916 !important; }

/* ── Info strip ── */
#info-strip {
    border-top: 1px solid #C8C3B8;
    margin-top: 3rem;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    display: flex;
    gap: 3rem;
    flex-wrap: wrap;
}
#info-strip .info-item { flex: 1; min-width: 160px; }
#info-strip .info-label {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8A8479;
    margin-bottom: 4px;
}
#info-strip .info-val {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 600;
    color: #1A1916;
}

/* ── Two-column layout refinement ── */
.main-row { gap: 2.5rem !important; align-items: flex-start !important; }
"""

with gr.Blocks(title="SmartLens", css=CSS) as demo:

    # ── Header ──────────────────────────────────────────────────────────────
    gr.HTML("""
    <div id="smartlens-header">
        <p class="eyebrow">AI · Computer Vision · NLP</p>
        <h1>SmartLens</h1>
        <p class="sub">Contextual image captioning · BLIP by Salesforce · Beam search · Hindi translation</p>
    </div>
    """)

    # ── Main layout ──────────────────────────────────────────────────────────
    with gr.Row(elem_classes="main-row"):

        with gr.Column(scale=5):
            gr.HTML('<span class="section-label">Upload image</span>')
            image_input = gr.Image(
                label="", type="numpy", height=340,
                elem_classes="upload-zone", show_label=False
            )
            translate_toggle = gr.Checkbox(
                label="Translate best caption to Hindi",
                value=True, elem_classes="translate-check"
            )
            submit_btn = gr.Button(
                "Generate Captions", elem_id="generate-btn", variant="primary"
            )

        with gr.Column(scale=7):
            gr.HTML('<span class="section-label">Generated captions</span>')
            cap1 = gr.Textbox(label="Best caption", elem_classes="caption-card", lines=2)
            cap2 = gr.Textbox(label="Alternative 01", elem_classes="caption-card", lines=2)
            cap3 = gr.Textbox(label="Alternative 02", elem_classes="caption-card", lines=2)
            gr.HTML('<span class="section-label" style="margin-top:1rem">Hindi translation</span>')
            hindi_out = gr.Textbox(label="हिन्दी", elem_classes="caption-card hindi-card", lines=2)

    # ── Info strip ───────────────────────────────────────────────────────────
    gr.HTML("""
    <div id="info-strip">
        <div class="info-item">
            <div class="info-label">Model</div>
            <div class="info-val">BLIP Base</div>
        </div>
        <div class="info-item">
            <div class="info-label">Encoder</div>
            <div class="info-val">ViT-B / 16</div>
        </div>
        <div class="info-item">
            <div class="info-label">Captions</div>
            <div class="info-val">3 via beam search</div>
        </div>
        <div class="info-item">
            <div class="info-label">Translation</div>
            <div class="info-val">EN → Hindi</div>
        </div>
        <div class="info-item">
            <div class="info-label">API key needed</div>
            <div class="info-val">None</div>
        </div>
    </div>
    """)

    submit_btn.click(
        fn=analyze_image,
        inputs=[image_input, translate_toggle],
        outputs=[cap1, cap2, cap3, hindi_out],
    )

if __name__ == "__main__":
    demo.launch(share=False)
