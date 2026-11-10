import re

from django.core.exceptions import ValidationError

# Canadian postal codes exclude D, F, I, O, Q, U.
# First letter excludes D, F, I, O, Q, U, W, Z.
CANADIAN_POSTAL_CODE_REGEX = re.compile(
    r"^[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJKLMNPRSTVWXYZ]\d[ABCEGHJKLMNPRSTVWXYZ]\d$",
    re.IGNORECASE,
)


def validate_canadian_postal_code(value: str) -> str:
    """Validate and normalize a Canadian postal code.

    Format must be A1A 1A1 (with or without space). Disallows D, F, I, O, Q, U.
    First letter excludes W, Z in addition to D, F, I, O, Q, U.

    Returns the normalized postal code in uppercase with a space (e.g. 'K1A 0B1').
    Raises ValidationError if the postal code is invalid.
    """
    if not value or not isinstance(value, str):
        raise ValidationError("Postal code cannot be empty.")

    compact = "".join(value.split()).upper()
    if not CANADIAN_POSTAL_CODE_REGEX.match(compact):
        raise ValidationError("Enter a valid Canadian postal code (e.g. A1A 1A1).")

    return f"{compact[:3]} {compact[3:]}"
