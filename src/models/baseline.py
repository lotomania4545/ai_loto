"""Baseline models for comparison"""

import numpy as np
from typing import List
from src.utils.logging import get_logger

logger = get_logger(__name__)


class RandomBaseline:
    """Random prediction baseline"""
    
    def __init__(
        self,
        min_val: int = 1,
        max_val: int = 43,
        predict_count: int = 6,
    ):
        """Initialize random baseline
        
        Args:
            min_val: Minimum number value
            max_val: Maximum number value
            predict_count: Number of predictions to make
        """
        self.min_val = min_val
        self.max_val = max_val
        self.predict_count = predict_count
        self.logger = get_logger(__name__)
    
    def predict(self) -> List[int]:
        """Generate random prediction
        
        Returns:
            List of predicted numbers
        """
        return sorted(
            np.random.choice(
                range(self.min_val, self.max_val + 1),
                size=self.predict_count,
                replace=False,
            ).tolist()
        )
