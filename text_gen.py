import json
import requests
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL

def _chat(messages):
    # Dynamically build headers on every request to ensure fresh config API keys are used
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": OPENROUTER_MODEL, 
        "messages": messages
    }
    
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
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


def generate_tagline(product: str, audience: str, tone: str) -> list[str]:
    examples = FEW_SHOT_EXAMPLES.get(tone.lower(), FEW_SHOT_EXAMPLES["playful"])
    few_shot = "\n".join(
        f"Product: {e['product']}, Audience: {e['audience']} → Tagline: {e['tagline']}"
        for e in examples
    )
    messages = [
        {"role": "system", "content": "You are an expert copywriter. Generate taglines under 10 words each."},
        {"role": "user", "content": (
            f"Here are examples for {tone} tone:\n{few_shot}\n\n"
            f"Now generate exactly TWO distinct tagline variants for:\nProduct: {product}\nAudience: {audience}\nTone: {tone}\n"
            "Reply with only the two taglines, one per line, no numbering or extra text."
        )},
    ]
    raw = _chat(messages)
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    return lines[:2] if len(lines) >= 2 else (lines + lines)[:2]


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
    raw = _chat(messages).strip()
    
    # Robust cleanup of markdown wrappers (like ```json ... ```)
    if raw.startswith("```"):
        raw = raw.strip("`").strip()
        if raw.startswith("json"):
            raw = raw[4:].strip()
            
    try:
        return json.loads(raw)
    except Exception as parse_err:
        print(f"Failed to parse model JSON directly: {parse_err}. Raw data was: {raw}")
        # Return fallback dictionary structure so UI elements don't crash
        return {
            "twitter": f"Discover {product}, built perfectly for your target lifestyle!",
            "instagram": f"Introducing {product}! Built specifically for our community. #launch #innovation",
            "linkedin": f"We are proud to introduce our latest advancement: {product}, optimized for high performance workflows."
        }