"""Tests for utility functions"""

import pytest
from src.utils.helpers import validate_numbers, calculate_hits


class TestValidateNumbers:
    """Test number validation"""
    
    def test_valid_numbers(self):
        """Test valid lottery numbers"""
        numbers = [1, 5, 12, 23, 34, 43]
        assert validate_numbers(numbers) is True
    
    def test_invalid_count(self):
        """Test invalid count"""
        numbers = [1, 5, 12, 23, 34]
        assert validate_numbers(numbers) is False
    
    def test_out_of_range(self):
        """Test out of range numbers"""
        numbers = [1, 5, 12, 23, 34, 44]
        assert validate_numbers(numbers) is False
    
    def test_duplicates(self):
        """Test duplicate numbers"""
        numbers = [1, 5, 12, 23, 34, 1]
        assert validate_numbers(numbers) is False


class TestCalculateHits:
    """Test hit calculation"""
    
    def test_perfect_match(self):
        """Test perfect match"""
        predicted = [1, 5, 12, 23, 34, 43]
        actual = [1, 5, 12, 23, 34, 43]
        hits = calculate_hits(predicted, actual)
        assert len(hits) == 6
    
    def test_partial_match(self):
        """Test partial match"""
        predicted = [1, 5, 12, 23, 34, 43]
        actual = [1, 5, 12, 40, 41, 42]
        hits = calculate_hits(predicted, actual)
        assert len(hits) == 3
    
    def test_no_match(self):
        """Test no match"""
        predicted = [1, 5, 12, 23, 34, 43]
        actual = [2, 6, 13, 24, 35, 44]
        hits = calculate_hits(predicted, actual)
        assert len(hits) == 0
