import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChemLens",
    page_icon="⚗️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #111118;
    --surface2: #1a1a24;
    --border: #2a2a3a;
    --accent: #00ff88;
    --accent2: #7c3aed;
    --accent3: #ff6b35;
    --text: #e8e8f0;
    --muted: #6b6b80;
}

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse at 10% 20%, rgba(124,58,237,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(0,255,136,0.06) 0%, transparent 50%),
        var(--bg) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 2rem 0 1rem;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(124,58,237,0.1));
    border: 1px solid rgba(0,255,136,0.3);
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    padding: 0.3rem 0.9rem;
    border-radius: 2rem;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
}
.hero-title {
    font-size: clamp(2.5rem, 8vw, 4rem);
    font-weight: 800;
    line-height: 1;
    margin: 0.3rem 0;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent) 50%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.03em;
}
.hero-sub {
    color: var(--muted);
    font-size: 0.9rem;
    font-family: 'Space Mono', monospace;
    margin-top: 0.3rem;
}

/* ── Result Card ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem;
    margin-top: 1.2rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3));
}
.result-tag {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(0,255,136,0.08);
    border: 1px solid rgba(0,255,136,0.2);
    padding: 0.2rem 0.7rem;
    border-radius: 4px;
    margin-bottom: 1rem;
}
.result-tag.retro {
    color: #a78bfa;
    background: rgba(124,58,237,0.08);
    border-color: rgba(124,58,237,0.2);
}
.result-tag.compound {
    color: #fb923c;
    background: rgba(255,107,53,0.08);
    border-color: rgba(255,107,53,0.2);
}

/* ── Streamlit overrides ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #00cc6a) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(0,255,136,0.25) !important;
}

[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.1) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
.stTabs [aria-selected="true"] {
    background: var(--surface2) !important;
    color: var(--text) !important;
}

[data-testid="stCameraInput"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
}

.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

.stNumberInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Space Mono', monospace !important;
}

.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.2rem 0;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Session state init ─────────────────────────────────────────────────────────
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "analysis_mode" not in st.session_state:
    st.session_state.analysis_mode = None
if "history" not in st.session_state:
    st.session_state.history = []
if "current_image" not in st.session_state:
    st.session_state.current_image = None


# ── Configure Gemini Securely ──────────────────────────────────────────────────
SYSTEM_INSTRUCTION = """You are an expert chemistry assistant with deep knowledge of 
organic, inorganic, physical, and analytical chemistry. You provide accurate, 
structured, and educational chemistry analysis. Always use proper chemical notation."""

# Safely fetch the API key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("🚨 API key not found! Developer: Please add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
except Exception as e:
    st.error(f"API configuration error: {e}")
    st.stop()


# ── Sidebar — Settings + History ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚗️ ChemLens")
    st.markdown("---")

    # Explain level toggle
    st.markdown("**🎓 Explanation Level**")
    explain_level = st.select_slider(
        label="Level",
        options=["Beginner", "Intermediate", "Expert"],
        value="Intermediate",
        label_visibility="collapsed"
    )

    st.markdown("---")

    # History
    st.markdown("**📋 Analysis History**")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-10:])):
            with st.expander(f"{item['icon']} {item['mode']} — {item['time']}"):
                st.text(item["result"][:300] + "..." if len(item["result"]) > 300 else item["result"])
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()
    else:
        st.caption("No analyses yet.")


# ── Main UI ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚗️ AI-Powered Chemistry</div>
    <div class="hero-title">ChemLens</div>
    <div class="hero-sub">Point. Snap. Understand.</div>
</div>
""", unsafe_allow_html=True)


# ── Mode selector ──────────────────────────────────────────────────────────────
st.markdown("#### Select Analysis Mode")
mode = st.segmented_control(
    label="Mode",
    options=["⚗️ Reaction Predictor", "🔄 Retrosynthesis", "🔬 Compound Identifier"],
    default="⚗️ Reaction Predictor",
    label_visibility="collapsed"
)

if mode is None:
    mode = "⚗️ Reaction Predictor"

is_reaction = "Reaction" in mode
is_retro    = "Retro" in mode
is_compound = "Compound" in mode

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)


# ── Yield calculator (reaction mode only) ─────────────────────────────────────
mass1, mass2 = None, None
if is_reaction:
    with st.expander("⚖️ Optional: Yield Calculator — enter reactant masses"):
        col1, col2 = st.columns(2)
        with col1:
            mass1 = st.number_input("Reactant 1 mass (g)", min_value=0.0, step=0.1, format="%.2f")
        with col2:
            mass2 = st.number_input("Reactant 2 mass (g)", min_value=0.0, step=0.1, format="%.2f")


# ── Image input ───────────────────────────────────────────────────────────────
if is_reaction:
    label = "📸 Capture or Upload Reactants"
    hint  = "Photo of written/drawn reactants — whiteboard, textbook, paper"
elif is_retro:
    label = "🔬 Capture or Upload Target Molecule"
    hint  = "Photo of the molecule you want to synthesize"
else:
    label = "🧪 Capture or Upload Compound"
    hint  = "Photo of any chemical structure or compound name"

st.markdown(f"**{label}**")
st.caption(hint)

tab_cam, tab_gal = st.tabs(["📷 Camera", "🖼️ Gallery / Upload"])

with tab_cam:
    cam = st.camera_input(label="Camera", label_visibility="collapsed", key=f"cam_{mode}")
    if cam:
        st.session_state.current_image = Image.open(io.BytesIO(cam.getvalue()))

with tab_gal:
    upl = st.file_uploader(
        label="Upload",
        type=["jpg", "jpeg", "png", "webp", "bmp"],
        label_visibility="collapsed",
        key=f"upl_{mode}"
    )
    if upl:
        st.session_state.current_image = Image.open(io.BytesIO(upl.getvalue()))


# ── Build prompt based on mode + level ────────────────────────────────────────
LEVEL_INSTRUCTIONS = {
    "Beginner":     "Use simple language. Avoid jargon. Explain every term. Target a high school student.",
    "Intermediate": "Use standard chemistry terminology. Assume first/second year university level.",
    "Expert":       "Use advanced IUPAC nomenclature, detailed mechanisms, stereochemical considerations. Target a PhD chemist.",
}

level_note = LEVEL_INSTRUCTIONS[explain_level]

REACTION_PROMPT = f"""
Analyze the image. It shows chemical reactants.
Explanation level: {explain_level}. {level_note}

Respond in this EXACT format:

🔬 IDENTIFIED REACTANTS
[List all reactants identified]

⚗️ PREDICTED REACTION
[Balanced chemical equation]

📋 REACTION TYPE
[e.g., SN2 Substitution, Aldol Addition, Redox, etc.]

🌡️ RECOMMENDED CONDITIONS
• Temperature: 
• Catalyst: 
• Solvent: 
• Pressure: 
• Approximate time: 

⚡ MECHANISM OVERVIEW
[Numbered step-by-step mechanism]

🧪 EXPECTED PRODUCTS
[All products including byproducts]

{"⚖️ YIELD CALCULATION" + chr(10) + f"Reactant 1 mass: {mass1}g | Reactant 2 mass: {mass2}g" + chr(10) + "[Identify limiting reagent. Calculate theoretical yield step by step.]" + chr(10) if (isinstance(mass1, (int, float)) and isinstance(mass2, (int, float)) and mass1 > 0 and mass2 > 0) else ""}
⚠️ SAFETY NOTES
[Key hazards and lab precautions]

📊 EXPECTED YIELD & NOTES
[Yield range and practical notes]
"""

RETRO_PROMPT = f"""
Analyze the molecular structure in the image. Perform a retrosynthetic analysis.
Explanation level: {explain_level}. {level_note}

Respond in this EXACT format:

🎯 TARGET MOLECULE
[Name and identify the compound]

🔄 RETROSYNTHETIC DISCONNECTIONS

Disconnection 1:
• Bond broken: 
• Synthon: 
• Synthetic equivalent (reagent): 
• Transform type: 

Disconnection 2:
• Bond broken: 
• Synthon: 
• Synthetic equivalent (reagent): 
• Transform type: 

[Continue for all necessary disconnections]

🧱 STARTING MATERIALS
[List all commercially available starting materials]

📍 FORWARD SYNTHESIS ROUTE
[Numbered steps from starting materials to target]

🔀 ALTERNATIVE ROUTE
[One alternative retrosynthetic approach]

💡 STRATEGIC NOTES
[Stereochemistry, protecting groups, selectivity]

⚠️ CHALLENGING STEPS
[Difficult transformations and solutions]
"""

COMPOUND_PROMPT = f"""
Identify and analyze the chemical compound or structure shown in the image.
Explanation level: {explain_level}. {level_note}

Respond in this EXACT format:

🔬 COMPOUND IDENTIFICATION
• IUPAC Name: 
• Common Name(s): 
• Molecular Formula: 
• Molecular Weight: 

📐 STRUCTURE & PROPERTIES
• Structure type: 
• Functional groups: 
• Molecular geometry: 
• Polarity: 

🌡️ PHYSICAL PROPERTIES
• Melting point: 
• Boiling point: 
• Solubility: 
• Appearance: 

⚗️ CHEMICAL PROPERTIES
• Reactivity: 
• Common reactions: 
• Stability: 

🏭 COMMON USES
[Industrial, pharmaceutical, laboratory uses]

⚠️ HAZARD INFORMATION
• GHS hazard class: 
• Key risks: 
• First aid measures: 
• Storage requirements: 

📚 ADDITIONAL NOTES
[Interesting chemistry or context about this compound]
"""

PROMPTS = {
    "reaction": REACTION_PROMPT,
    "retro":    RETRO_PROMPT,
    "compound": COMPOUND_PROMPT,
}
ICONS      = {"reaction": "⚗️", "retro": "🔄", "compound": "🔬"}
TAGS       = {"reaction": "REACTION ANALYSIS", "retro": "RETROSYNTHETIC ANALYSIS", "compound": "COMPOUND IDENTIFICATION"}
TAG_CLASSES = {"reaction": "", "retro": "retro", "compound": "compound"}

mode_key = "reaction" if is_reaction else ("retro" if is_retro else "compound")


# ── Preview + Analyze ─────────────────────────────────────────────────────────
if st.session_state.current_image:
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(st.session_state.current_image, caption="Your image", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    btn_labels = {
        "reaction": "⚗️ Predict Reaction",
        "retro":    "🔄 Analyze Retrosynthesis",
        "compound": "🔬 Identify Compound",
    }

    button_clicked = st.button(btn_labels[mode_key], use_container_width=True)

    # 1. GENERATION + STREAMING — only on button click
    if button_clicked:
        try:
            with st.spinner("Analyzing with Gemini Vision..."):
                response = model.generate_content(
                    [PROMPTS[mode_key], st.session_state.current_image],
                    stream=True
                )

            tag_class = TAG_CLASSES[mode_key]
            tag_text  = TAGS[mode_key]

            st.markdown(f"""
            <div class="result-card" style="padding-bottom: 0;">
                <div class="result-tag {tag_class}">{tag_text}</div>
            </div>
            """, unsafe_allow_html=True)

            # Stream with native Streamlit
            def stream_response(r):
                for chunk in r:
                    if chunk.text:
                        yield chunk.text

            full_text = st.write_stream(stream_response(response))

            # Persist to session state
            st.session_state.analysis_result = full_text
            st.session_state.analysis_mode   = mode_key

            from datetime import datetime
            st.session_state.history.append({
                "mode":   TAGS[mode_key],
                "icon":   ICONS[mode_key],
                "result": full_text,
                "time":   datetime.now().strftime("%H:%M"),
            })

        except Exception as e:
            err = str(e)
            if "quota" in err.lower() or "429" in err:
                st.error("⚠️ API quota exceeded. Wait a minute or check your usage at aistudio.google.com")
            else:
                st.error(f"Analysis failed: {err}\n\nTry a clearer image with better lighting.")

    # 2. STATIC RENDERING — on every rerun
    elif st.session_state.analysis_result and st.session_state.analysis_mode == mode_key:
        tag_class = TAG_CLASSES[mode_key]
        tag_text  = TAGS[mode_key]

        st.markdown(f"""
        <div class="result-card" style="padding-bottom: 0; border-bottom-left-radius: 0;
             border-bottom-right-radius: 0; border-bottom: none;">
            <div class="result-tag {tag_class}">{tag_text}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(st.session_state.analysis_result)

    # 3. DOWNLOAD + CLEAR — always visible when result exists
    if st.session_state.analysis_result and st.session_state.analysis_mode == mode_key:
        st.markdown("<br>", unsafe_allow_html=True)
        col_dl, col_clear = st.columns([3, 1])
        with col_dl:
            st.download_button(
                label="📥 Download Analysis",
                data=st.session_state.analysis_result,
                file_name=f"chemlens_{mode_key}_analysis.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_clear:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.analysis_result = None
                st.session_state.analysis_mode   = None
                st.rerun()

else:
    hints = {
        "reaction": "📸 Snap or upload an image of your reactants to begin",
        "retro":    "🔬 Snap or upload the target molecule structure",
        "compound": "🧪 Snap or upload any chemical compound",
    }
    st.markdown(f"""
    <div style="text-align:center; padding:2rem; color:#6b6b80;
                font-family:'Space Mono',monospace; font-size:0.8rem;
                border:1px dashed #2a2a3a; border-radius:12px; margin-top:1rem;">
        {hints[mode_key]}
    </div>
    """, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2rem 0 0.5rem; color:#3a3a4a;
            font-family:'Space Mono',monospace; font-size:0.62rem; letter-spacing:0.1em;">
    CHEMLENS v2 · GEMINI 1.5 FLASH · FOR EDUCATIONAL USE
</div>
""", unsafe_allow_html=True)
