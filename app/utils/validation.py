from typing import Any
from app.models.questions import QuestionType  # update this path based on your project structure


def validate_answer_type(answer: Any, question_type: str) -> Any:
    try:
        qtype = QuestionType(question_type)
    except ValueError:
        raise ValueError(f"Unsupported question type: {question_type}")

    if qtype in [QuestionType.CHECKBOX]:
        if not isinstance(answer, list):
            raise ValueError("Checkbox answers must be a list of selected values.")
        if not all(isinstance(item, str) for item in answer):
            raise ValueError("Each checkbox answer must be a string.")

    elif qtype in [QuestionType.RADIO, QuestionType.DROPDOWN, QuestionType.SHORT_TEXT, QuestionType.PARAGRAPH, QuestionType.EMAIL, QuestionType.PHONE_NUMBER, QuestionType.URL, QuestionType.CURRENCY, QuestionType.ADDRESS, QuestionType.SIGNATURE]:
        if not isinstance(answer, str):
            raise ValueError(f"{qtype.value.replace('_', ' ').title()} answer must be a string.")

    elif qtype == QuestionType.NUMBER:
        if not isinstance(answer, int):
            raise ValueError("Number answer must be an integer.")

    elif qtype in [QuestionType.DATE, QuestionType.TIME]:
        if not isinstance(answer, str):
            raise ValueError(f"{qtype.value.title()} must be a valid ISO date/time string.")

    elif qtype == QuestionType.FILE_UPLOAD:
        if not isinstance(answer, dict) or "filename" not in answer or "url" not in answer:
            raise ValueError("File upload must be a dict with 'filename' and 'url'.")

    elif qtype in [QuestionType.MATRIX, QuestionType.MATRIX_RANKING]:
        if not isinstance(answer, dict):
            raise ValueError("Matrix answers must be a dict of row-question to selected value(s).")

    elif qtype == QuestionType.TIME_RANGE:
        if not isinstance(answer, dict) or "start" not in answer or "end" not in answer:
            raise ValueError("Time range must be a dict with 'start' and 'end' times.")

    elif qtype == QuestionType.SCALE:
        if not isinstance(answer, int):
            raise ValueError("Scale must be an integer.")

    return answer
