"""Helper utilities"""

from typing import List


def validate_numbers(
    numbers: List[int],
    min_val: int = 1,
    max_val: int = 43,
    expected_count: int = 6,
) -> bool:
    """Validate lottery numbers
    
    Args:
        numbers: List of numbers to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        expected_count: Expected count of numbers
        
    Returns:
        True if valid, False otherwise
    """
    if len(numbers) != expected_count:
        return False
    
    if not all(min_val <= n <= max_val for n in numbers):
        return False
    
    if len(set(numbers)) != len(numbers):
        return False
    
    return True


def calculate_hits(
    predicted: List[int],
    actual: List[int]
) -> List[int]:
    """Calculate matching numbers between predicted and actual
    
    Args:
        predicted: Predicted numbers
        actual: Actual numbers
        
    Returns:
        List of matching numbers
    """
    return sorted(list(set(predicted) & set(actual)))
