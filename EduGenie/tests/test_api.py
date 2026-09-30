from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "EduGenie API"


def test_qa(monkeypatch):
    def fake_answer_question(question):
        return "This is a test answer."

    monkeypatch.setattr(
        main,
        "answer_question",
        fake_answer_question
    )

    response = client.post(
        "/qa",
        json={
            "question": "What is Artificial Intelligence?"
        }
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "This is a test answer."


def test_explain(monkeypatch):
    def fake_explain_topic(topic, level):
        return "This is a simple explanation."

    monkeypatch.setattr(
        main,
        "explain_topic",
        fake_explain_topic
    )

    response = client.post(
        "/explain",
        json={
            "topic": "Machine Learning",
            "level": "beginner"
        }
    )

    assert response.status_code == 200
    assert response.json()["explanation"] == (
        "This is a simple explanation."
    )


def test_quiz(monkeypatch):
    def fake_generate_quiz(text, level):
        return {
            "questions": [
                {
                    "question": "What is Python?",
                    "options": [
                        "Programming language",
                        "Database",
                        "Operating system",
                        "Browser"
                    ],
                    "correct_answer": "Programming language",
                    "explanation": (
                        "Python is a programming language."
                    )
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
                    "explanation": (
                        "HTML is a markup language."
                    )
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
                    "explanation": (
                        "CSS is used for styling web pages."
                    )
                }
            ]
        }

    monkeypatch.setattr(
        main,
        "generate_quiz",
        fake_generate_quiz
    )

    response = client.post(
        "/quiz",
        json={
            "text": "Python is a programming language.",
            "level": "beginner"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "questions" in data
    assert len(data["questions"]) == 3
    assert len(data["questions"][0]["options"]) == 4


def test_summarize(monkeypatch):
    def fake_summarize_text(text):
        return "This is a test summary."

    monkeypatch.setattr(
        main,
        "summarize_text",
        fake_summarize_text
    )

    response = client.post(
        "/summarize",
        json={
            "text": (
                "Artificial intelligence is a field "
                "of computer science."
            )
        }
    )

    assert response.status_code == 200
    assert response.json()["summary"] == (
        "This is a test summary."
    )


def test_learning_recommendations(monkeypatch):
    def fake_get_learning_recommendations(
        topic,
        level,
        goal
    ):
        return "Learn basics, practice, then build projects."

    monkeypatch.setattr(
        main,
        "get_learning_recommendations",
        fake_get_learning_recommendations
    )

    response = client.post(
        "/learn/recommendations",
        json={
            "topic": "Python",
            "level": "beginner",
            "goal": "Learn Python programming"
        }
    )

    assert response.status_code == 200

    assert response.json()["learning_path"] == (
        "Learn basics, practice, then build projects."
    )