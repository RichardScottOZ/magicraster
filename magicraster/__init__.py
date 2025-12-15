"""Magic eye (stereogram) raster GeoTIFF generator."""

__version__ = "0.1.0"

from .stereogram import generate_stereogram, save_as_geotiff

__all__ = ["generate_stereogram", "save_as_geotiff"]
