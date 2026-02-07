"""Message bus module for decoupled channel-agent communication."""

from friday.bus.events import InboundMessage, OutboundMessage
from friday.bus.queue import MessageBus

__all__ = ["MessageBus", "InboundMessage", "OutboundMessage"]
