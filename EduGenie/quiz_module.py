import json

from gemini_client import generate_text


QUIZ_SCHEMA = {
    "type": "array",
    "minItems": 3,
    "maxItems": 3,

    "items": {
        "type": "object",

        "properties": {

            "question": {
                "type": "string"
            },

            "options": {
                "type": "array",
                "minItems": 4,
                "maxItems": 4,

                "items": {
                    "type": "string"
                }
            },

            "correct_answer": {
                "type": "string"
            },

            "explanation": {
                "type": "string"
            }
        },

        "required": [
            "question",
            "options",
            "correct_answer",
            "explanation"
        ]
    }
}


def clean_json_block(text: str) -> str:

    text = text.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines)

    return text.strip()


def validate_quiz(data):

    if not isinstance(data, list):
        raise ValueError(
            "Quiz must be a list."
        )

    if len(data) != 3:
        raise ValueError(
            "Quiz must contain exactly 3 questions."
        )

    for question in data:

        if not isinstance(question, dict):
            raise ValueError(
                "Invalid quiz question."
            )

        required_fields = [
            "question",
            "options",
            "correct_answer",
            "explanation"
        ]

        for field in required_fields:

            if field not in question:
                raise ValueError(
                    f"Missing field: {field}"
                )

        options = question["options"]

        if not isinstance(options, list):
            raise ValueError(
                "Options must be a list."
            )

        if len(options) != 4:
            raise ValueError(
                "Each question must have exactly 4 options."
            )

        if question["correct_answer"] not in options:
            raise ValueError(
                "Correct answer must be one of the options."
            )


def generate_quiz(
    text: str,
    level: str = "beginner"
) -> dict:

    prompt = f"""
Create a multiple-choice quiz from this educational passage.

Learner level:
{level}

PASSAGE:

{text}

Requirements:

- Exactly 3 questions.
- Each question must have exactly 4 options.
- Only one option can be correct.
- Wrong options should be plausible.
- Provide the correct answer.
- Provide a short explanation.
- Questions must be based on the passage.
- Return ONLY valid JSON.
"""

    response = generate_text(

        prompt,

        system_instruction=(
            "You are EduGenie, an educational assessment designer."
        ),

        temperature=0.35,

        max_output_tokens=1600,

        response_mime_type="application/json",

        response_schema=QUIZ_SCHEMA
    )

    try:

        cleaned = clean_json_block(response)

        data = json.loads(cleaned)

        validate_quiz(data)

        return {
            "questions": data
        }

    except Exception as error:

        raise RuntimeError(
            f"Unable to create a valid quiz: {error}"
        ) from error