import pytest
from roagg.utils import is_valid_doi, find_doi_in_text, string_word_count


class TestIsValidDoi:
    """Test cases for the is_valid_doi function."""

    def test_valid_doi_basic(self):
        """Test basic valid DOI format."""
        assert is_valid_doi("10.1234/example")

    def test_valid_doi_with_longer_prefix(self):
        """Test valid DOI with longer prefix number."""
        assert is_valid_doi("10.123456789/test")

    def test_valid_doi_with_special_characters(self):
        """Test valid DOI with allowed special characters."""
        assert is_valid_doi("10.1000/test-example_123")
        assert is_valid_doi("10.1000/test.example")
        assert is_valid_doi("10.1000/test(123)")
        assert is_valid_doi("10.1000/test;123")
        assert is_valid_doi("10.1000/test:123")
        assert is_valid_doi("10.1000/test/subpath")

    def test_valid_doi_with_uppercase(self):
        """Test valid DOI with uppercase letters."""
        assert is_valid_doi("10.1234/ABC-DEF")
        assert is_valid_doi("10.1234/Test-Example")

    def test_valid_doi_with_numbers(self):
        """Test valid DOI with various numbers in suffix."""
        assert is_valid_doi("10.1234/123456789")

    def test_valid_doi_complex(self):
        """Test complex real-world DOI examples."""
        assert is_valid_doi("10.1000/182")
        assert is_valid_doi("10.1038/nphys1170")
        assert is_valid_doi("10.1016/j.cell.2009.01.002")

    def test_invalid_doi_missing_prefix(self):
        """Test invalid DOI without '10.' prefix."""
        assert not is_valid_doi("11.1234/example")
        assert not is_valid_doi("1.1234/example")
        assert not is_valid_doi("1234/example")

    def test_invalid_doi_short_prefix_number(self):
        """Test invalid DOI with too short prefix number."""
        assert not is_valid_doi("10.123/example")  # Only 3 digits
        assert not is_valid_doi("10.12/example")   # Only 2 digits
        assert not is_valid_doi("10.1/example")    # Only 1 digit

    def test_invalid_doi_missing_slash(self):
        """Test invalid DOI without slash separator."""
        assert not is_valid_doi("10.1234-example")
        assert not is_valid_doi("10.1234.example")

    def test_invalid_doi_missing_suffix(self):
        """Test invalid DOI without suffix."""
        assert not is_valid_doi("10.1234/")
        assert not is_valid_doi("10.1234")

    def test_invalid_doi_empty_string(self):
        """Test invalid DOI with empty string."""
        assert not is_valid_doi("")

    def test_invalid_doi_whitespace(self):
        """Test invalid DOI with whitespace."""
        assert not is_valid_doi("10.1234/ example")
        assert not is_valid_doi("10.1234 /example")
        assert not is_valid_doi(" 10.1234/example")
        assert not is_valid_doi("10.1234/example ")

    def test_invalid_doi_only_prefix(self):
        """Test invalid DOI with only the prefix."""
        assert not is_valid_doi("10.")

    def test_invalid_doi_non_numeric_prefix(self):
        """Test invalid DOI with non-numeric prefix."""
        assert not is_valid_doi("10.abcd/example")

    def test_edge_case_minimum_valid_length(self):
        """Test DOI with minimum valid prefix length (4 digits)."""
        assert is_valid_doi("10.1000/a")

    def test_edge_case_maximum_valid_length(self):
        """Test DOI with maximum valid prefix length (9 digits)."""
        assert is_valid_doi("10.123456789/a")

    def test_edge_case_too_long_prefix(self):
        """Test DOI with prefix longer than 9 digits."""
        assert not is_valid_doi("10.1234567890/example")


class TestFindDoiInText:
    """Test cases for the find_doi_in_text function."""

    def test_pangea_doi_url(self):
        """PANGAEA DOI URL."""
        text = "https://doi.pangaea.de/10.1234/example"
        result = find_doi_in_text(text)
        assert result == ["10.1234/example"]

    def test_zenodo_doi_url(self):
        """ZENODO DOI URL."""
        text = "https://zenodo.org/doi/10.1234/example"
        result = find_doi_in_text(text)
        assert result == ["10.1234/example"]

    def test_single_doi_in_text(self):
        """Test finding a single DOI in text."""
        text = "This is a reference to 10.1234/example in the middle of text."
        result = find_doi_in_text(text)
        assert result == ["10.1234/example"]

    def test_multiple_dois_in_text(self):
        """Test finding multiple DOIs in text."""
        text = "See 10.1234/first and also 10.5678/second for more info."
        result = find_doi_in_text(text)
        assert result == ["10.1234/first", "10.5678/second"]

    def test_doi_at_start_of_text(self):
        """Test finding DOI at the beginning of text."""
        text = "10.1234/example is the DOI for this article."
        result = find_doi_in_text(text)
        assert result == ["10.1234/example"]

    def test_doi_at_end_of_text(self):
        """Test finding DOI at the end of text."""
        text = "The DOI for this article is 10.1234/example"
        result = find_doi_in_text(text)
        assert result == ["10.1234/example"]

    def test_doi_with_special_characters(self):
        """Test finding DOIs with various special characters."""
        text = "DOI: 10.1038/nphys1170 and 10.1016/j.cell.2009.01.002"
        result = find_doi_in_text(text)
        assert len(result) == 2
        assert "10.1038/nphys1170" in result
        assert "10.1016/j.cell.2009.01.002" in result

    def test_doi_with_parentheses(self):
        """Test finding DOI with parentheses."""
        text = "See DOI 10.1234/test(2024) for details."
        result = find_doi_in_text(text)
        assert "10.1234/test(2024)" in result

    def test_no_doi_in_text(self):
        """Test text without any DOI."""
        text = "This text has no DOI at all."
        result = find_doi_in_text(text)
        assert result == []

    def test_empty_text(self):
        """Test with empty string."""
        result = find_doi_in_text("")
        assert result == []

    def test_doi_with_url(self):
        """Test finding DOI within a URL."""
        text = "Visit https://doi.org/10.1234/example for the article."
        result = find_doi_in_text(text)
        assert "10.1234/example" in result

    def test_doi_minimum_prefix_length(self):
        """Test DOI with minimum prefix length (4 digits)."""
        text = "The DOI is 10.1000/test"
        result = find_doi_in_text(text)
        assert result == ["10.1000/test"]

    def test_doi_maximum_prefix_length(self):
        """Test DOI with maximum prefix length (9 digits)."""
        text = "The DOI is 10.123456789/test"
        result = find_doi_in_text(text)
        assert result == ["10.123456789/test"]

    def test_invalid_doi_too_short_prefix(self):
        """Test that DOIs with too short prefix are not found."""
        text = "This is not a valid DOI: 10.123/test"
        result = find_doi_in_text(text)
        assert result == []

    def test_doi_with_underscores(self):
        """Test finding DOI with underscores."""
        text = "DOI: 10.1234/test_example_123"
        result = find_doi_in_text(text)
        assert "10.1234/test_example_123" in result

    def test_doi_in_multiline_text(self):
        """Test finding DOI in multiline text."""
        text = """This is a paper.
        The DOI is 10.1234/example
        It was published in 2024."""
        result = find_doi_in_text(text)
        assert result == ["10.1234/example"]

    def test_doi_with_mixed_case(self):
        """Test finding DOI with mixed case letters."""
        text = "DOI: 10.1234/AbCdEf123"
        result = find_doi_in_text(text)
        assert "10.1234/AbCdEf123" in result

    def test_real_world_dois(self):
        """Test finding real-world DOI examples."""
        text = "See 10.1038/nature12373 and 10.1126/science.1259855 for more information."
        result = find_doi_in_text(text)
        assert len(result) == 2
        assert "10.1038/nature12373" in result
        assert "10.1126/science.1259855" in result

class TestStringWordCount:
    def test_single_word(self):
        """Test with a single word."""
        assert string_word_count("file.csv") == 1
        assert string_word_count("another_file[2].jpg") == 1

    def test_multiple_words(self):
        """Test with multiple words."""
        assert string_word_count("Hello World from Roagg") == 4

    def test_leading_trailing_spaces(self):
        """Test with leading and trailing spaces."""
        # "Leading and trailing spaces" = 4 words (not 5)
        assert string_word_count("   Leading and trailing spaces   ") == 4

    def test_multiple_spaces_between_words(self):
        """Test with multiple spaces between words."""
        # "Multiple spaces between words" = 4 words (not 5)
        assert string_word_count("Multiple   spaces   between   words") == 4

    def test_empty_string(self):
        """Test with an empty string."""
        assert string_word_count("") == 0

    def test_string_with_only_spaces(self):
        """Test with a string containing only spaces."""
        assert string_word_count("     ") == 0

    def test_string_with_newlines_and_tabs(self):
        """Test with newlines and tabs."""
        assert string_word_count("Hello\nWorld\tfrom Roagg") == 4

    def test_string_with_punctuation(self):
        """Test with punctuation - split() doesn't separate on punctuation."""
        # "Hello, world! This is Roagg." = 5 words (punctuation stays attached)
        assert string_word_count("Hello, world! This is Roagg.") == 5

    def test_string_with_special_characters(self):
        """Test with special characters - split() doesn't separate on special chars."""
        # "datafile.csv is ready!" = 3 words
        assert string_word_count("datafile.csv is ready!  ") == 3

    def test_string_with_numeric_characters(self):
        """Test with numeric characters - split() doesn't separate on dots."""
        # "Version 2.0 of the software" = 5 words (2.0 is one word)
        assert string_word_count("Version 2.0 of the software    ") == 5