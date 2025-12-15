#!/usr/bin/env python3
"""Generate example magic eye stereograms."""

import sys
from pathlib import Path

# Add parent directory to path to import magicraster
sys.path.insert(0, str(Path(__file__).parent.parent))

from magicraster import generate_stereogram, save_as_geotiff


def main():
    """Generate various example stereograms."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    print("Generating example magic eye stereograms...")
    
    # Example 1: Sine wave pattern
    print("\n1. Generating sine wave pattern...")
    stereogram = generate_stereogram(
        width=800,
        height=600,
        pattern_type="sine",
        depth_amplitude=50.0,
    )
    save_as_geotiff(
        stereogram,
        str(output_dir / "sine_wave.tif"),
        bounds=(-122.5, 37.5, -122.0, 38.0),
        crs="EPSG:4326",
    )
    print("   ✓ Saved sine_wave.tif")
    
    # Example 2: Concentric circles
    print("\n2. Generating concentric circles...")
    stereogram = generate_stereogram(
        width=800,
        height=600,
        pattern_type="circles",
        depth_amplitude=60.0,
    )
    save_as_geotiff(
        stereogram,
        str(output_dir / "circles.tif"),
        bounds=(0, 0, 800, 600),
    )
    print("   ✓ Saved circles.tif")
    
    # Example 3: Pyramid
    print("\n3. Generating pyramid...")
    stereogram = generate_stereogram(
        width=800,
        height=600,
        pattern_type="pyramid",
        depth_amplitude=70.0,
    )
    save_as_geotiff(
        stereogram,
        str(output_dir / "pyramid.tif"),
    )
    print("   ✓ Saved pyramid.tif")
    
    # Example 4: Dinosaur with DMC logo
    print("\n4. Generating dinosaur with DMC logo...")
    stereogram = generate_stereogram(
        width=1000,
        height=700,
        pattern_type="dinosaur",
        depth_amplitude=70.0,
    )
    save_as_geotiff(
        stereogram,
        str(output_dir / "dinosaur_dmc.tif"),
    )
    print("   ✓ Saved dinosaur_dmc.tif")
    
    # Example 5: High resolution sine
    print("\n5. Generating high-resolution sine wave...")
    stereogram = generate_stereogram(
        width=1600,
        height=1200,
        pattern_type="sine",
        depth_amplitude=80.0,
    )
    save_as_geotiff(
        stereogram,
        str(output_dir / "hires_sine.tif"),
    )
    print("   ✓ Saved hires_sine.tif")
    
    print(f"\n✓ All examples generated in '{output_dir}/' directory!")
    print("\nTo view the 3D effect:")
    print("  1. Open any .tif file in an image viewer")
    print("  2. Hold the image close to your face")
    print("  3. Focus your eyes as if looking through the image")
    print("  4. Slowly move the image away while maintaining focus")
    print("  5. A 3D shape should emerge!")


if __name__ == "__main__":
    main()
