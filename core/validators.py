import re

from django.core.exceptions import ValidationError

# Canadian Postal Code format: A1A 1A1 or A1A1A1 (case-insensitive input)
# Disallowed letters in Canadian postal codes anywhere: D, F, I, O, Q, U
# First letter restricted: no D, F, I, O, Q, U, W, Z.
POSTAL_CODE_REGEX = re.compile(
    r"^[A-CEGHJ-NPR-TVXY]\d[A-CEGHJ-NPR-TV-Z]\s?\d[A-CEGHJ-NPR-TV-Z]\d$",
    re.IGNORECASE,
)


def validate_canadian_postal_code(value: str) -> str:
    """Validate and normalize a Canadian postal code.

    Format expected: A1A 1A1 or A1A1A1 (with optional leading/trailing whitespace).
    Normalizes input to upper-case with a single space (e.g., 'N2L 3G1').
    Disallows invalid letters (D, F, I, O, Q, U) and invalid initial letters (W, Z).
    """
    if not value or not isinstance(value, str):
        raise ValidationError("Postal code cannot be empty.")

    cleaned = value.strip().upper()

    if not POSTAL_CODE_REGEX.match(cleaned):
        raise ValidationError(
            f"'{value}' is not a valid Canadian postal code. Standard format is A1A 1A1."
        )

    compact = cleaned.replace(" ", "")
    return f"{compact[:3]} {compact[3:]}"
