import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
st.sidebar.warning(f"SDK Version: {genai.__version__}")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChemLens Pro",
    page_icon="⚗️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── 3D Asset URLs (Microsoft Fluent) ───────────────────────────────────────────
URL_FLASK = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Alembic/3D/alembic_3d.png"
URL_RETRO = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Microscope/3D/microscope_3d.png"
URL_COMP  = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Test%20tube/3D/test_tube_3d.png"
URL_CAM   = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Camera%20with%20flash/3D/camera_with_flash_3d.png"
URL_GAL   = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Framed%20picture/3D/framed_picture_3d.png"
URL_PRO   = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/Sparkles/3D/sparkles_3d.png"

# ── Custom CSS with Animations & 3D Styling ────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #13131c;
    --surface2: #1e1e2d;
    --border: #2a2a3a;
    --accent: #00e57a;
    --accent-dark: #009952;
    --accent2: #8b5cf6;
    --accent3: #ff6b35;
    --text: #e8e8f0;
    --muted: #8b8b9e;
}

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

/* 3D Ambient Lighting */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 15% 20%, rgba(139, 92, 246, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(0, 229, 122, 0.1) 0%, transparent 40%),
        var(--bg) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 5px 0 20px rgba(0,0,0,0.3);
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Smooth 3D Icon Animations */
.icon-3d {
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.3s ease;
    filter: drop-shadow(0 10px 15px rgba(0,0,0,0.4));
}
.icon-3d:hover {
    transform: translateY(-8px) scale(1.08);
    filter: drop-shadow(0 15px 25px rgba(0,229,122,0.3));
}

/* ── Pro 3D Physical Buttons ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    transition: all 0.15s cubic-bezier(0.4, 0.0, 0.2, 1) !important;
    margin-bottom: 8px !important; /* Space for the 3D push */
}

/* Primary Button (Green) */
button[kind="primary"] {
    background: linear-gradient(145deg, var(--accent), var(--accent-dark)) !important;
    color: #050508 !important;
    box-shadow: 
        0 6px 0 #006636, 
        0 12px 20px rgba(0,229,122,0.3),
        inset 0 2px 2px rgba(255,255,255,0.4) !important;
}
button[kind="primary"]:hover { filter: brightness(1.1); }
button[kind="primary"]:active {
    transform: translateY(6px) scale(0.98) !important;
    box-shadow: 
        0 0 0 #006636, 
        0 4px 10px rgba(0,229,122,0.2),
        inset 0 2px 2px rgba(255,255,255,0.4) !important;
}

/* Secondary Button (Dark) */
button[kind="secondary"] {
    background: linear-gradient(145deg, var(--surface2), var(--surface)) !important;
    color: var(--text) !important;
    box-shadow: 
        0 6px 0 #0a0a0f, 
        0 12px 20px rgba(0,0,0,0.4),
        inset 0 2px 2px rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
}
button[kind="secondary"]:hover { border-color: rgba(255,255,255,0.15) !important; }
button[kind="secondary"]:active {
    transform: translateY(6px) scale(0.98) !important;
    box-shadow: 
        0 0 0 #0a0a0f, 
        0 4px 10px rgba(0,0,0,0.4),
        inset 0 2px 2px rgba(255,255,255,0.05) !important;
}

/* ── Result Card (Glassmorphism) ── */
.result-card {
    background: rgba(19, 19, 28, 0.6);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.8rem;
    margin-top: 1.2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
    animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3));
}
.result-tag {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 700;
    color: var(--accent);
    background: rgba(0,229,122,0.1);
    border: 1px solid rgba(0,229,122,0.3);
    padding: 0.3rem 0.8rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    box-shadow: 0 4px 10px rgba(0,229,122,0.1);
}
.result-tag.retro { color: #a78bfa; background: rgba(139,92,246,0.1); border-color: rgba(139,92,246,0.3); }
.result-tag.compound { color: #fb923c; background: rgba(255,107,53,0.1); border-color: rgba(255,107,53,0.3); }

/* ── Inputs ── */
[data-testid="stFileUploader"] {
    background: rgba(30, 30, 45, 0.4) !important;
    border: 2px dashed rgba(255,255,255,0.1) !important;
    border-radius: 16px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
    background: rgba(0,229,122,0.05) !important;
}
[data-testid="stCameraInput"] {
    background: var(--surface) !important;
    border: 2px solid var(--border) !important;
    border-radius: 16px !important;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    animation: scaleIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}
.section-divider { border: none; border-top: 1px solid rgba(255,255,255,0.05); margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)


# ── Session state init ─────────────────────────────────────────────────────────
if "analysis_result" not in st.session_state: st.session_state.analysis_result = None
if "analysis_mode" not in st.session_state: st.session_state.analysis_mode = None
if "history" not in st.session_state: st.session_state.history = []
if "current_image" not in st.session_state: st.session_state.current_image = None

# New UI states
if "mode" not in st.session_state: st.session_state.mode = "reaction"
if "input_method" not in st.session_state: st.session_state.input_method = "cam"
if "camera_active" not in st.session_state: st.session_state.camera_active = False


# ── Configure Gemini Securely ──────────────────────────────────────────────────
SYSTEM_INSTRUCTION = """You are an expert chemistry assistant with deep knowledge of 
organic, inorganic, physical, and analytical chemistry. You provide accurate, 
structured, and educational chemistry analysis. Always use proper chemical notation."""

_secret_key = st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, "secrets") else ""

try:
    if not _secret_key:
        st.error("🚨 API key not found! Developer: Please add GEMINI_API_KEY to Streamlit Secrets.")
        st.stop()
    genai.configure(api_key=_secret_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=SYSTEM_INSTRUCTION
    )
except Exception as e:
    st.error(f"API configuration error: {e}")
    st.stop()


# ── Sidebar — Settings + History ───────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### <img src='{URL_PRO}' width='24' style='vertical-align: middle; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));'> ChemLens Pro", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("**🎓 Explanation Level**")
    explain_level = st.select_slider(
        label="Level",
        options=["Beginner", "Intermediate", "Expert"],
        value="Intermediate",
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**📋 Analysis History**")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-10:])):
            with st.expander(f"{item['icon']} {item['mode']} — {item['time']}"):
                st.text(item["result"][:300] + "..." if len(item["result"]) > 300 else item["result"])
        if st.button("🗑️ Clear History", use_container_width=True, type="secondary"):
            st.session_state.history = []
            st.rerun()
    else:
        st.caption("No analyses yet.")


# ── Main UI: Hero ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem;">
    <div style="display: inline-block; background: linear-gradient(135deg, rgba(0,229,122,0.15), rgba(139,92,246,0.15)); border: 1px solid rgba(0,229,122,0.4); color: var(--accent); font-family: 'Space Mono', monospace; font-size: 0.65rem; letter-spacing: 0.2em; padding: 0.4rem 1.2rem; border-radius: 2rem; margin-bottom: 1rem; text-transform: uppercase; box-shadow: 0 4px 15px rgba(0,229,122,0.15);">
        ⚗️ AI-Powered Chemistry
    </div>
    <h1 style="font-size: clamp(2.8rem, 8vw, 4.5rem); font-weight: 800; line-height: 1; margin: 0.3rem 0; background: linear-gradient(135deg, #ffffff 0%, var(--accent) 50%, var(--accent2) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0px 4px 10px rgba(0,0,0,0.5));">ChemLens</h1>
    <p style="color: var(--muted); font-size: 0.95rem; font-family: 'Space Mono', monospace; margin-top: 0.5rem;">Point. Snap. Understand.</p>
</div>
""", unsafe_allow_html=True)


# ── 1. 3D Mode Selector ────────────────────────────────────────────────────────
st.markdown("<h4 style='text-align:center; font-weight: 700; color: #fff;'>Select Analysis Mode</h4>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.markdown(f"<div style='text-align:center; height:80px;'><img class='icon-3d' src='{URL_FLASK}' width='75'></div>", unsafe_allow_html=True)
    if st.button("Reaction", type="primary" if st.session_state.mode == "reaction" else "secondary", use_container_width=True):
        st.session_state.mode = "reaction"
        st.rerun()

with col_m2:
    st.markdown(f"<div style='text-align:center; height:80px;'><img class='icon-3d' src='{URL_RETRO}' width='75'></div>", unsafe_allow_html=True)
    if st.button("Retro", type="primary" if st.session_state.mode == "retro" else "secondary", use_container_width=True):
        st.session_state.mode = "retro"
        st.rerun()

with col_m3:
    st.markdown(f"<div style='text-align:center; height:80px;'><img class='icon-3d' src='{URL_COMP}' width='75'></div>", unsafe_allow_html=True)
    if st.button("Compound", type="primary" if st.session_state.mode == "compound" else "secondary", use_container_width=True):
        st.session_state.mode = "compound"
        st.rerun()

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)


# ── Yield calculator (reaction mode only) ─────────────────────────────────────
mass1, mass2 = None, None
if st.session_state.mode == "reaction":
    with st.expander("⚖️ Optional: Yield Calculator (Enter reactant masses)"):
        col1, col2 = st.columns(2)
        with col1:
            mass1 = st.number_input("Reactant 1 mass (g)", min_value=0.0, step=0.1, format="%.2f")
        with col2:
            mass2 = st.number_input("Reactant 2 mass (g)", min_value=0.0, step=0.1, format="%.2f")


# ── 2. 3D Input Method Selector & Logic ────────────────────────────────────────
if st.session_state.mode == "reaction":
    label, hint = "📸 Reactants Input", "Photo of written/drawn reactants"
elif st.session_state.mode == "retro":
    label, hint = "🔬 Target Molecule Input", "Photo of the molecule to synthesize"
else:
    label, hint = "🧪 Compound Input", "Photo of any chemical structure"

st.markdown(f"<div style='text-align:center;'><b>{label}</b><br><span style='color:var(--muted); font-size:0.85rem;'>{hint}</span></div><br>", unsafe_allow_html=True)

col_i1, col_i2 = st.columns(2)
with col_i1:
    st.markdown(f"<div style='text-align:center; height:60px;'><img class='icon-3d' src='{URL_CAM}' width='55'></div>", unsafe_allow_html=True)
    if st.button("Pro Camera", type="primary" if st.session_state.input_method == "cam" else "secondary", use_container_width=True):
        st.session_state.input_method = "cam"
        st.rerun()

with col_i2:
    st.markdown(f"<div style='text-align:center; height:60px;'><img class='icon-3d' src='{URL_GAL}' width='55'></div>", unsafe_allow_html=True)
    if st.button("Smart Gallery", type="primary" if st.session_state.input_method == "gal" else "secondary", use_container_width=True):
        st.session_state.input_method = "gal"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Input Execution
if st.session_state.input_method == "cam":
    if not st.session_state.camera_active:
        st.markdown("""
        <div style="text-align:center; padding:2rem; background: rgba(30, 30, 45, 0.4); border: 2px dashed rgba(255,255,255,0.1); border-radius:16px; margin-bottom: 1rem;">
            <span style="color:#8b8b9e; font-family:'Space Mono';">Camera is sleeping to save battery.</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🟢 POWER ON LENS", type="primary", use_container_width=True):
            st.session_state.camera_active = True
            st.rerun()
    else:
        cam = st.camera_input("Capture", label_visibility="collapsed")
        if cam:
            st.session_state.current_image = Image.open(io.BytesIO(cam.getvalue()))
            st.session_state.camera_active = False # Auto-destruct
            st.rerun()
        if st.button("❌ CLOSE LENS", type="secondary", use_container_width=True):
            st.session_state.camera_active = False
            st.rerun()

elif st.session_state.input_method == "gal":
    upl = st.file_uploader("Upload", type=["jpg", "jpeg", "png", "webp", "bmp"], label_visibility="collapsed")
    if upl:
        st.session_state.current_image = Image.open(io.BytesIO(upl.getvalue()))


# ── Build Prompts ──────────────────────────────────────────────────────────────
LEVEL_INSTRUCTIONS = {
    "Beginner":     "Use simple language. Avoid jargon. Explain every term. Target a high school student.",
    "Intermediate": "Use standard chemistry terminology. Assume first/second year university level.",
    "Expert":       "Use advanced IUPAC nomenclature, detailed mechanisms, stereochemical considerations. Target a PhD chemist.",
}
level_note = LEVEL_INSTRUCTIONS[explain_level]

REACTION_PROMPT = f"""
Analyze the image. It shows chemical reactants. Explanation level: {explain_level}. {level_note}
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
Analyze the molecular structure in the image. Perform a retrosynthetic analysis. Explanation level: {explain_level}. {level_note}
Respond in this EXACT format:
🎯 TARGET MOLECULE
[Name and identify the compound]
🔄 RETROSYNTHETIC DISCONNECTIONS
Disconnection 1:
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
Identify and analyze the chemical compound or structure shown in the image. Explanation level: {explain_level}. {level_note}
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
"""

PROMPTS = {"reaction": REACTION_PROMPT, "retro": RETRO_PROMPT, "compound": COMPOUND_PROMPT}
ICONS   = {"reaction": "⚗️", "retro": "🔄", "compound": "🔬"}
TAGS    = {"reaction": "REACTION ANALYSIS", "retro": "RETROSYNTHETIC ANALYSIS", "compound": "COMPOUND IDENTIFICATION"}
TAG_CLASSES = {"reaction": "", "retro": "retro", "compound": "compound"}


# ── 3. Preview & Pro Analysis Trigger ─────────────────────────────────────────
if st.session_state.current_image:
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    
    col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
    with col_img2:
        st.image(st.session_state.current_image, caption="Current Target Locked", use_container_width=True)
        if st.button("🔄 Retake / Clear Image", type="secondary", use_container_width=True):
            st.session_state.current_image = None
            st.session_state.analysis_result = None
            if st.session_state.input_method == "cam": st.session_state.camera_active = True
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Giant Pro Trigger Design
    st.markdown(f"""
    <div style="display:flex; justify-content:center; align-items:center; gap: 10px; margin-bottom: 15px;">
        <img class="icon-3d" src="{URL_PRO}" width="35">
        <span style="font-weight: 900; font-size: 1.3rem; color: #00e57a; letter-spacing: 2px;">PRO ENGINE READY</span>
    </div>
    """, unsafe_allow_html=True)

    btn_labels = {
        "reaction": "⚡ INITIATE REACTION PREDICTION",
        "retro":    "⚡ INITIATE RETROSYNTHESIS",
        "compound": "⚡ INITIATE IDENTIFICATION",
    }

    button_clicked = st.button(btn_labels[st.session_state.mode], type="primary", use_container_width=True)

    # 1. GENERATION + STREAMING
    if button_clicked:
        try:
            with st.spinner("Analyzing with Gemini Vision Pro..."):
                response = model.generate_content(
                    [PROMPTS[st.session_state.mode], st.session_state.current_image],
                    stream=True
                )

            tag_class = TAG_CLASSES[st.session_state.mode]
            tag_text  = TAGS[st.session_state.mode]

            st.markdown(f"""
            <div class="result-card" style="padding-bottom: 0;">
                <div class="result-tag {tag_class}">{tag_text}</div>
            </div>
            """, unsafe_allow_html=True)

            def stream_response(r):
                for chunk in r:
                    if chunk.text: yield chunk.text

            full_text = st.write_stream(stream_response(response))

            # Save to state
            st.session_state.analysis_result = full_text
            st.session_state.analysis_mode   = st.session_state.mode

            from datetime import datetime
            st.session_state.history.append({
                "mode":   TAGS[st.session_state.mode],
                "icon":   ICONS[st.session_state.mode],
                "result": full_text,
                "time":   datetime.now().strftime("%H:%M"),
            })

        except Exception as e:
            err = str(e)
            if "quota" in err.lower() or "429" in err:
                st.error("⚠️ API quota exceeded. Wait a minute.")
            else:
                st.error(f"Analysis failed: {err}\n\nTry a clearer image.")

    # 2. STATIC RENDERING (on rerun)
    elif st.session_state.analysis_result and st.session_state.analysis_mode == st.session_state.mode:
        tag_class = TAG_CLASSES[st.session_state.mode]
        tag_text  = TAGS[st.session_state.mode]

        st.markdown(f"""
        <div class="result-card" style="padding-bottom: 0; border-bottom-left-radius: 0;
             border-bottom-right-radius: 0; border-bottom: none;">
            <div class="result-tag {tag_class}">{tag_text}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(st.session_state.analysis_result)

    # 3. DOWNLOAD + CLEAR BUTTONS
    if st.session_state.analysis_result and st.session_state.analysis_mode == st.session_state.mode:
        st.markdown("<br>", unsafe_allow_html=True)
        col_dl, col_clear = st.columns([3, 1])
        with col_dl:
            st.download_button(
                label="📥 Download Output",
                data=st.session_state.analysis_result,
                file_name=f"chemlens_{st.session_state.mode}_analysis.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with col_clear:
            if st.button("🗑️ Clear", use_container_width=True, type="secondary"):
                st.session_state.analysis_result = None
                st.session_state.analysis_mode   = None
                st.rerun()


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:3rem 0 1rem; color:#4a4a5a;
            font-family:'Space Mono',monospace; font-size:0.65rem; letter-spacing:0.15em;">
    CHEMLENS PRO · POWERED BY GEMINI 1.5 FLASH
</div>
""", unsafe_allow_html=True)
