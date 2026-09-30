from pydantic import BaseModel, Field, field_validator


class QARequest(BaseModel):

    question: str = Field(
        min_length=2,
        max_length=10000
    )

    @field_validator("question")
    @classmethod
    def clean_question(cls, value: str):

        value = value.strip()

        if not value:
            raise ValueError(
                "Question cannot be empty."
            )

        return value


class ExplainRequest(BaseModel):

    topic: str = Field(
        min_length=2,
        max_length=5000
    )

    level: str = Field(
        default="beginner",
        max_length=30
    )


class QuizRequest(BaseModel):

    text: str = Field(
        min_length=1,
        max_length=20000
    )

    level: str = Field(
        default="beginner",
        max_length=30
    )


class SummaryRequest(BaseModel):

    text: str = Field(
        min_length=1,
        max_length=20000
    )


class LearningPathRequest(BaseModel):

    topic: str = Field(
        min_length=2,
        max_length=5000
    )

    level: str = Field(
        default="beginner",
        max_length=30
    )

    goal: str = Field(
        default="understand the topic well",
        max_length=500
    )


class QuizQuestion(BaseModel):

    question: str

    options: list[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str


class QuizResponse(BaseModel):

    questions: list[QuizQuestion] = Field(
        min_length=3,
        max_length=3
    )


class HealthResponse(BaseModel):

    status: str

    service: str