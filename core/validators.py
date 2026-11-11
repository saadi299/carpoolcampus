import re

from django.core.exceptions import ValidationError

# Canadian postal codes alternate letter and digit: A1A 1A1.
# Canada Post rules:
# 1. Letters D, F, I, O, Q, U are not used anywhere in a postal code.
# 2. Letters W and Z are not used as the first letter.
# Valid first letters: A, B, C, E, G, H, J, K, L, M, N, P, R, S, T, V, X, Y
VALID_FIRST_LETTERS = "ABCEGHJKLMNPRSTVXY"
VALID_LETTERS = "ABCEGHJKLMNPRSTVWXYZ"

CANADIAN_POSTAL_CODE_REGEX = re.compile(
    rf"^[{VALID_FIRST_LETTERS}]\d[{VALID_LETTERS}]\s?\d[{VALID_LETTERS}]\d$",
    re.IGNORECASE,
)


def normalize_canadian_postal_code(value: str) -> str:
    """Normalize a Canadian postal code to standard format 'A1A 1A1'.

    Removes surrounding whitespace, converts to uppercase, and ensures
    a single space between the forward sortation area (FSA) and local
    delivery unit (LDU).
    """
    cleaned = re.sub(r"\s+", "", value.strip()).upper()
    if len(cleaned) == 6:
        return f"{cleaned[:3]} {cleaned[3:]}"
    return cleaned


def validate_canadian_postal_code(value: str) -> None:
    """Validate that a string represents a valid Canadian postal code.

    Format must conform to A1A 1A1 (optional middle space accepted).
    The letters D, F, I, O, Q, and U are never used in Canadian postal codes.
    The first letter must belong to the valid Canadian postal district letters
    (cannot be D, F, I, O, Q, U, W, or Z).
    """
    if not value or not isinstance(value, str):
        raise ValidationError("Postal code cannot be empty.")

    stripped = value.strip()
    if not CANADIAN_POSTAL_CODE_REGEX.match(stripped):
        raise ValidationError(
            f"'{value}' is not a valid Canadian postal code. "
            "Expected format is 'A1A 1A1' using valid Canadian postal letters "
            "(excluding D, F, I, O, Q, U and W/Z as first letter)."
        )
