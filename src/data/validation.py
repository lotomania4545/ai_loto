"""Data validation utilities"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from src.utils.logging import get_logger
from src.utils.helpers import validate_numbers

logger = get_logger(__name__)


class DataValidator:
    """Validate lottery data"""
    
    def __init__(
        self,
        min_val: int = 1,
        max_val: int = 43,
        numbers_count: int = 6,
    ):
        """Initialize validator
        
        Args:
            min_val: Minimum number value
            max_val: Maximum number value
            numbers_count: Expected count of numbers per draw
        """
        self.min_val = min_val
        self.max_val = max_val
        self.numbers_count = numbers_count
        self.logger = get_logger(__name__)
    
    def validate_draw(self, draw: Dict[str, Any]) -> bool:
        """Validate a single draw record
        
        Args:
            draw: Draw record to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check required fields
            required_fields = ["draw_number", "date", "numbers"]
            if not all(field in draw for field in required_fields):
                self.logger.warning(f"Missing required fields in draw: {draw}")
                return False
            
            # Validate numbers
            if not validate_numbers(
                draw["numbers"],
                self.min_val,
                self.max_val,
                self.numbers_count,
            ):
                self.logger.warning(f"Invalid numbers in draw: {draw}")
                return False
            
            # Validate date format
            try:
                datetime.fromisoformat(draw["date"])
            except (ValueError, TypeError):
                self.logger.warning(f"Invalid date format in draw: {draw}")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error validating draw: {e}")
            return False
    
    def validate_dataset(self, draws: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Validate entire dataset
        
        Args:
            draws: List of draw records
            
        Returns:
            Tuple of (valid_draws, invalid_draws)
        """
        valid_draws = []
        invalid_draws = []
        
        for draw in draws:
            if self.validate_draw(draw):
                valid_draws.append(draw)
            else:
                invalid_draws.append(draw)
        
        self.logger.info(
            f"Validation complete: {len(valid_draws)} valid, {len(invalid_draws)} invalid"
        )
        
        return valid_draws, invalid_draws
