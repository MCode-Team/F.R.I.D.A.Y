"""Configuration module for friday."""

from friday.config.loader import load_config, get_config_path
from friday.config.schema import Config

__all__ = ["Config", "load_config", "get_config_path"]
