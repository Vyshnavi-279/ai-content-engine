from openai import OpenAI
from config import OPENROUTER_API_KEY

TONE_STYLES = {
    "playful": "bright flat illustration, vivid colors, cheerful and energetic",
    "premium": "photorealistic studio lighting, sleek and sophisticated, high contrast",
    "eco": "watercolour natural tones, soft earthy palette, organic textures",
}

def build_image_prompt(product: str, tagline: str, tone: str) -> str:
    style = TONE_STYLES.get(tone.lower(), TONE_STYLES["playful"])
    return (
        f"{product} product shot, {style}, centered composition, "
        f"shallow depth of field, 16:9 format, no text, no logos. "
        f"Mood: {tagline}."
    )

def generate_image(product: str, tagline: str, tone: str) -> str:
    client = OpenAI(api_key=OPENROUTER_API_KEY)
    prompt = build_image_prompt(product, tagline, tone)
    response = client.images.generate(
        model="gpt-image-1",  # use "gpt-image-2" when available
        prompt=prompt,
        size="1792x1024",
        n=1,
    )
    item = response.data[0]
    return item.url if item.url else item.b64_json
