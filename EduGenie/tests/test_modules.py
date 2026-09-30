import json

import qna
import explanation_module
import summary_module
import learning_path
import quiz_module


def test_answer_question(monkeypatch):
    def fake_generate_text(*args, **kwargs):
        return "This is a test answer."

    monkeypatch.setattr(
        qna,
        "generate_text",
        fake_generate_text
    )

    result = qna.answer_question("What is AI?")

    assert result == "This is a test answer."


def test_explain_topic(monkeypatch):
    def fake_generate_text(*args, **kwargs):
        return "AI is the ability of machines to perform tasks that normally require human intelligence."

    monkeypatch.setattr(
        explanation_module,
        "generate_text",
        fake_generate_text
    )

    result = explanation_module.explain_topic(
        "Artificial Intelligence",
        "beginner"
    )

    assert "AI" in result


def test_summarize_text(monkeypatch):
    def fake_generate_text(*args, **kwargs):
        return "This is a short summary."

    monkeypatch.setattr(
        summary_module,
        "generate_text",
        fake_generate_text
    )

    result = summary_module.summarize_text(
        "Artificial intelligence allows computers to perform tasks that normally require human intelligence."
    )

    assert result == "This is a short summary."


def test_learning_path(monkeypatch):
    def fake_generate_text(*args, **kwargs):
        return "1. Learn the basics\n2. Practice\n3. Build projects"

    monkeypatch.setattr(
        learning_path,
        "generate_text",
        fake_generate_text
    )

    result = learning_path.get_learning_recommendations(
        topic="Python",
        level="beginner",
        goal="learn Python programming"
    )

    assert "Learn the basics" in result


def test_clean_json_block():
    json_text = """```json
[
    {
        "question": "What is Python?",
        "options": [
            "Programming language",
            "Database",
            "Operating system",
            "Browser"
        ],
        "correct_answer": "Programming language",
        "explanation": "Python is a programming language."
    }
]
```"""

    cleaned = quiz_module.clean_json_block(json_text)

    data = json.loads(cleaned)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["correct_answer"] == "Programming language"


def test_validate_quiz():
    quiz_data = [
        {
            "question": "What is Python?",
            "options": [
                "Programming language",
                "Database",
                "Operating system",
                "Browser"
            ],
            "correct_answer": "Programming language",
            "explanation": "Python is a programming language."
        },
        {
            "question": "What is HTML?",
            "options": [
                "Markup language",
                "Database",
                "Operating system",
                "Compiler"
            ],
            "correct_answer": "Markup language",
            "explanation": "HTML is a markup language."
        },
        {
            "question": "What is CSS?",
            "options": [
                "Styling language",
                "Database",
                "Programming language",
                "Operating system"
            ],
            "correct_answer": "Styling language",
            "explanation": "CSS is used for styling web pages."
        }
    ]

    result = quiz_module.validate_quiz(quiz_data)

    assert result is None


def test_generate_quiz(monkeypatch):
    quiz_data = [
        {
            "question": "What is Python?",
            "options": [
                "Programming language",
                "Database",
                "Operating system",
                "Browser"
            ],
            "correct_answer": "Programming language",
            "explanation": "Python is a programming language."
        },
        {
            "question": "What is HTML?",
            "options": [
                "Markup language",
                "Database",
                "Operating system",
                "Compiler"
            ],
            "correct_answer": "Markup language",
            "explanation": "HTML is a markup language."
        },
        {
            "question": "What is CSS?",
            "options": [
                "Styling language",
                "Database",
                "Programming language",
                "Operating system"
            ],
            "correct_answer": "Styling language",
            "explanation": "CSS is used for styling web pages."
        }
    ]

    def fake_generate_text(*args, **kwargs):
        return json.dumps(quiz_data)

    monkeypatch.setattr(
        quiz_module,
        "generate_text",
        fake_generate_text
    )

    result = quiz_module.generate_quiz(
        "Python is a programming language. HTML is a markup language. CSS is used for styling."
    )

    assert "questions" in result
    assert len(result["questions"]) == 3
    assert len(result["questions"][0]["options"]) == 4