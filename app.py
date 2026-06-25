import time
import html
import streamlit as st
import google.generativeai as genai
from secret import API_KEY

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="Gemini Architect",
    page_icon="🧠",
    layout="wide"
)

# 2. Gemini Configuration with Robust Model Fallback
genai.configure(api_key=API_KEY)
try:
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    # Safe engineering fallback if premium endpoints are throttled
    model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize Session State variables to prevent UI disappearing acts
if "generated_text" not in st.session_state:
    st.session_state.generated_text = None
if "has_animated" not in st.session_state:
    st.session_state.has_animated = False

# 3. Inject Advanced Visual CSS with FORCE-MOTION Background
st.markdown("""
<style>
/* Target the base container classes aggressively to override default layouts */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMainViewContainer"] {
    background: linear-gradient(-45deg, #0b0d19, #1a163a, #071c35, #0a0f1d) !important;
    background-size: 400% 400% !important;
    animation: gradientMotion 12s ease infinite !important;
    font-family: 'Inter', sans-serif;
}

/* Motion Keyframes for Background Gradient Loop */
@keyframes gradientMotion {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Glassmorphic Hero Banner */
.hero {
    text-align: center;
    padding: 3.5rem 2rem;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    margin-bottom: 2.5rem;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    animation: fadeIn 1s ease-in-out;
}

.hero h1 {
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.hero p {
    font-size: 1.2rem;
    color: #94a3b8;
    margin-top: 0.75rem;
    font-weight: 400;
}

/* Custom Styled Input Containers */
.element-container textarea {
    background-color: rgba(20, 24, 43, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
}

/* High-Gloss Glow Button Styling */
.stButton > button {
    width: 100%;
    border: none !important;
    border-radius: 14px !important;
    height: 54px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    background: linear-gradient(90deg, #6366f1, #a855f7) !important;
    color: white !important;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4) !important;
    transition: all 0.3s ease-in-out !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(168, 85, 247, 0.6) !important;
    background: linear-gradient(90deg, #5051f1, #9333ea) !important;
}

/* Premium Output Glass Containers */
.output-box {
    background: rgba(10, 15, 30, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 2rem;
    border-radius: 18px;
    color: #e2e8f0;
    line-height: 1.7;
    font-size: 1.1rem;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    white-space: pre-wrap; /* Keeps structural linebreaks rendering cleanly */
}

/* Interactive Dashboard Cards */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    text-align: center;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# 4. App Structural Layout
st.markdown("""
<div class="hero">
<h1>🧠 Gemini Creative Studio</h1>
<p>Deploy cutting-edge AI engine modeling to generate modern web copy and articles instantly.</p>
</div>
""", unsafe_allow_html=True)

# 5. Core Engine Content Function with Advanced Engineering Prompts
def generate_content(prompt, content_type, tone, length):
    prompts = {
        "Blog": (
            f"Write a complete, comprehensive, and highly detailed {length.lower()} blog post in a {tone.lower()} tone "
            f"about the topic: {prompt}.\n\n"
            f"Structure your entire output strictly as follows:\n"
            f"Title\n\nIntroduction\n\nSection 1 (with heading)\n\nSection 2 (with heading)\n\n"
            f"Section 3 (with heading)\n\nConclusion\n\n"
            f"Do not use raw markdown markup elements like hashes (#) or asterisks (*). Make the article rich and completely structured."
        ),
        "Instagram Caption": f"Write an engaging {tone.lower()} Instagram caption containing native expressive emojis and hashtags for the topic: {prompt}",
        "Product Description": f"Write a {length.lower()} high-converting product description in a {tone.lower()} tone highlighting advanced features, values, and key consumer benefits for: {prompt}",
        "Email": f"Write a complete {length.lower()} professional email sequence in a {tone.lower()} tone with a clear subject line, structured email body, and call-to-action block for: {prompt}"
    }
    try:
        response = model.generate_content(
            prompts[content_type],
            generation_config={"temperature": 0.7, "max_output_tokens": 1500}
        )
        return response.text if hasattr(response, "text") and response.text else "No content generated."
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "Quota exceeded" in error_msg:
            return "❌ API Daily Limit Reached (20 requests max for Free Tier). Please switch to pay-as-you-go in Google AI Studio or try again tomorrow!"
        return f"❌ Error: {error_msg}"

# 6. Two-Column Dashboard Setup
layout_left, layout_right = st.columns([1.1, 1.4], gap="large")

with layout_left:
    st.markdown("### 🎛️ Engine Workspace")
    
    prompt = st.text_area(
        "Context Input & Core Topic",
        placeholder="Describe what you want to create (e.g., The future of quantum computing in web design)...",
        height=150
    )
    
    c1, c2 = st.columns(2)
    with c1:
        content_type = st.selectbox("Format Style", ["Blog", "Instagram Caption", "Product Description", "Email"])
        length = st.selectbox("Length Scale", ["Short", "Medium", "Long"])
    with c2:
        tone = st.selectbox("Voice Tone", ["Professional", "Friendly", "Creative", "Formal"])
        
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 Execute Architecture", use_container_width=True)

# 7. Output Display Logic Block
with layout_right:
    st.markdown("### 🖥️ Display Terminal")
    
    if generate_btn:
        if prompt.strip():
            with st.spinner("Compiling structural content parameters..."):
                st.session_state.generated_text = generate_content(prompt, content_type, tone, length)
                st.session_state.has_animated = False
        else:
            st.warning("⚠️ Terminal requires an active topic footprint input.")

    if st.session_state.generated_text:
        result = st.session_state.generated_text
        
        if result.startswith("❌"):
            st.error(result)
        else:
            text_placeholder = st.empty()
            
            # 1 & 2. Escape HTML string parameters and handle terminal carets cleanly
            if not st.session_state.has_animated:
                display_text = ""
                words = result.split(" ")
                for index, word in enumerate(words):
                    display_text += word + " "
                    safe_display = html.escape(display_text)
                    # Add character caret symbol ONLY while running layout steps
                    text_placeholder.markdown(f'<div class="output-box">{safe_display}▌</div>', unsafe_allow_html=True)
                    time.sleep(0.012)
                st.session_state.has_animated = True
            
            # Render final lock block cleanly without any trailing carets
            safe_final_result = html.escape(result)
            text_placeholder.markdown(f'<div class="output-box">{safe_final_result}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Live Engine Analytics Row
            m1, m2, m3 = st.columns(3)
            m1.metric("Words Created", len(result.split()))
            m2.metric("Characters", len(result))
            m3.metric("Asset Classification", content_type)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Simplified Actions: Single high-performance export button
            st.download_button(
                label="📥 Export Text Asset",
                data=result,
                file_name=f"asset_{content_type.lower().replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

st.markdown("""
---
<p style='text-align: center; color: #64748b; font-size: 0.9rem;'>Powered by Streamlit Framework & Google Gemini Engine Workspace</p>
""", unsafe_allow_html=True)