"""Unit tests for core validators."""

import pytest
from django.core.exceptions import ValidationError

from core.validators import validate_canadian_postal_code


@pytest.mark.parametrize(
    "input_code, expected_output",
    [
        ("N2L 3G1", "N2L 3G1"),
        ("n2l 3g1", "N2L 3G1"),
        ("N2L3G1", "N2L 3G1"),
        ("n2l3g1", "N2L 3G1"),
        ("M5S 2Z9", "M5S 2Z9"),
        ("m5s2z9", "M5S 2Z9"),
        ("K1A 0B1", "K1A 0B1"),
        ("k1a0b1", "K1A 0B1"),
        ("V6T 1Z4", "V6T 1Z4"),
        ("T2N 1N4", "T2N 1N4"),
        ("  N2L 3G1  ", "N2L 3G1"),
        ("  n2l3g1  ", "N2L 3G1"),
    ],
)
def test_validate_canadian_postal_code_valid(input_code: str, expected_output: str) -> None:
    """Valid Canadian postal codes are normalized to upper-case with a space."""
    assert validate_canadian_postal_code(input_code) == expected_output


@pytest.mark.parametrize(
    "invalid_code",
    [
        "",
        "   ",
        "12345",
        "12345-6789",
        "N2L 3G",  # Too short
        "N2L 3G11",  # Too long
        "2NL 3G1",  # Starts with digit
        "N23 3G1",  # Digit instead of letter in position 3
        "N2L AG1",  # Letter instead of digit in position 4
        "N2L 311",  # Digit instead of letter in position 5
        "N2L 3GA",  # Letter instead of digit in position 6
        # Disallowed letters (D, F, I, O, Q, U) anywhere:
        "D1A 1A1",  # Starts with D
        "F1A 1A1",  # Starts with F
        "I1A 1A1",  # Starts with I
        "O1A 1A1",  # Starts with O
        "Q1A 1A1",  # Starts with Q
        "U1A 1A1",  # Starts with U
        "W1A 1A1",  # Starts with W (invalid first letter in Canada)
        "Z1A 1A1",  # Starts with Z (invalid first letter in Canada)
        "A1D 1A1",  # Contains D
        "A1F 1A1",  # Contains F
        "A1I 1A1",  # Contains I
        "A1O 1A1",  # Contains O
        "A1Q 1A1",  # Contains Q
        "A1U 1A1",  # Contains U
        "A1A 1D1",  # Contains D in second segment
        "A1A 1F1",  # Contains F in second segment
        "A1A 1I1",  # Contains I in second segment
        "A1A 1O1",  # Contains O in second segment
        "A1A 1Q1",  # Contains Q in second segment
        "A1A 1U1",  # Contains U in second segment
        "N2L--3G1",  # Invalid separator
        "N2L  3G1",  # Double space
    ],
)
def test_validate_canadian_postal_code_invalid(invalid_code: str) -> None:
    """Invalid postal codes raise ValidationError with descriptive messages."""
    with pytest.raises(ValidationError):
        validate_canadian_postal_code(invalid_code)


def test_validate_canadian_postal_code_non_string() -> None:
    """Non-string or None inputs raise ValidationError."""
    with pytest.raises(ValidationError):
        validate_canadian_postal_code(None)  # type: ignore[arg-type]

    with pytest.raises(ValidationError):
        validate_canadian_postal_code(12345)  # type: ignore[arg-type]
