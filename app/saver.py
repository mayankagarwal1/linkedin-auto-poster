from pathlib import Path
from datetime import datetime

def save_post(topic: str, content: str) -> str:
    """Saves the final generated post to a local text file."""
    folder = Path("generated_posts")
    folder.mkdir(exist_ok=True)

    # Clean the topic string for a safe filename
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_')).replace(" ", "_").lower()
    
    # Truncate if the AI generated a very long topic title
    if len(safe_topic) > 50:
        safe_topic = safe_topic[:50]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_topic}_{timestamp}.txt"
    file_path = folder / filename

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return str(file_path)