import pytest
from django.core.exceptions import ValidationError

from core.validators import validate_canadian_postal_code


class TestValidateCanadianPostalCode:
    """Unit tests for validate_canadian_postal_code validator."""

    @pytest.mark.parametrize(
        "postal_code,expected",
        [
            ("K1A 0B1", "K1A 0B1"),
            ("M5V 2T6", "M5V 2T6"),
            ("V6T 1Z4", "V6T 1Z4"),
            ("T2N 1N4", "T2N 1N4"),
            ("H3A 0G4", "H3A 0G4"),
            ("B3H 4R2", "B3H 4R2"),
            ("R3T 2N2", "R3T 2N2"),
            ("S7N 5A2", "S7N 5A2"),
            ("E1B 2V8", "E1B 2V8"),
            ("C1A 4P3", "C1A 4P3"),
            ("A1C 5S7", "A1C 5S7"),
            ("X0A 0H0", "X0A 0H0"),
            ("Y1A 2C6", "Y1A 2C6"),
        ],
    )
    def test_valid_postal_codes(self, postal_code: str, expected: str) -> None:
        """Valid standard Canadian postal codes should pass and return normalised format."""
        assert validate_canadian_postal_code(postal_code) == expected

    @pytest.mark.parametrize(
        "postal_code,expected",
        [
            ("k1a 0b1", "K1A 0B1"),
            ("m5v 2t6", "M5V 2T6"),
            ("v6t 1z4", "V6T 1Z4"),
            ("h3a 0g4", "H3A 0G4"),
        ],
    )
    def test_lower_case_postal_codes_are_capitalized(self, postal_code: str, expected: str) -> None:
        """Lower-case postal codes should be converted to upper-case."""
        assert validate_canadian_postal_code(postal_code) == expected

    @pytest.mark.parametrize(
        "postal_code,expected",
        [
            ("K1A0B1", "K1A 0B1"),
            ("m5v2t6", "M5V 2T6"),
            ("V6T1Z4", "V6T 1Z4"),
            ("  H3A0G4  ", "H3A 0G4"),
            ("t2n  1n4", "T2N 1N4"),
        ],
    )
    def test_missing_space_and_extra_whitespace(self, postal_code: str, expected: str) -> None:
        """Postal codes without spaces or with irregular spacing should normalise to A1A 1A1."""
        assert validate_canadian_postal_code(postal_code) == expected

    @pytest.mark.parametrize(
        "invalid_postal_code",
        [
            "D1A 1A1",  # D is never allowed in Canadian postal codes
            "F1A 1A1",  # F is never allowed in Canadian postal codes
            "I1A 1A1",  # I is never allowed in Canadian postal codes
            "O1A 1A1",  # O is never allowed in Canadian postal codes
            "Q1A 1A1",  # Q is never allowed in Canadian postal codes
            "U1A 1A1",  # U is never allowed in Canadian postal codes
            "W1A 1A1",  # W is never allowed as the first character
            "Z1A 1A1",  # Z is never allowed as the first character
            "K1D 0B1",  # D in third position
            "K1A 0D1",  # D in fifth position
            "K1F 0B1",  # F in third position
            "K1I 0B1",  # I in third position
            "K1O 0B1",  # O in third position
            "K1Q 0B1",  # Q in third position
            "K1U 0B1",  # U in third position
            "K1A 0U1",  # U in fifth position
        ],
    )
    def test_invalid_letters(self, invalid_postal_code: str) -> None:
        """Postal codes containing disallowed letters or invalid first letters should fail."""
        with pytest.raises(ValidationError, match="Enter a valid Canadian postal code"):
            validate_canadian_postal_code(invalid_postal_code)

    @pytest.mark.parametrize(
        "malformed_postal_code",
        [
            "",
            "   ",
            "12345",
            "123456",
            "12345-6789",
            "90210",
            "K1A",
            "K1A 0B11",
            "1KA 0B1",
            "KAA 0B1",
            "K11 0B1",
            "K1A 011",
            "K1A BB1",
            "invalid",
        ],
    )
    def test_malformed_postal_codes(self, malformed_postal_code: str) -> None:
        """Malformed postal codes not matching A1A 1A1 pattern should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_canadian_postal_code(malformed_postal_code)

    @pytest.mark.parametrize("non_string_value", [None, 12345, [], {}])
    def test_non_string_input_raises_validation_error(self, non_string_value: object) -> None:
        """Non-string inputs should raise ValidationError."""
        with pytest.raises(ValidationError, match="Postal code cannot be empty"):
            validate_canadian_postal_code(non_string_value)  # type: ignore[arg-type]
