from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import (
    QARequest,
    ExplainRequest,
    QuizRequest,
    SummaryRequest,
    LearningPathRequest,
    QuizResponse,
    HealthResponse,
)

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# Static files
app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static"
)


# Templates
templates = Jinja2Templates(
    directory=str(
        BASE_DIR / "templates"
    )
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

@app.get(
    "/health",
    response_model=HealthResponse
)
async def health():

    return HealthResponse(
        status="ok",
        service="EduGenie API"
    )


@app.post("/qa")
async def qa(
    request: QARequest
):

    answer = answer_question(
        request.question
    )

    return {
        "answer": answer
    }


@app.post("/explain")
async def explain(
    request: ExplainRequest
):

    explanation = explain_topic(
        request.topic,
        request.level
    )

    return {
        "explanation": explanation
    }


@app.post(
    "/quiz",
    response_model=QuizResponse
)
async def quiz(
    request: QuizRequest
):

    return generate_quiz(
        request.text,
        request.level
    )


@app.post("/summarize")
async def summarize(
    request: SummaryRequest
):

    summary = summarize_text(
        request.text
    )

    return {
        "summary": summary
    }


@app.post(
    "/learn/recommendations"
)
async def learning_recommendations(
    request: LearningPathRequest
):

    learning_path = get_learning_recommendations(
        request.topic,
        request.level,
        request.goal
    )

    return {
        "learning_path": learning_path
    }