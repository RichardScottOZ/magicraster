"""Command-line interface for magic raster generation."""

import argparse
import sys
from pathlib import Path
from typing import Optional, Tuple

from .stereogram import generate_stereogram, save_as_geotiff


def parse_bounds(bounds_str: str) -> Tuple[float, float, float, float]:
    """Parse bounds string in format 'minx,miny,maxx,maxy'."""
    try:
        parts = [float(x.strip()) for x in bounds_str.split(',')]
        if len(parts) != 4:
            raise ValueError
        return tuple(parts)
    except (ValueError, AttributeError):
        raise argparse.ArgumentTypeError(
            "Bounds must be in format 'minx,miny,maxx,maxy'"
        )


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate magic eye (stereogram) raster GeoTIFF images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a basic sine wave stereogram
  magicraster output.tif
  
  # Generate a circular pattern with custom size
  magicraster output.tif --width 1024 --height 768 --pattern circles
  
  # Generate with geographic bounds
  magicraster output.tif --bounds "-122.5,37.5,-122.0,38.0" --crs EPSG:4326
  
  # Generate a pyramid with custom depth
  magicraster output.tif --pattern pyramid --depth 80
        """,
    )
    
    parser.add_argument(
        "output",
        type=str,
        help="Output GeoTIFF file path",
    )
    
    parser.add_argument(
        "--width",
        type=int,
        default=800,
        help="Width of the image in pixels (default: 800)",
    )
    
    parser.add_argument(
        "--height",
        type=int,
        default=600,
        help="Height of the image in pixels (default: 600)",
    )
    
    parser.add_argument(
        "--pattern",
        type=str,
        choices=["sine", "circles", "pyramid", "random", "dinosaur"],
        default="sine",
        help="Depth pattern type (default: sine)",
    )
    
    parser.add_argument(
        "--depth",
        type=float,
        default=50.0,
        help="Depth amplitude (0-100, default: 50.0)",
    )
    
    parser.add_argument(
        "--strip-width",
        type=int,
        default=100,
        help="Width of the random pattern strip (default: 100)",
    )
    
    parser.add_argument(
        "--bounds",
        type=parse_bounds,
        default=None,
        help="Geographic bounds as 'minx,miny,maxx,maxy'",
    )
    
    parser.add_argument(
        "--crs",
        type=str,
        default="EPSG:4326",
        help="Coordinate reference system (default: EPSG:4326)",
    )
    
    parser.add_argument(
        "--eye-separation",
        type=float,
        default=0.12,
        help="Eye separation factor (default: 0.12)",
    )
    
    parser.add_argument(
        "--depth-scale",
        type=float,
        default=0.3,
        help="Depth scale factor (default: 0.3)",
    )
    
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite output file if it exists without prompting",
    )
    
    args = parser.parse_args()
    
    # Validate output path
    output_path = Path(args.output)
    if output_path.exists() and not args.force:
        response = input(f"File {output_path} exists. Overwrite? [y/N]: ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating magic eye stereogram...")
    print(f"  Pattern: {args.pattern}")
    print(f"  Size: {args.width}x{args.height}")
    print(f"  Depth: {args.depth}")
    
    # Generate stereogram
    try:
        stereogram = generate_stereogram(
            width=args.width,
            height=args.height,
            pattern_type=args.pattern,
            depth_amplitude=args.depth,
            strip_width=args.strip_width,
            eye_separation=args.eye_separation,
            depth_scale=args.depth_scale,
        )
        
        print(f"Saving to {output_path}...")
        
        # Save as GeoTIFF
        save_as_geotiff(
            stereogram,
            str(output_path),
            bounds=args.bounds,
            crs=args.crs,
        )
        
        print(f"✓ Successfully created {output_path}")
        print(f"\nTo view the 3D effect:")
        print("  1. Hold the image close to your face")
        print("  2. Focus your eyes as if looking through the image")
        print("  3. Slowly move the image away while maintaining focus")
        print("  4. A 3D shape should emerge!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
