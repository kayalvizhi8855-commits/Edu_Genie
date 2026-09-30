from functools import lru_cache
import time

from google import genai
from google.genai import types
from google.genai.errors import ServerError

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    if not GEMINI_API_KEY:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(
    prompt: str,
    system_instruction: str = (
        "You are EduGenie, a helpful educational assistant."
    ),
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
    response_mime_type: str | None = None,
    response_schema=None,
) -> str:

    client = get_client()

    config_options = {
        "system_instruction": system_instruction,
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }

    if response_mime_type:
        config_options["response_mime_type"] = response_mime_type

    if response_schema:
        config_options["response_schema"] = response_schema

    last_error = None

    # Try the request 3 times if Gemini temporarily returns 503.
    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    **config_options
                ),
            )

            text = (response.text or "").strip()

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text

        except ServerError as error:
            last_error = error

            # 503 = temporary Gemini server overload.
            if "503" in str(error):

                if attempt < 2:
                    time.sleep(3 * (attempt + 1))
                    continue

                raise RuntimeError(
                    "Gemini is temporarily unavailable because "
                    "the selected model is experiencing high demand. "
                    "Please try again in a few minutes."
                ) from error

            raise

    raise RuntimeError(
        f"Gemini request failed: {last_error}"
    )