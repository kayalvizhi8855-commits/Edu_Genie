from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    goal: str = "understand the topic well"
) -> str:

    prompt = f"""
Create a personalized learning path.

Topic:
{topic}

Current level:
{level}

Learning goal:
{goal}

Create a structured roadmap from beginner to advanced.

For every stage include:

1. Topics to learn
2. Concepts to understand
3. Practice activities
4. Approximate time required
5. Recommended types of resources

At the end provide:

- A weekly study routine
- Practice suggestions
- A checklist for moving to the next level

Use clear headings and bullet points.

Do not invent specific URLs.
"""

    return generate_text(

        prompt,

        system_instruction=(
            "You are an expert educational learning-path designer."
        ),

        temperature=0.45,

        max_output_tokens=1800,
    )