import os
import tempfile
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

HF_TOKEN = os.getenv("HF_TOKEN")

# HF text-to-video model via the serverless inference API
# Using damo-vilab/text-to-video-ms-1.7b — free, no credits needed, just a valid HF token
HF_VIDEO_API = "https://api-inference.huggingface.co/models/damo-vilab/text-to-video-ms-1.7b"


def generate_product_video(image_url_or_path: str, product_name: str) -> str | None:
    """
    Generate a short product video using Hugging Face text-to-video (free tier).
    Returns a local .mp4 file path, or None if generation fails.
    """
    print(f"\n🎬 Starting video generation for: '{product_name}'...")

    if not HF_TOKEN:
        print("⚠️  HF_TOKEN missing in .env — skipping video generation.")
        return None

    prompt = (
        f"Cinematic commercial product showcase for {product_name}, "
        "smooth slow camera movement, professional studio lighting, "
        "high quality product video"
    )

    try:
        print("⏳ Calling HuggingFace text-to-video API...")
        resp = requests.post(
            HF_VIDEO_API,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": prompt},
            timeout=120,
        )

        # Handle common errors clearly
        if resp.status_code == 401:
            print("❌ HF token is invalid or expired. Update HF_TOKEN in .env")
            return None
        if resp.status_code == 403:
            print("❌ HF token lacks inference permissions.")
            print("   → Go to huggingface.co/settings/tokens, edit your token,")
            print("     set type to 'Read' or enable 'Make calls to Inference API'")
            return None
        if resp.status_code == 503:
            print("❌ Model is loading (cold start). Try again in 20 seconds.")
            return None
        if resp.status_code == 429:
            print("❌ HF rate limit hit. Try again in a minute.")
            return None

        resp.raise_for_status()

        content_type = resp.headers.get("content-type", "")
        if "video" not in content_type and "octet-stream" not in content_type:
            print(f"❌ Unexpected response type: {content_type}")
            print(f"   Response: {resp.text[:200]}")
            return None

        # Save video to a temp file
        tmp = tempfile.NamedTemporaryFile(
            suffix=".mp4", delete=False,
            prefix=f"video_{product_name[:20].replace(' ', '_')}_"
        )
        tmp.write(resp.content)
        tmp.flush()
        tmp.close()

        print(f"✅ Video generated! Saved to: {tmp.name} ({len(resp.content):,} bytes)")
        return tmp.name

    except requests.exceptions.Timeout:
        print("❌ Video generation timed out after 120s — model may be cold, try again.")
        return None
    except Exception as e:
        print(f"❌ Video generation error: {e}")
        return None