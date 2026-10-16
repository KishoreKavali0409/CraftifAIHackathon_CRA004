"""Compatibility imports; domain implementation lives in models.zones."""
# Preserve existing integrations while keeping one domain implementation.
from .models.zones import ZoneEngine, point_in_polygon
__all__ = ["ZoneEngine", "point_in_polygon"]
