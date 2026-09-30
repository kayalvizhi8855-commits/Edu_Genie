from gemini_client import generate_text


def explain_topic(
    topic: str,
    level: str = "beginner"
) -> str:

    prompt = f"""
Explain the following educational topic to a {level} learner.

Topic:
{topic}

Use this structure:

1. Simple definition
2. Easy explanation
3. Real-world analogy
4. Simple example
5. Key points to remember

Rules:

- Use simple student-friendly language.
- Avoid unnecessary jargon.
- Do not assume advanced knowledge.
- Keep the explanation organized.
"""

    return generate_text(

        prompt,

        system_instruction=(
            "You are a patient teacher who specializes "
            "in simplifying difficult concepts."
        ),

        temperature=0.3,

        max_output_tokens=1000,
    )