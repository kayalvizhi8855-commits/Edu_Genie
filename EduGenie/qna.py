from gemini_client import generate_text


def answer_question(question: str) -> str:

    prompt = f"""
You are answering a student's academic question.

Student question:
{question}

Instructions:

1. Answer the question directly.
2. Use simple and clear language.
3. Explain important terms.
4. Use examples when helpful.
5. Do not unnecessarily make the answer long.
6. If the question is ambiguous, clearly mention the assumption.
"""

    return generate_text(
        prompt,

        system_instruction=(
            "You are EduGenie's academic Q&A tutor. "
            "Be accurate, clear, friendly and educational."
        ),

        temperature=0.25,

        max_output_tokens=1000,
    )