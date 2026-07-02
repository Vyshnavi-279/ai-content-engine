import importlib
import io
import base64
import zipfile
import requests as _requests
import streamlit as st
from text_gen import generate_tagline, generate_blog_intro, generate_social_posts
from image_gen import generate_image
from video_gen import generate_product_video

# ── 1. PILLOW-SHADED 3D DESIGN MATRIX (Directly from image_1a8b7e.png) ──────────
st.set_page_config(page_title="AI Content Engine", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&display=swap');
    
    /* Smooth clay-matted lavender backdrop */
    .stApp {
        background-color: #ECE9F7 !important;
        font-family: 'Fredoka', sans-serif !important;
    }
    
    /* Overhauling Streamlit Containers into Puffed-Up 3D Clay Cards */
    div[data-testid="stVerticalBlockBorder"] {
        background-color: #FBF9FF !important;
        border: none !important;
        border-radius: 28px !important;
        padding: 30px !important;
        /* Hyper-precise double layer shadow for true physical depth mapping */
        box-shadow: 
            12px 12px 24px rgba(132, 122, 179, 0.22),
            -10px -10px 20px rgba(255, 255, 255, 0.9),
            inset 4px 4px 8px rgba(255, 255, 255, 0.8),
            inset -4px -4px 8px rgba(147, 134, 201, 0.1) !important;
        margin-bottom: 24px !important;
    }
    
    /* The Left Purple Sidebar Panel styling from the reference photo */
    [data-testid="stSidebar"] {
        background-color: #8C83E2 !important;
        border-right: none !important;
        box-shadow: inset -10px 0px 20px rgba(0, 0, 0, 0.05) !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    /* Clean Typography Color Balancing */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #423E5D !important;
    }
    
    /* Soft 3D Bubble Input Cavities */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #F1EFF9 !important;
        border: none !important;
        border-radius: 18px !important;
        padding: 12px 16px !important;
        box-shadow: 
            inset 3px 3px 6px rgba(121, 110, 179, 0.15),
            inset -3px -3px 6px rgba(255, 255, 255, 0.8) !important;
        color: #423E5D !important;
        font-weight: 500;
    }
    
    /* High-Gloss Candy-Pink Action Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #FF91B6 0%, #FA5B8F 100%) !important;
        color: #FFFFFF !important;
        border-radius: 22px !important;
        border: none !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        box-shadow: 
            0px 8px 20px rgba(250, 91, 143, 0.35),
            inset 3px 3px 6px rgba(255, 255, 255, 0.4),
            inset -3px -3px 6px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0px 12px 24px rgba(250, 91, 143, 0.45) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }
    
    /* Header Step Stepper Elements */
    .clay-navigation {
        display: flex;
        gap: 16px;
        margin-bottom: 30px;
        justify-content: center;
    }
    .clay-step {
        padding: 10px 24px;
        background: #F1EFF9;
        border-radius: 40px;
        font-size: 14px;
        font-weight: 700;
        color: #837E9C;
        box-shadow: 4px 4px 10px rgba(132, 122, 179, 0.1), inset 2px 2px 4px #FFF;
    }
    .clay-step.active {
        background-color: #6C5DD3 !important;
        color: #FFFFFF !important;
        box-shadow: 0px 8px 16px rgba(108, 93, 211, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

def build_zip(tagline: str, blog_intro: str, social: dict, image_url: str) -> bytes:
    import os as _os
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        txt = f"TAGLINE\n{'='*40}\n{tagline}\n\nBLOG INTRO\n{'='*40}\n{blog_intro}\n\nSOCIALS\n{social}"
        zf.writestr("campaign_copy.txt", txt)
        if image_url:
            try:
                if image_url.startswith("http"):
                    # Hosted URL — download it
                    img_bytes = _requests.get(image_url, timeout=15).content
                    zf.writestr("hero_image.png", img_bytes)
                elif _os.path.isfile(image_url):
                    # Local file path from AI image generation
                    with open(image_url, "rb") as f:
                        zf.writestr("hero_image.png", f.read())
            except Exception:
                pass
    buf.seek(0)
    return buf.read()

# ── 2. WORKSPACE STATE ARCHITECTURE ──────────────────────────────────────────
if "app_step" not in st.session_state:
    st.session_state["app_step"] = 1

if "campaign_data" not in st.session_state:
    st.session_state["campaign_data"] = {}

def go_to_step(step_number):
    st.session_state["app_step"] = step_number
    st.rerun()

# Rounded Profile Panel Left Sidebar
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 44px; margin-bottom: 10px;'>🎵</div>
            <h2 style='font-size: 22px; margin: 0;'>Dashboard Suite</h2>
            <p style='font-size: 12px; opacity: 0.8; margin-top: 5px;'>AI Content Engine v2.0</p>
        </div>
        <hr style='border: 0; border-top: 2px solid rgba(255,255,255,0.15); margin: 15px 0;'>
    """, unsafe_allow_html=True)
    if st.button("🔄 Clear System State"):
        st.session_state.clear()
        st.rerun()

# Navigation Timeline Steps Bar
s = st.session_state["app_step"]
st.markdown(f"""
    <div class="clay-navigation">
        <div class="clay-step {'active' if s==1 else ''}">🎵 1. Brand Blueprint</div>
        <div class="clay-step {'active' if s==2 else ''}">🔮 2. Variant Selector</div>
        <div class="clay-step {'active' if s==3 else ''}">🛠️ 3. Asset Studio</div>
        <div class="clay-step {'active' if s==4 else ''}">🎁 4. Delivery Suite</div>
    </div>
""", unsafe_allow_html=True)


# ── STEP 1: BRAND BLUEPRINT INITIALIZATION ────────────────────────────────────
if st.session_state["app_step"] == 1:
    col1, col2 = st.columns([1.1, 0.9])
    
    with col1:
        with st.container(border=True):
            st.markdown('<h3>Good Morning, Creator! 👋</h3>', unsafe_allow_html=True)
            st.markdown('<p style="font-size: 14px; margin-bottom: 20px;">Let\'s enjoy making some content assets today.</p>', unsafe_allow_html=True)
            
            prod_name = st.text_input("📦 Product Line Identity", placeholder="e.g., Pastel Wireless Headphones")
            target_aud = st.text_input("👥 Target Audience Demographics", placeholder="e.g., Casual Music Listeners")
            tone = st.selectbox("🎨 Brand Vocal Tone", ["playful", "premium", "eco"])
            
            if st.button("Generate Strategy Blueprint ✨"):
                if prod_name and target_aud:
                    with st.spinner("Baking clay models..."):
                        st.session_state["campaign_data"] = {"product": prod_name, "audience": target_aud, "tone": tone}
                        st.session_state["campaign_data"]["taglines"] = generate_tagline(prod_name, target_aud, tone)
                        go_to_step(2)
                else:
                    st.warning("Please configure your campaign targets before generating.")
        
    with col2:
        with st.container(border=True):
            st.markdown('<h3>📊 Dynamic Matching Hub</h3>', unsafe_allow_html=True)
            st.info("🌱 Gen Z Blend | 💼 Millennials Core | 🎨 Creative Segments")
            st.markdown("""
                <div style="background-color: #F1EFF9; padding: 18px; border-radius: 20px; margin-top: 15px; box-shadow: inset 2px 2px 5px rgba(0,0,0,0.03);">
                    <span style="color:#FA5B8F; font-weight:700; font-size:15px;">★ 85% Matrix Reach Expected</span><br>
                    <p style="margin-top: 6px; font-size: 13px; opacity: 0.8; line-height: 1.5;">
                        Assets automatically link keywords to dynamic rendering suites for responsive layout integration.
                    </p>
                </div>
            """, unsafe_allow_html=True)


# ── STEP 2: STRATEGY VARIANT CHOICE ───────────────────────────────────────────
elif st.session_state["app_step"] == 2:
    with st.container(border=True):
        st.markdown('<h3>🔮 Select Your Core Concept Hook</h3>', unsafe_allow_html=True)
        tags = st.session_state["campaign_data"].get("taglines", ["Sound that wraps your soul.", "Pure design, pure performance."])
        
        chosen_tag = st.radio("Available Engine Blueprints:", tags, index=0)
        
        if st.button("Confirm Blueprint & Build Universe 🚀"):
            st.session_state["campaign_data"]["chosen_tagline"] = chosen_tag
            go_to_step(3)


# ── STEP 3: STUDIO ASSET WORKBENCH (GRID MATRIX) ──────────────────────────────
elif st.session_state["app_step"] == 3:
    cdata = st.session_state["campaign_data"]
    
    # If any key piece is missing, regenerate everything from scratch
    needs_regen = (
        "blog_intro" not in cdata or
        not cdata.get("social") or
        not cdata.get("image_url")
    )

    if needs_regen:
        # Clear stale partial data before regenerating
        for key in ("blog_intro", "social", "image_url", "video_url"):
            cdata.pop(key, None)
        with st.spinner("Generating your campaign assets..."):
            cdata["blog_intro"] = generate_blog_intro(cdata["product"], cdata["audience"], cdata["tone"], cdata["chosen_tagline"])
            cdata["social"]     = generate_social_posts(cdata["product"], cdata["audience"], cdata["tone"])
            cdata["image_url"]  = generate_image(cdata["product"], cdata["chosen_tagline"], cdata["tone"])
            cdata["video_url"]  = generate_product_video(cdata["image_url"], cdata["product"])
            st.session_state["campaign_data"] = cdata
            st.rerun()

    st.markdown('<h2 style="margin-bottom: 25px; font-weight:700;">🛠️ Creative Studio Asset Workbench</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown('<h4>🏷️ Core Tagline Driver</h4>', unsafe_allow_html=True)
            st.success(cdata.get("chosen_tagline"))
        
        with st.container(border=True):
            st.markdown('<h4>✍️ Editorial Copy Blog Frame</h4>', unsafe_allow_html=True)
            st.write(cdata.get("blog_intro"))
        
        with st.container(border=True):
            st.markdown('<h4>📱 Microblogging Social Array</h4>', unsafe_allow_html=True)
            soc = cdata.get("social", {})
            st.markdown(f"**🐦 Micro-Post Frame:**<br>{soc.get('twitter','')}", unsafe_allow_html=True)
            st.write(" ")
            st.markdown(f"**📸 Instagram Content Card:**<br>{soc.get('instagram','')}", unsafe_allow_html=True)
        
    with col2:
        with st.container(border=True):
            st.markdown('<h4>🎨 3D Creative Hero Visual</h4>', unsafe_allow_html=True)
            img = cdata.get("image_url", "")
            if img:
                st.image(img, use_column_width=True)
            else:
                st.info("Image generation skipped or failed.")
                if st.button("🔄 Retry Image"):
                    cdata.pop("image_url", None)
                    cdata.pop("video_url", None)
                    st.session_state["campaign_data"] = cdata
                    st.rerun()
        
        with st.container(border=True):
            st.markdown('<h4>🎬 Production Motion Stream</h4>', unsafe_allow_html=True)
            vid = cdata.get("video_url", "")
            if vid:
                st.video(vid)
            else:
                st.warning(
                    "🎬 Video generation skipped or failed.\n\n"
                    "**Common reasons:**\n"
                    "- 💳 Insufficient RunwayML credits → [Top up at app.runwayml.com](https://app.runwayml.com)\n"
                    "- 🔑 Missing or invalid `RUNWAY_API_KEY` in your `.env` file\n"
                    "- 🖼️ Hero image generation also failed (no source image to animate)\n\n"
                    "Check the terminal for the exact error."
                )
                
    if st.button("Pack Deliverables & Finalize Campaign ➡️"):
        go_to_step(4)


# ── STEP 4: PACKAGE DELIVERY SUITE ────────────────────────────────────────────
elif st.session_state["app_step"] == 4:
    cdata = st.session_state["campaign_data"]
    
    with st.container(border=True):
        st.markdown('<div style="text-align: center;"><h3>🎁 Complete Distribution Delivery Suite</h3></div>', unsafe_allow_html=True)
        st.balloons()
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Campaign Architecture Manifest")
            st.info(f"**Product Asset Target:** {cdata.get('product')}")
            st.info(f"**Selected Strategy Blueprint:** {cdata.get('chosen_tagline')}")
            st.write("**Blog Script Content:**", cdata.get("blog_intro"))
            
        with col2:
            if cdata.get("image_url"):
                st.image(cdata.get("image_url"), caption="Distribution Reference Blueprint Visual", use_column_width=True)
                
        st.divider()
        
        zip_data = build_zip(cdata.get("chosen_tagline",""), cdata.get("blog_intro",""), cdata.get("social",{}), cdata.get("image_url",""))
        
        st.download_button(
            label="⚡ DOWNLOAD COMPACT DISTRIBUTION SUITE (.ZIP) ⚡",
            data=zip_data,
            file_name=f"{cdata.get('product','asset')}_campaign_pack.zip",
            mime="application/zip"
        )