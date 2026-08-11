"""Evaluation metrics"""

from typing import List, Dict, Any
from src.utils.logging import get_logger
from src.utils.helpers import calculate_hits

logger = get_logger(__name__)


class Metrics:
    """Calculate evaluation metrics"""
    
    @staticmethod
    def calculate_hit_count(
        predicted: List[int],
        actual: List[int],
    ) -> int:
        """Calculate number of hits
        
        Args:
            predicted: Predicted numbers
            actual: Actual numbers
            
        Returns:
            Number of matching numbers
        """
        hits = calculate_hits(predicted, actual)
        return len(hits)
    
    @staticmethod
    def calculate_accuracy(
        predictions: List[List[int]],
        actuals: List[List[int]],
    ) -> float:
        """Calculate average accuracy
        
        Args:
            predictions: List of predictions
            actuals: List of actual results
            
        Returns:
            Average hit rate
        """
        if not predictions:
            return 0.0
        
        hits = [
            Metrics.calculate_hit_count(pred, actual)
            for pred, actual in zip(predictions, actuals)
        ]
        return sum(hits) / len(hits)
