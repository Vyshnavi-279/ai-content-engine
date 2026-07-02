"""
image_prompts.py — Premium Prompt Library for AI Content Engine

This module contains the master prompt for Grok Imagine (and any top-tier
image generator) to produce the signature "AI Content Engine" hero visual.
It also provides tone-adapted variants and bonus modifiers so the same
underlying scene can be rendered in different moods.

Usage:
    from image_prompts import build_master_prompt

    prompt = build_master_prompt(tone="premium")
    # → returns the full prompt string ready to send to the image API
"""

# ──────────────────────────────────────────────────────────────────────────────
# MASTER PROMPT — "Ignite Ideas. Launch Instantly."
# ──────────────────────────────────────────────────────────────────────────────
# This is the canonical, production-grade prompt designed for Grok Imagine
# (or DALL-E 3, Midjourney, Stable Diffusion, etc.).  It paints a cinematic,
# ultra-modern isometric view of the AI Content Engine as a floating UI
# launchpad in a vibrant cosmic space.
# ──────────────────────────────────────────────────────────────────────────────

MASTER_PROMPT = (
    "Ultra-modern, premium 3D floating UI design for AI Content Engine — "
    "an intelligent marketing launchpad app, cinematic top-down isometric view "
    "like premium Behance food delivery mockups but elevated to world-class level. "
    "Sleek dark glassmorphic mobile phone screens floating elegantly in a vibrant "
    "cosmic space with subtle glowing particles, floating holographic 3D icons "
    "(sparkling lightbulbs, dynamic taglines, image canvases, video reels), "
    "soft neon accents in electric teal, vibrant magenta, and golden gradients. "
    "One main phone screen shows beautiful product name generator interface with "
    "real-time suggestions, another shows target audience insights dashboard, "
    "another displays generated eye-catching blog intro preview with images. "
    "Dynamic motion: gentle floating elements, subtle parallax, glowing connections "
    "between screens, premium depth of field, volumetric lighting, hyper-detailed, "
    "ultra-clean typography, luxurious minimalism mixed with playful energy, "
    "8K resolution, masterpiece, best UI/UX design in the world --ar 3:4 --stylize 750"
)

# ──────────────────────────────────────────────────────────────────────────────
# TONE-ADAPTED VARIANTS
# ──────────────────────────────────────────────────────────────────────────────

LIGHT_THEME_SUFFIX = (
    "bright elegant cream and soft gradient background, "
    "warm ivory and rose-gold accents replacing the dark cosmic backdrop, "
    "airy glassmorphism with soft white glow, pastel neon highlights"
)

DARK_THEME_SUFFIX = (
    "deep cosmic void background with rich midnight blue and violet gradients, "
    "intense neon glow, high-contrast glassmorphism, dramatic volumetric lighting"
)

MOTION_SUFFIX = (
    "subtle animated floating 3D elements and glowing energy lines, "
    "gentle particle drift, slow-rotating holographic icons, "
    "pulsing neon connections between screens, cinematic parallax depth"
)

# ──────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ──────────────────────────────────────────────────────────────────────────────

def build_master_prompt(
    tone: str = "premium",
    add_motion: bool = False,
    add_light_theme: bool = False,
) -> str:
    """
    Build the final image generation prompt by composing the master scene
    with optional tone modifiers.

    Parameters
    ----------
    tone : str
        One of "premium", "playful", or "eco".  Controls the colour palette
        and atmosphere of the generated image.
    add_motion : bool
        If True, appends the motion/animation suffix for generators that
        support animated output (e.g. Grok Imagine, Pika, Runway).
    add_light_theme : bool
        If True, replaces the dark cosmic background with a light, airy
        cream-and-rose-gold palette.

    Returns
    -------
    str
        The fully composed prompt string.
    """
    # Start with the core master scene
    prompt = MASTER_PROMPT

    # Apply light / dark theme modifier
    if add_light_theme:
        prompt = prompt.replace(
            "Sleek dark glassmorphic mobile phone screens floating elegantly in a vibrant cosmic space",
            f"Sleek glassmorphic mobile phone screens floating elegantly, {LIGHT_THEME_SUFFIX}"
        )

    # Append motion suffix if requested
    if add_motion:
        prompt += f", {MOTION_SUFFIX}"

    return prompt


def get_prompt_variations() -> dict[str, str]:
    """
    Return a dictionary of ready-to-use prompt variations for quick reference.

    Returns
    -------
    dict[str, str]
        Keys are descriptive labels; values are the full prompt strings.
    """
    return {
        "default (dark premium)": build_master_prompt(tone="premium"),
        "light theme":            build_master_prompt(tone="premium", add_light_theme=True),
        "with motion":            build_master_prompt(tone="premium", add_motion=True),
        "light + motion":         build_master_prompt(tone="premium", add_light_theme=True, add_motion=True),
    }


# ──────────────────────────────────────────────────────────────────────────────
# SELF-TEST
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 72)
    print("  AI Content Engine — Image Prompt Library")
    print("=" * 72)
    print()

    for label, prompt in get_prompt_variations().items():
        print(f"─── {label.upper()} ───")
        print(prompt)
        print()