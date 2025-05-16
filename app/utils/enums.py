from enum import Enum


class OptionType(str, Enum):
    RADIO = "radio"
    MULTIPLE_GRID = "multiple_grid"
    SCALE = "scale"
    CHECKBOX = "checkbox"
    DROPDOWN = "dropdown"

class QuestionType(str, Enum):
    RADIO = "radio"
    MULTIPLE_GRID = "multiple_grid"
    SCALE = "scale"
    CHECKBOX = "checkbox"
    DROPDOWN = "dropdown"
    SHORT_TEXT = "short_text"
    PARAGRAPH = "paragraph"
    NUMBER = "number"
    DATE = "date"
    TIME = "time"
    FILE_UPLOAD = "file_upload"
    EMAIL = "email"
    PHONE = "phone"
    URL = "url"
    CURRENCY = "currency"
    ADDRESS = "address"
    SIGNATURE = "signature"
    MATRIX = "matrix"
    MATRIX_RANKING = "matrix_ranking"
    TIMEZONE = "timezone"
    FILE = "file"
    PHONE_NUMBER = "phone_number"
    TIME_RANGE = "time_range"
