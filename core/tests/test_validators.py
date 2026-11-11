import pytest
from django.core.exceptions import ValidationError

from core.validators import normalize_canadian_postal_code, validate_canadian_postal_code


class TestNormalizeCanadianPostalCode:
    """Tests for the normalize_canadian_postal_code helper function."""

    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("N2L 3G1", "N2L 3G1"),
            ("n2l 3g1", "N2L 3G1"),
            ("N2L3G1", "N2L 3G1"),
            ("n2l3g1", "N2L 3G1"),
            ("  k1a   0b1  ", "K1A 0B1"),
            ("m5s 2z9", "M5S 2Z9"),
            ("V6T 1Z4", "V6T 1Z4"),
            ("h3a 0g4", "H3A 0G4"),
        ],
    )
    def test_normalizes_to_uppercase_with_space(self, raw: str, expected: str) -> None:
        """Postal codes should be converted to uppercase with a single space."""
        assert normalize_canadian_postal_code(raw) == expected

    def test_non_standard_length_returns_cleaned(self) -> None:
        """Strings that are not 6 alphanumeric chars return stripped/uppercased."""
        assert normalize_canadian_postal_code("invalid") == "INVALID"
        assert normalize_canadian_postal_code("  ") == ""


class TestValidateCanadianPostalCode:
    """Tests for validate_canadian_postal_code."""

    @pytest.mark.parametrize(
        "valid_code",
        [
            "N2L 3G1",  # Waterloo, ON
            "n2l 3g1",  # Lowercase with space
            "N2L3G1",  # Uppercase without space
            "n2l3g1",  # Lowercase without space
            "K1A 0B1",  # Ottawa, ON
            "M5S 2Z9",  # Toronto, ON
            "V6T 1Z4",  # Vancouver, BC
            "H3A 0G4",  # Montreal, QC
            "T6G 2R3",  # Edmonton, AB
            "R3T 2N2",  # Winnipeg, MB
            "S7N 5A2",  # Saskatoon, SK
            "B3H 4R2",  # Halifax, NS
            "E1B 2L5",  # Moncton, NB
            "C1A 4P3",  # Charlottetown, PE
            "A1B 3X9",  # St. John's, NL
            "X1A 2P7",  # Yellowknife, NT
            "Y1A 3V4",  # Whitehorse, YT
            "X0A 0H0",  # Iqaluit, NU
        ],
    )
    def test_valid_canadian_postal_codes(self, valid_code: str) -> None:
        """Valid Canadian postal codes should pass validation without error."""
        # Should not raise
        validate_canadian_postal_code(valid_code)

    @pytest.mark.parametrize(
        "invalid_letter_code",
        [
            "D1A 1A1",  # D is never used anywhere
            "N2D 3G1",  # D in position 3
            "F1A 1A1",  # F is never used anywhere
            "N2F 3G1",  # F in position 3
            "I1A 1A1",  # I is never used anywhere
            "N2I 3G1",  # I in position 3
            "O1A 1A1",  # O is never used anywhere
            "N2O 3G1",  # O in position 3
            "Q1A 1A1",  # Q is never used anywhere
            "N2Q 3G1",  # Q in position 3
            "U1A 1A1",  # U is never used anywhere
            "N2U 3G1",  # U in position 3
            "N2L 3D1",  # D in position 5
            "N2L 3F1",  # F in position 5
            "N2L 3I1",  # I in position 5
            "N2L 3O1",  # O in position 5
            "N2L 3Q1",  # Q in position 5
            "N2L 3U1",  # U in position 5
        ],
    )
    def test_disallowed_letters_fail(self, invalid_letter_code: str) -> None:
        """Letters D, F, I, O, Q, U are not valid anywhere in Canadian postal codes."""
        with pytest.raises(ValidationError) as exc_info:
            validate_canadian_postal_code(invalid_letter_code)
        assert "not a valid Canadian postal code" in str(exc_info.value)

    @pytest.mark.parametrize(
        "invalid_first_letter",
        [
            "W1A 1A1",  # W cannot be the first letter
            "Z1A 1A1",  # Z cannot be the first letter
        ],
    )
    def test_disallowed_first_letters_fail(self, invalid_first_letter: str) -> None:
        """W and Z cannot be the first letter of a Canadian postal code."""
        with pytest.raises(ValidationError):
            validate_canadian_postal_code(invalid_first_letter)

    @pytest.mark.parametrize(
        "invalid_format",
        [
            "",
            "   ",
            "12345",  # US zip code format
            "12345-6789",  # US zip+4
            "N2L  3G1",  # Double space inside
            "NL2 3G1",  # Letters out of order (LLD DLD)
            "2NL 3G1",  # Starts with number
            "N2L 3G",  # Too short
            "N2L 3G11",  # Too long
            "N2L-3G1",  # Hyphenated
            "SW1A 1AA",  # UK postal code
        ],
    )
    def test_invalid_formats_raise_validation_error(self, invalid_format: str) -> None:
        """Malformed or foreign postal codes must raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_canadian_postal_code(invalid_format)

    @pytest.mark.parametrize("non_string", [None, 12345, [], {}])
    def test_non_string_raises_validation_error(self, non_string: object) -> None:
        """Non-string inputs must raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_canadian_postal_code(non_string)  # type: ignore[arg-type]
