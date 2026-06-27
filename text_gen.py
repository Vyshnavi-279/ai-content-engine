import json
import requests
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

def _chat(messages):
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=HEADERS,
        json={"model": OPENROUTER_MODEL, "messages": messages},
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


FEW_SHOT_EXAMPLES = {
    "playful": [
        {"product": "energy drink", "audience": "teens", "tagline": "Crack open the fun!"},
        {"product": "sneakers", "audience": "kids", "tagline": "Run wild, jump higher!"},
    ],
    "premium": [
        {"product": "luxury watch", "audience": "executives", "tagline": "Time, redefined for the elite."},
        {"product": "silk scarf", "audience": "fashionistas", "tagline": "Elegance you can wear."},
    ],
    "eco": [
        {"product": "reusable bottle", "audience": "activists", "tagline": "Sip sustainably, save the planet."},
        {"product": "bamboo toothbrush", "audience": "eco-conscious adults", "tagline": "Brush green, live clean."},
    ],
}


def generate_tagline(product: str, audience: str, tone: str) -> str:
    examples = FEW_SHOT_EXAMPLES.get(tone.lower(), FEW_SHOT_EXAMPLES["playful"])
    few_shot = "\n".join(
        f"Product: {e['product']}, Audience: {e['audience']} → Tagline: {e['tagline']}"
        for e in examples
    )
    messages = [
        {"role": "system", "content": "You are an expert copywriter. Generate ONE tagline under 10 words."},
        {"role": "user", "content": (
            f"Here are examples for {tone} tone:\n{few_shot}\n\n"
            f"Now generate ONE tagline for:\nProduct: {product}\nAudience: {audience}\nTone: {tone}\n"
            "Reply with only the tagline."
        )},
    ]
    return _chat(messages)


def generate_blog_intro(product: str, audience: str, tone: str, tagline: str) -> str:
    messages = [
        {"role": "system", "content": (
            "You are a senior content strategist with 10 years of experience writing high-converting brand content. "
            "Write engaging, audience-focused copy that drives action."
        )},
        {"role": "user", "content": (
            f"Write a blog introduction of exactly 200 words for:\n"
            f"Product: {product}\nAudience: {audience}\nTone: {tone}\nTagline: \"{tagline}\"\n"
            "The tagline must be woven naturally into the introduction. Output only the blog intro."
        )},
    ]
    return _chat(messages)


def generate_social_posts(product: str, audience: str, tone: str) -> dict:
    messages = [
        {"role": "system", "content": "You are a social media copywriter. Return only valid JSON."},
        {"role": "user", "content": (
            f"Create social media posts for:\nProduct: {product}\nAudience: {audience}\nTone: {tone}\n\n"
            "Return a JSON object with exactly these keys:\n"
            "- twitter: max 280 characters\n"
            "- instagram: max 2200 characters (include hashtags)\n"
            "- linkedin: max 700 characters (professional tone)\n"
            "Output only the JSON object."
        )},
    ]
    raw = _chat(messages)
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
