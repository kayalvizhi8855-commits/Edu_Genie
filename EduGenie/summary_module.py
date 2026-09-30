from gemini_client import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following educational passage.

PASSAGE:

{text}

Requirements:

- Keep the important information.
- Remove unnecessary repetition.
- Use simple language.
- Keep important facts and relationships.
- Make it useful for quick revision.
- Give a short summary followed by key points.
"""

    return generate_text(

        prompt,

        system_instruction=(
            "You are an accurate academic summarizer."
        ),

        temperature=0.25,

        max_output_tokens=1200,
    )