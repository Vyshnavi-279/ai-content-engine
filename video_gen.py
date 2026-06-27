import time
import runwayml
from config import RUNWAY_API_KEY

MOTION_PROMPT = "Slow cinematic push-in. Soft light shifts gently. Background mostly still. 5 seconds."

def generate_video(image_url: str, product: str) -> str:
    try:
        client = runwayml.RunwayML(api_key=RUNWAY_API_KEY)
        task = client.image_to_video.create(
            model="gen4_turbo",
            prompt_image=image_url,
            prompt_text=MOTION_PROMPT,
        )
        # Poll until complete
        while task.status not in ("SUCCEEDED", "FAILED"):
            time.sleep(5)
            task = client.tasks.retrieve(task.id)
        if task.status == "FAILED":
            raise RuntimeError(f"Runway task failed: {task.failure or 'unknown error'}")
        return task.output[0]
    except runwayml.APIError as e:
        raise RuntimeError(f"Runway API error: {e.status_code} – {e.message}") from e
