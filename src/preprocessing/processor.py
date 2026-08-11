"""Data preprocessing"""

import pandas as pd
from typing import Optional
from src.utils.logging import get_logger

logger = get_logger(__name__)


class DataProcessor:
    """Process and normalize lottery data"""
    
    def __init__(self):
        """Initialize data processor"""
        self.logger = get_logger(__name__)
    
    def load_csv(self, filepath: str) -> Optional[pd.DataFrame]:
        """Load CSV data file
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            DataFrame or None if failed
        """
        try:
            df = pd.read_csv(filepath)
            self.logger.info(f"Loaded {len(df)} rows from {filepath}")
            return df
        except Exception as e:
            self.logger.error(f"Error loading CSV: {e}")
            return None
    
    def save_csv(self, df: pd.DataFrame, filepath: str) -> bool:
        """Save DataFrame to CSV
        
        Args:
            df: DataFrame to save
            filepath: Path to save to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df.to_csv(filepath, index=False)
            self.logger.info(f"Saved {len(df)} rows to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving CSV: {e}")
            return False
