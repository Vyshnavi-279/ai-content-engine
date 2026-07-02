import requests
from urllib.parse import quote

# Pollinations.ai — completely free, no API key, no signup required
POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}"


def generate_image(product_name: str, tagline: str, tone: str) -> str | None:
    """
    Generate a product hero image using Pollinations.ai (free, no API key).

    Returns the direct HTTPS image URL — Streamlit's st.image() and
    RunwayML's prompt_image both accept this directly.
    """
    print(f"\n🎨 Generating hero image for: '{product_name}' (tone: {tone})")

    tone_styles = {
        "playful": "vibrant colorful fun energetic lifestyle product photography, pastel colors, bright studio",
        "premium": "ultra premium luxury product shot, dark background, cinematic studio lighting, dramatic shadows",
        "eco":     "clean natural earthy tones, sustainable product photography, soft daylight, minimal white background",
    }
    style = tone_styles.get(tone.lower(), tone_styles["premium"])

    prompt = (
        f"Professional product hero image of {product_name}, "
        f"{style}, "
        f"concept: {tagline}, "
        "sharp focus, high resolution, no text, no watermarks, "
        "marketing campaign photo, 16:9"
    )

    url = POLLINATIONS_URL.format(prompt=quote(prompt))
    # Append quality params
    url += "?width=1280&height=720&model=flux&nologo=true&enhance=true"

    try:
        print(f"⏳ Requesting image from Pollinations.ai...")
        resp = requests.get(url, timeout=60, allow_redirects=True)
        resp.raise_for_status()

        content_type = resp.headers.get("content-type", "")
        if "image" not in content_type:
            print(f"⚠️  Unexpected content-type: {content_type}")
            return None

        print(f"✅ Image generated successfully ({len(resp.content):,} bytes)")
        # Return the URL directly — it's a stable public HTTPS URL
        # Streamlit st.image() and RunwayML both accept it
        return url

    except requests.exceptions.Timeout:
        print("❌ Image generation timed out after 60 seconds.")
        return None
    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        return None
