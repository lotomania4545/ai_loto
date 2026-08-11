"""Configuration management for ai_loto"""

import os
from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel, Field


class ProjectConfig(BaseModel):
    """Project configuration"""
    name: str
    version: str
    description: str
    author: str


class LotteryConfig(BaseModel):
    """Lottery configuration"""
    type: str
    country: str
    numbers_min: int = Field(default=1, alias="numbers.min")
    numbers_max: int = Field(default=43, alias="numbers.max")
    numbers_count: int = Field(default=6, alias="numbers.count")
    bonus_included: bool = Field(default=False, alias="bonus_included")


def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from YAML file
    
    Args:
        config_path: Path to config file. If None, uses default location.
        
    Returns:
        Dictionary with configuration
    """
    if config_path is None:
        config_path = os.path.join(Path(__file__).parent.parent, "configs", "config.yaml")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    return config


def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).parent.parent


def get_data_dir(subdir: str = None) -> Path:
    """Get data directory path
    
    Args:
        subdir: Subdirectory name (raw, processed, features, predictions, results)
        
    Returns:
        Path to data directory
    """
    root = get_project_root()
    data_dir = root / "data"
    
    if subdir:
        data_dir = data_dir / subdir
    
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_log_dir() -> Path:
    """Get logs directory path"""
    root = get_project_root()
    log_dir = root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir
