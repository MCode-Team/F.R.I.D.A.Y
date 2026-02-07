"""Chat channels module with plugin architecture."""

from friday.channels.base import BaseChannel
from friday.channels.manager import ChannelManager

__all__ = ["BaseChannel", "ChannelManager"]
