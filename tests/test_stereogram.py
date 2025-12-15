"""Tests for stereogram generation."""

import tempfile
from pathlib import Path

import numpy as np
import pytest

from magicraster import generate_stereogram, save_as_geotiff


def test_generate_stereogram_basic():
    """Test basic stereogram generation."""
    stereogram = generate_stereogram(width=400, height=300)
    
    assert stereogram.shape == (300, 400)
    assert stereogram.dtype == np.uint8
    assert stereogram.min() >= 0
    assert stereogram.max() <= 255


def test_generate_stereogram_patterns():
    """Test different pattern types."""
    patterns = ["sine", "circles", "pyramid", "dinosaur"]
    
    for pattern in patterns:
        stereogram = generate_stereogram(
            width=200,
            height=150,
            pattern_type=pattern,
        )
        assert stereogram.shape == (150, 200)
        assert stereogram.dtype == np.uint8


def test_generate_stereogram_custom_params():
    """Test stereogram with custom parameters."""
    stereogram = generate_stereogram(
        width=500,
        height=400,
        pattern_type="circles",
        depth_amplitude=80.0,
        strip_width=120,
    )
    
    assert stereogram.shape == (400, 500)
    assert stereogram.dtype == np.uint8


def test_save_as_geotiff():
    """Test saving stereogram as GeoTIFF."""
    import rasterio
    
    stereogram = generate_stereogram(width=200, height=150)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.tif"
        
        save_as_geotiff(
            stereogram,
            str(output_path),
            bounds=(-10.0, 50.0, 10.0, 60.0),
            crs="EPSG:4326",
        )
        
        assert output_path.exists()
        
        # Verify the GeoTIFF
        with rasterio.open(output_path) as src:
            assert src.shape == (150, 200)
            assert src.crs.to_string() == "EPSG:4326"
            assert src.count == 1
            assert src.dtypes[0] == "uint8"


def test_save_as_geotiff_default_bounds():
    """Test saving with default bounds."""
    import rasterio
    
    stereogram = generate_stereogram(width=300, height=200)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_default.tif"
        
        save_as_geotiff(stereogram, str(output_path))
        
        assert output_path.exists()
        
        with rasterio.open(output_path) as src:
            bounds = src.bounds
            assert bounds.left == 0.0
            assert bounds.bottom == 0.0
            assert bounds.right == 300.0
            assert bounds.top == 200.0


def test_invalid_pattern():
    """Test that invalid pattern raises ValueError."""
    with pytest.raises(ValueError, match="Unknown pattern"):
        generate_stereogram(pattern_type="invalid_pattern")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
