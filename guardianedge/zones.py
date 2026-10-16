"""Compatibility imports; domain implementation lives in models.zones."""
from .models.zones import ZoneEngine, point_in_polygon
__all__ = ["ZoneEngine", "point_in_polygon"]
