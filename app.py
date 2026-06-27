import importlib
import streamlit as st
from text_gen import generate_tagline, generate_blog_intro, generate_social_posts
from image_gen import generate_image
from video_gen import generate_video

st.set_page_config(page_title="AI Content Engine", layout="wide")
st.title("🚀 AI Content Engine")

# ── Requirements check ────────────────────────────────────────────────────────
REQUIRED_PACKAGES = ["streamlit", "openai", "dotenv", "requests", "PIL", "runwayml"]
missing = [pkg for pkg in REQUIRED_PACKAGES if importlib.util.find_spec(pkg) is None]
if missing:
    st.error(f"Missing packages: {', '.join(missing)}. Run `pip install -r requirements.txt`")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Campaign Inputs")
    product = st.text_input("Product Name")
    audience = st.text_input("Target Audience")
    tone = st.selectbox("Brand Tone", ["playful", "premium", "eco"])
    run = st.button("Generate Campaign", type="primary", disabled=not (product and audience))

if not run:
    st.stop()

# ── Generation ────────────────────────────────────────────────────────────────
results = {}
errors = {}

steps = [
    ("tagline",    "Generating tagline…",       lambda: generate_tagline(product, audience, tone)),
    ("blog_intro", "Writing blog introduction…", lambda: generate_blog_intro(product, audience, tone, results.get("tagline", ""))),
    ("social",     "Creating social posts…",     lambda: generate_social_posts(product, audience, tone)),
    ("image_url",  "Generating hero image…",     lambda: generate_image(product, results.get("tagline", ""), tone)),
    ("video_url",  "Rendering campaign video…",  lambda: generate_video(results.get("image_url", ""), product)),
]

for key, label, fn in steps:
    with st.spinner(label):
        try:
            results[key] = fn()
        except Exception as e:
            errors[key] = str(e)
            st.warning(f"⚠️ {label.rstrip('…')} failed: {e}")

# ── Display ───────────────────────────────────────────────────────────────────
left, right = st.columns(2)

with left:
    st.subheader("Tagline")
    if "tagline" in errors:
        st.warning(errors["tagline"])
    else:
        st.info(results.get("tagline", ""))
    st.caption("Technique: Few-shot prompting")

    st.subheader("Blog Introduction")
    if "blog_intro" in errors:
        st.warning(errors["blog_intro"])
    else:
        st.text_area("", results.get("blog_intro", ""), height=220, label_visibility="collapsed")
    st.caption("Technique: Role-based prompting (content strategist persona)")

    st.subheader("Social Posts")
    social = results.get("social") or {}
    for icon, platform, key in [("🐦", "Twitter", "twitter"), ("📸", "Instagram", "instagram"), ("💼", "LinkedIn", "linkedin")]:
        with st.expander(f"{icon} {platform}", expanded=True):
            if "social" in errors:
                st.warning(errors["social"])
            else:
                st.write(social.get(key, ""))
            st.caption("Technique: Structured JSON output prompting")

with right:
    st.subheader("Hero Image")
    if "image_url" in errors:
        st.warning(errors["image_url"])
    else:
        image_url = results.get("image_url", "")
        if image_url:
            if not image_url.startswith("http"):
                st.image(f"data:image/png;base64,{image_url}", use_container_width=True)
            else:
                st.image(image_url, use_container_width=True)
    st.caption("Technique: Tone-driven visual prompt engineering")

    st.subheader("Campaign Video")
    if "video_url" in errors:
        st.warning(errors["video_url"])
    else:
        video_url = results.get("video_url", "")
        if video_url:
            st.video(video_url)
    st.caption("Technique: Cinematic motion prompt (image-to-video)")
